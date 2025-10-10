# syntax=docker/dockerfile:1
#use official python base image
FROM python:3.10

# Set environment viriables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set working directory inside container
WORKDIR /app

# Compy requiments file to container
COPY requirements.txt /app/

# install dependencies
RUN pip install -r requirements.txt
RUN pip install --upgrade pip

#Copy the remaining of the application into the work directory
COPY . /app/

# Expose the port Django run on
EXPOSE 8000

# Runtime: docker run -p 8000:8000

# Command to run Django developement server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
