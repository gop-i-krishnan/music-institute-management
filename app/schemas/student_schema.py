from pydantic import BaseModel


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