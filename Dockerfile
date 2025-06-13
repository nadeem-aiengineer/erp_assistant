# Use official Python 3.12.3 base image
FROM python:3.12.3-slim

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libmagic1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first and install them
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Copy app code
COPY . .

# Set virtual environment path
ENV PATH="/opt/venv/bin:$PATH"

# Expose Flask port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
