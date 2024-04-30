# Use an official Python runtime as a parent image
FROM python:3.9-slim-bookworm

# Set the working directory to /app
WORKDIR /app

# Update, upgrade system packages, and clean up in a single layer
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY runtime_requirements.txt .

# Upgrade pip and install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r runtime_requirements.txt

# Copy the current directory contents into the container at /app
COPY on_call_rotation.py .

# Run as non-root user
RUN useradd -m --uid 1001 myuser
USER 1001

# Run app.py when the container launches
CMD ["python", "on_call_rotation.py"]