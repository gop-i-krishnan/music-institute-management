from pydantic import BaseModel


# Request body used when registering a new user.
# The password is accepted here but stored only after hashing.
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str
    

# Request body shape for email and password login data.
# The current /login route uses OAuth2PasswordRequestForm instead of this schema.
class UserLogin(BaseModel):
    email: str
    password: str
