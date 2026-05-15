from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from datetime import datetime

from app.database import Base
from sqlalchemy.orm import relationship


# SQLAlchemy model for attendance entries marked for students.
class Attendance(Base):
    __tablename__ = "attendance"

    # Primary key for each attendance record.
    id = Column(Integer, primary_key=True, index=True)

    # Links each attendance record to a student.
    student_id = Column(
        Integer,
        ForeignKey("students.id")
    )

    # Attendance status such as present or absent.
    status = Column(String)

    # Email of the admin user who marked the attendance.
    marked_by = Column(String)

    # Timestamp automatically set when the attendance record is created.
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    # Relationship back to the student who owns this attendance record.
    student = relationship(
        "Student",
        back_populates="attendance_records"
    )
