from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.schemas.student_schema import StudentCreate
from app.schemas.student_schema import StudentUpdate
from app.core.security import get_current_user
from app.core.security import admin_only

router = APIRouter()


@router.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
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
    
@router.get("/students")
def get_students(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": "Protected route working",
        "current_user": current_user
    }

@router.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    return student

@router.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_student: StudentUpdate,
    db: Session = Depends(get_db)
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