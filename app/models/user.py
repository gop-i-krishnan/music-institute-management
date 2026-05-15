from sqlalchemy import Column, Integer, String
from app.database import Base


# SQLAlchemy model for application users.
class User(Base):
    __tablename__ = "users"

    # Basic user account fields.
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    email = Column(String, unique=True, index=True)

    # Passwords are stored as hashes, never as plain text.
    hashed_password = Column(String)

    # Role controls route permissions, for example admin access.
    role = Column(String)
