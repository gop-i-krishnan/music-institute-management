from fastapi import HTTPException

from app.models.student import Student
from app.models.attendance import Attendance
from sqlalchemy.exc import SQLAlchemyError
from app.core.logger import logger


# Create an attendance record after confirming the student exists.
# Keeping this in a service makes the route easier to read and reuse.
def create_attendance_record(
    attendance,
    db,
    current_user
):
    # Validate that the attendance request points to a real student.
    student = db.query(Student).filter(
        Student.id == attendance.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Store who marked the attendance using the current user's email.
    new_attendance = Attendance(
        student_id=attendance.student_id,
        # Normalize attendance status format for consistent database storage.
        status=attendance.status.capitalize(),
        marked_by=current_user["email"]
    )

    # Persist attendance safely while handling transaction failures gracefully.
    db.add(new_attendance)
    try:
        # Attempt database transaction commit.
        db.commit()

        # Refresh ORM object with generated DB values.
        db.refresh(new_attendance)

        logger.info(
            f"Attendance marked for "
            f"student_id={attendance.student_id}"
        )

    except SQLAlchemyError as e:
        # Rollback failed transaction to reset session state.
        db.rollback()

        logger.error(
            f"Attendance creation failed for "
            f"student_id={attendance.student_id}: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to mark attendance"
        )

    return new_attendance
