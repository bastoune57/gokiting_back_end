# Dockerfile

# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Copy project
#COPY . /code/
ADD . /code

# upgrade pip
RUN python3 -m pip install --upgrade pip

# Install dependencies
RUN pip install -r /code/requirements.txt
