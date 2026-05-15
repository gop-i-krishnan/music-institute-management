from pydantic import BaseModel


# Request body used when an admin marks attendance for a student.
# The route uses student_id to connect the attendance row to a student.
class AttendanceCreate(BaseModel):
    student_id: int
    status: str


# Response model returned when attendance records are read from the database.
# This hides internal fields that should not be part of the API response.
class AttendanceResponse(BaseModel):
    id: int
    status: str
    marked_by: str

    # Allows Pydantic to read values directly from SQLAlchemy model objects.
    model_config = {
        "from_attributes": True
    }
