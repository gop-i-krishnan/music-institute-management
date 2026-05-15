from sqlalchemy import desc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
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
    db.commit()
    db.refresh(new_student)

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
    response_model=StudentResponse
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

    return student

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

    # Copy validated request values onto the database model.
    student.name = updated_student.name
    student.email = updated_student.email
    student.phone = updated_student.phone
    student.course = updated_student.course

    # Persist the changes and refresh the model for the response.
    db.commit()
    db.refresh(student)

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

    return StandardResponse(
        success=True,
        message="Student deleted successfully"
    )
