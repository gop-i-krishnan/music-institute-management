from fastapi import FastAPI

from app.database import engine, Base
from app.models.student import Student
from app.routes.student_routes import router as student_router

from app.models.user import User
from app.routes.auth_routes import router as auth_router

from app.models.attendance import Attendance
from app.routes.attendance_routes import (
    router as attendance_router
)

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler
)
from app.core.middleware import (
    LoggingMiddleware
)

# Create database tables for all imported SQLAlchemy models.
# In production, Alembic migrations are usually preferred for schema changes.
Base.metadata.create_all(bind=engine)

# FastAPI application instance.
app = FastAPI()

# Register request logging middleware.
app.add_middleware(LoggingMiddleware)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

# Register all route groups with the application.
app.include_router(student_router)
app.include_router(auth_router)
app.include_router(attendance_router)


# Simple health-check route for confirming the backend is running.
@app.get("/")
def home():
    return {"message": "Music Institute Backend Running"}
