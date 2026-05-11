from fastapi import FastAPI

from app.database import engine, Base
from app.models.student import Student
from app.routes.student_routes import router as student_router

from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(student_router)


@app.get("/")
def home():
    return {"message": "Music Institute Backend Running"}