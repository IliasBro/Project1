# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set a working directory in the container
WORKDIR /app

# Install system dependencies if needed (e.g., build-essential, gcc) 
# (Optional: Uncomment if necessary)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Copy requirements.txt first (for better Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your application code into the container.
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5001

# Set the environment variable for Flask (optional)
ENV FLASK_APP backend/app.py

# Command to run your app using Flask's built-in server
CMD ["python", "backend/app.py"]
