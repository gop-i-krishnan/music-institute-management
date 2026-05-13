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


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id")
    )

    status = Column(String)

    marked_by = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    student = relationship(
        "Student",
        back_populates="attendance_records"
    )