# Use a specific, stable Python image based on Debian Bullseye
FROM python:3.10-bullseye

# Set environment variables for non-buffered output and the port
ENV PYTHONUNBUFFERED True
ENV PORT 8080

# Clean apt cache and ensure complete Debian package sources are available
RUN apt-get clean && rm -rf /var/lib/apt/lists/* \
    && echo "deb http://deb.debian.org/debian bullseye main contrib non-free" > /etc/apt/sources.list \
    && echo "deb http://deb.debian.org/debian-security bullseye-security main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb http://deb.debian.org/debian bullseye-updates main contrib non-free" >> /etc/apt/sources.list

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Update package lists, install system dependencies, then install Python dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libgfortran5 \
    libopenblas-base \
    libopenblas-dev \
    liblapack3 \
    liblapack-dev \
    && pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# Copy your entire application code into the container
# Since api_server.py, Dockerfile, and requirements.txt are all in C:\Users\emada\Downloads\testproject,
# this will copy api_server.py to /app in the container.
COPY . .

# Command to run the application using uvicorn directly on the module
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
