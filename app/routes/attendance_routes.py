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
    AttendanceCreate
)

from app.core.security import (
    admin_only
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
        "message": "Attendance marked successfully"
    }