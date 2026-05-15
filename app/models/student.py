from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


# SQLAlchemy model for students enrolled in the institute.
# This model maps directly to the students database table.
class Student(Base):
    __tablename__ = "students"

    # Primary key used by route path parameters and relationships.
    id = Column(Integer, primary_key=True, index=True)

    # Basic student profile fields.
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    course = Column(String)

    # Optional address field added through a later Alembic migration.
    address = Column(String)
    
    # All attendance records connected to this student.
    # back_populates keeps this relationship linked with Attendance.student.
    attendance_records = relationship(
        "Attendance",
        back_populates="student"
    )
