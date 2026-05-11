from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from jose import JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    return pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
    
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        role = payload.get("role")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return {
            "email": email,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid or expired"
        )

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    return verify_access_token(token)

def admin_only(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user