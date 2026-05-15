from fastapi import HTTPException

from app.models.student import Student
from app.models.attendance import Attendance


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
        status=attendance.status,
        marked_by=current_user["email"]
    )

    # Insert the attendance row and refresh it to get generated values like id.
    db.add(new_attendance)

    db.commit()

    db.refresh(new_attendance)

    return new_attendance
