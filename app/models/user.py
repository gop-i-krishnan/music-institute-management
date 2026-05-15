from sqlalchemy import Column, Integer, String
from app.database import Base


# SQLAlchemy model for application users.
# Users authenticate through /login and receive role-based access.
class User(Base):
    __tablename__ = "users"

    # Primary key for the users table.
    id = Column(Integer, primary_key=True, index=True)

    # Display name for the user account.
    name = Column(String)

    # Email is unique because it is used as the login identifier.
    email = Column(String, unique=True, index=True)

    # Passwords are stored as hashes, never as plain text.
    hashed_password = Column(String)

    # Role controls route permissions, for example admin access.
    role = Column(String)
