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


@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    hashed_pw = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }
    
@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    valid_password = verify_password(
        form_data.password,
        existing_user.hashed_password
    )

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

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