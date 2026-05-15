from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password
from app.schemas.user_schema import UserLogin
from app.core.security import (
    verify_password,
    create_access_token
)
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


# Register a new user and store the password as a hash.
# This creates the account that can later receive a JWT from /login.
@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # Hash the raw password before storing the user record.
    hashed_pw = hash_password(user.password)

    # Build the user model with the hashed password and selected role.
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )

    # Save the user to the database.
    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }
    

# Authenticate a user and return a bearer token for protected routes.
# OAuth2PasswordRequestForm sends the email value in form_data.username.
@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Find the user by email before checking the submitted password.
    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    # Use the same generic error so attackers cannot tell which field failed.
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify the submitted password against the stored password hash.
    valid_password = verify_password(
        form_data.password,
        existing_user.hashed_password
    )

    # Use the same generic error when the password check fails.
    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Store the user's email and role inside the token payload.
    access_token = create_access_token(
        data={
            "sub": existing_user.email,
            "role": existing_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
