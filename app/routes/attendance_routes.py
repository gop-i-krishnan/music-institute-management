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
from app.schemas.common_schema import (
    StandardResponse
)

router = APIRouter()


# Mark attendance for a student. Only admin users can access this route.
# The service layer handles student validation and database insert work.
@router.post(
    "/attendance",
    response_model=StandardResponse
)
def mark_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_only)
):
    # Delegate record creation so route code stays focused on HTTP concerns.
    new_attendance = create_attendance_record(
        attendance,
        db,
        current_user
    )

    return StandardResponse(
        success=True,
        message="Attendance marked successfully",
        data={
            "attendance_id": new_attendance.id
        }
    )


# Return all attendance records for a specific student.
# Authenticated users can view attendance, but only admins can mark it.
@router.get(
    "/students/{student_id}/attendance",
    response_model=list[AttendanceResponse]
)
def get_student_attendance(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Confirm the student exists before returning related attendance records.
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # SQLAlchemy loads attendance rows through Student.attendance_records.
    return student.attendance_records
