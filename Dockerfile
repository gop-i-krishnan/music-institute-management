# Use lightweight official Python image.
FROM python:3.10-slim

# Set working directory inside container.
WORKDIR /app

# Copy dependency file first for Docker layer caching.
COPY requirements.txt .

# Install all project dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy full backend source code into container.
COPY . .

# Expose FastAPI application port.
EXPOSE 8000

# Start FastAPI server inside container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]