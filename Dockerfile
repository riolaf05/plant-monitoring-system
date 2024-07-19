# Use the balenalib base image for Raspberry Pi 4 (ARM architecture)
FROM balenalib/raspberrypi4-64-python:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libopenjp2-7 \
    libtiff5 \
    libatlas-base-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables for InfluxDB
ENV INFLUXDB_HOST=localhost
ENV INFLUXDB_PORT=8086
ENV INFLUXDB
