from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


# SQLAlchemy model for students enrolled in the institute.
class Student(Base):
    __tablename__ = "students"

    # Basic student profile fields.
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    course = Column(String)
    
    # All attendance records connected to this student.
    attendance_records = relationship(
        "Attendance",
        back_populates="student"
    )
