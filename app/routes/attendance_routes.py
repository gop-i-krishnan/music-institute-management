from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student

from app.schemas.attendance_schema import (
    AttendanceCreate,
    AttendanceResponse
)
from app.services.attendance_service import (
    create_attendance_record
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
    new_attendance = create_attendance_record(
        attendance,
        db,
        current_user
    )

    return {
        "message": "Attendance marked successfully",
        "attendance_id": new_attendance.id
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