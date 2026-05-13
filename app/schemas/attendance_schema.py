from pydantic import BaseModel


class AttendanceCreate(BaseModel):
    student_id: int
    status: str


class AttendanceResponse(BaseModel):
    id: int
    status: str
    marked_by: str

    model_config = {
        "from_attributes": True
    }