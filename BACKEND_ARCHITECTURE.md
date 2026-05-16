# Music Institute Management Backend

A production-style backend system built using FastAPI,
PostgreSQL, SQLAlchemy, JWT authentication,
Alembic migrations, and layered backend architecture.

Core features include:
- Authentication and authorization
- Student management system
- Attendance tracking
- Filtering/search/pagination
- Validation and error handling
- Logging and transaction safety

# Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM |
| Pydantic | Validation and schemas |
| Alembic | Database migrations |
| JWT | Authentication |
| Passlib | Password hashing |
| python-dotenv | Environment configuration |

# Folder Structure

app/
│
├── core/
│   ├── security.py
│   ├── exceptions.py
│   ├── logger.py
│
├── models/
│   ├── user.py
│   ├── student.py
│   ├── attendance.py
│
├── routes/
│   ├── auth_routes.py
│   ├── student_routes.py
│   ├── attendance_routes.py
│
├── schemas/
│   ├── common_schema.py
│   ├── user_schema.py
│   ├── student_schema.py
│   ├── attendance_schema.py
│
├── services/
│   ├── attendance_service.py
│
├── database.py
├── main.py

# Database Relationships

Student
   ↓ one-to-many
Attendance

One student can have multiple attendance records.
Attendance rows reference students through a foreign key.

# JWT Authentication Flow

1. User registers with email/password
2. Password is hashed using Passlib
3. User logs in
4. JWT token is generated
5. Frontend sends token in Authorization header
6. Backend verifies token
7. Role-based access is enforced

# Student Features

- Create student
- Update student
- Delete student
- Get single student
- Filter students
- Search students
- Sort students
- Pagination system

# Attendance Features

- Mark attendance
- Retrieve attendance history

# Security Features

- JWT authentication
- Role-based authorization
- Password hashing

# Standard API Response Structure

All APIs follow a consistent response contract:

{
  "success": true,
  "message": "...",
  "data": ...,
  "meta": ...
}

# Validation System

Pydantic schemas validate:
- email format
- minimum field lengths
- request body structure

Global exception handlers return
consistent validation responses.

# Database Safety Features

- IntegrityError handling
- Transaction rollback
- Duplicate email protection
- Alembic migration system


# Logging System

Application logs:
- student creation
- updates
- deletions
- duplicate email attempts
- attendance operations

Logs are written into app.log
for debugging and monitoring.

# Future Improvements

- Middleware architecture
- Async database support
- Rate limiting
- Docker deployment
- Redis caching
- Automated testing
- CI/CD pipeline