from pydantic import BaseModel
from app.schemas.attendance_schema import (
    AttendanceResponse
)


# Request body used when creating a student.
# FastAPI validates incoming JSON against these required fields.
class StudentCreate(BaseModel):
    name: str
    email: str
    phone: str
    course: str
    

# Request body used when updating a student.
# The current update route expects a full replacement of these fields.
class StudentUpdate(BaseModel):
    name: str
    email: str
    phone: str
    course: str


# Response model for returning student details with attendance records.
# model_validate can convert matching SQLAlchemy Student objects into this shape.
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
