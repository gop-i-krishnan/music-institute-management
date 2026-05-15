from unittest import skip
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

router = APIRouter()


# Create a new student record. Only admin users can access this route.
@router.post("/students")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_only)
):
    new_student = Student(
        name=student.name,
        email=student.email,
        phone=student.phone,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student created successfully"
    }
    
# Retrieve students using dynamic filtering, searching,
# sorting, and paginated response architecture.
@router.get("/students")
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
    # Start with the base student query and narrow it down as filters are provided.
    query = db.query(Student)

    if course:
        query = query.filter(
            Student.course.ilike(f"%{course}%")
        )

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

    # Calculate pagination metadata before applying offset and limit.
    total = query.count()
    total_pages = (total + limit - 1) // limit
    skip = (page - 1) * limit
    students = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "data": students
    }

# Fetch a single student by ID for authenticated users.
@router.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

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
    student = db.query(Student).filter(Student.id == student_id).first()

    student.name = updated_student.name
    student.email = updated_student.email
    student.phone = updated_student.phone
    student.course = updated_student.course

    db.commit()
    db.refresh(student)

    return {
        "message": "Student updated successfully"
    }
    
# Delete a student record by ID. Only admin users can access this route.
@router.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_only)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)

    db.commit()

    return {
        "message": "Student deleted successfully"
    }
