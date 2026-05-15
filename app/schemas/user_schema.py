from pydantic import BaseModel


# Request body used when registering a new user.
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str
    

# Request body shape for email and password login data.
class UserLogin(BaseModel):
    email: str
    password: str
