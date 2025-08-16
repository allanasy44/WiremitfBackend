# Use slim Python base
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Collect static files into /app/staticfiles
RUN python manage.py collectstatic --noinput || true

# Default (overridden by docker-compose)
CMD ["gunicorn", "wiremit_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
