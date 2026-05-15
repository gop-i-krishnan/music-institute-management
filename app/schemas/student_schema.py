from pydantic import BaseModel
from app.schemas.attendance_schema import (
    AttendanceResponse
)


# Request body used when creating a student.
class StudentCreate(BaseModel):
    name: str
    email: str
    phone: str
    course: str
    

# Request body used when updating a student.
class StudentUpdate(BaseModel):
    name: str
    email: str
    phone: str
    course: str


# Response model for returning student details with attendance records.
class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    course: str

    attendance_records: list[AttendanceResponse] = []

    # Allows Pydantic to read values directly from SQLAlchemy model objects.
    model_config = {
        "from_attributes": True
    }
