from pydantic import BaseModel
from app.schemas.attendance_schema import (
    AttendanceResponse
)

class StudentCreate(BaseModel):
    name: str
    email: str
    phone: str
    course: str
    
class StudentUpdate(BaseModel):
    name: str
    email: str
    phone: str
    course: str

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    course: str

    attendance_records: list[AttendanceResponse] = []

    model_config = {
        "from_attributes": True
    }