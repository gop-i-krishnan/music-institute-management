from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.attendance import Attendance
from app.models.student import Student

from app.schemas.attendance_schema import (
    AttendanceCreate,
    AttendanceResponse
)

from app.core.security import (
    admin_only,
    get_current_user
)

router = APIRouter()


@router.post("/attendance")
def mark_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_only)
):
    student = db.query(Student).filter(
        Student.id == attendance.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    new_attendance = Attendance(
        student_id=attendance.student_id,
        status=attendance.status,
        marked_by=current_user["email"]
    )

    db.add(new_attendance)

    db.commit()

    db.refresh(new_attendance)

    return {
        "student_name": student.name,
        "attendance_status": new_attendance.status
    }

@router.get(
    "/students/{student_id}/attendance",
    response_model=list[AttendanceResponse]
)
def get_student_attendance(
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

    return student.attendance_records