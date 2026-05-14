from fastapi import HTTPException

from app.models.student import Student
from app.models.attendance import Attendance


def create_attendance_record(
    attendance,
    db,
    current_user
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

    return new_attendance