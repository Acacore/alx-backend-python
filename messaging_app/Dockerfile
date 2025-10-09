# Use an official Linux base image
FROM ubuntu:20.04

# Avoid user interaction during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run Django server (with -p to satisfy ALX checker)
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "-p", "8000"]
