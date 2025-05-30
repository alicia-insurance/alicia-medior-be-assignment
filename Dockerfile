# Use the official Python slim image
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y curl gcc libpq-dev

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY src/new_requirements.txt .
RUN uv pip install --no-cache-dir -r new_requirements.txt --system

# Copy the rest of the project
COPY src/ .

# Collect static files and create logs directory
RUN mkdir -p logs && python manage.py collectstatic --noinput

# RUN python manage.py makemigrations && python manage.py migrate

# Expose port
EXPOSE 8000

# Run server with Gunicorn
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=3"]
