from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from jose import JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Password hashing context used to hash and verify user passwords.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# JWT signing settings used when access tokens are created and verified.
# Secret key used for JWT token signing
SECRET_KEY = os.getenv("SECRET_KEY")

# JWT encryption algorithm
ALGORITHM = os.getenv("ALGORITHM")

# Token expiration duration loaded from environment
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

# Convert a plain password into a secure hash before saving it.
def hash_password(password: str):
    return pwd_context.hash(password)


# Extract bearer tokens from requests that use the /login token endpoint.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# Compare a plain password with the stored password hash.
def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
    

# Create a signed JWT containing user data and an expiration time.
def create_access_token(data: dict):
    # Copy the payload so the caller's original dictionary is not modified.
    to_encode = data.copy()

    # Add an expiration time so tokens stop working after the configured window.
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


# Decode and validate an access token, then return the authenticated user data.
def verify_access_token(token: str):
    try:
        # Decode the token and validate its signature and expiration time.
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        role = payload.get("role")

        # The subject claim identifies the logged-in user.
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


# FastAPI dependency that returns the currently authenticated user.
def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    return verify_access_token(token)


# FastAPI dependency that allows only admin users to access a route.
def admin_only(
    current_user: dict = Depends(get_current_user)
):
    # Protected admin routes call this dependency before the route function runs.
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user
