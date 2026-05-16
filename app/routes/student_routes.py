from sqlalchemy import desc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.schemas.student_schema import StudentCreate
from app.schemas.student_schema import StudentUpdate
from app.core.security import get_current_user
from app.core.security import admin_only
from app.schemas.student_schema import (
    StudentResponse
)
from app.schemas.common_schema import (
    StandardResponse
)
from sqlalchemy.exc import IntegrityError
from app.core.logger import logger

router = APIRouter()


# Create a new student record and return it inside the standard API response.
# Access is restricted to admins through the admin_only dependency.
@router.post(
    "/students",
    response_model=StandardResponse
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_only)
):
    # Build the SQLAlchemy model object from the validated request body.
    new_student = Student(
        name=student.name,
        email=student.email,
        phone=student.phone,
        course=student.course
    )

    # Save the student and refresh it so generated fields like id are available.
    db.add(new_student)
    try:
        # Attempt database transaction commit
        db.commit()

        # Refresh ORM object with generated DB values
        db.refresh(new_student)
        
        # Log successful student creation activity
        logger.info(
            f"Student created successfully: "
            f"{new_student.email}"
        )

    except IntegrityError:
        # Log duplicate email violation attempt
        logger.warning(
            f"Duplicate student email attempted: "
            f"{student.email}"
        )
        # Rollback failed transaction to keep session clean
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Student email already exists"
        )

    # Convert the ORM object into the response schema before returning it.
    return StandardResponse(
        success=True,
        message="Student created successfully",
        data=StudentResponse.model_validate(new_student)
    )

# Retrieve students using optional filters, safe sorting, and pagination.
# The response uses StandardResponse so list data and pagination meta stay consistent.
@router.get(
    "/students",
    response_model=StandardResponse
)
def get_students(
    course: str = None,
    name: str = None,
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 5,
    sort_by: str = "id",
    sort_order: str = "asc",
    current_user: dict = Depends(get_current_user)
):
    # Start with all students and narrow the query only when filters are provided.
    query = db.query(Student)

    # Filter by partial course name using a case-insensitive match.
    if course:
        query = query.filter(
            Student.course.ilike(f"%{course}%")
        )

    # Filter by partial student name using a case-insensitive match.
    if name:
        query = query.filter(
            Student.name.ilike(f"%{name}%")
        )

    # Restrict sortable fields to prevent invalid
    # attribute access and unsafe query behavior.
    allowed_sort_fields = [
        "id",
        "name",
        "email",
        "course"
    ]
    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    # Apply the requested sort direction to the selected student model field.
    if sort_order == "desc":
        query = query.order_by(
            desc(getattr(Student, sort_by))
        )
    else:
        query = query.order_by(
            getattr(Student, sort_by)
        )

    # Count all matching rows before slicing the query for the current page.
    total = query.count()
    total_pages = (total + limit - 1) // limit
    skip = (page - 1) * limit

    # Fetch only the rows that belong to the requested page.
    students = query.offset(skip).limit(limit).all()

    # Return records plus metadata that the frontend can use for pagination UI.
    return StandardResponse(
        success=True,
        message="Students retrieved successfully",
        data=[StudentResponse.model_validate(s) for s in students],
        meta={
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    )

# Fetch a single student by ID, including attendance data from the relationship.
@router.get(
    "/students/{student_id}",
    response_model=StandardResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Look up the student by primary key.
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    # Return a clear 404 if the requested student does not exist.
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return StandardResponse(
        success=True,
        message="Student retrieved successfully",
        data=StudentResponse.model_validate(student)
    )

# Update an existing student record. Only admin users can access this route.
@router.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_student: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_only)
):
    # Load the existing student record before changing its fields.
    student = db.query(Student).filter(Student.id == student_id).first()
    # Ensure the student exists before attempting updates.
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Copy validated request values onto the database model.
    update_data = updated_student.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    try:
        # Attempt database transaction commit
        db.commit()

        # Refresh ORM object with updated database values
        db.refresh(student)

        logger.info(
            f"Student updated successfully: "
            f"{student.email}"
        )

    except IntegrityError:
        # Rollback failed transaction to reset session state
        db.rollback()

        logger.warning(
            f"Duplicate email update attempted: "
            f"{updated_student.email}"
        )

        raise HTTPException(
            status_code=400,
            detail="Student email already exists"
        )

    return StandardResponse(
        success=True,
        message="Student updated successfully",
        data=StudentResponse.model_validate(student)
    )

# Delete a student record by ID. Only admin users can access this route.
@router.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_only)
):
    # Find the student first so the API can return 404 for missing records.
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Remove the student row from the database.
    db.delete(student)

    db.commit()

    logger.info(
        f"Student deleted successfully: "
        f"{student.email}"
    )

    return StandardResponse(
        success=True,
        message="Student deleted successfully"
    )
