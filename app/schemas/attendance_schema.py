from pydantic import BaseModel


# Request body used when an admin marks attendance for a student.
class AttendanceCreate(BaseModel):
    student_id: int
    status: str


# Response model returned when attendance records are read from the database.
class AttendanceResponse(BaseModel):
    id: int
    status: str
    marked_by: str

    # Allows Pydantic to read values directly from SQLAlchemy model objects.
    model_config = {
        "from_attributes": True
    }
