from pydantic import BaseModel


class AttendanceCreate(BaseModel):
    student_id: int
    status: str