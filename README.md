# Smart Guardian System Setup

This guide provides step-by-step instructions to set up the Smart Guardian system, which involves capturing images using a Raspberry Pi, reading sensor data using an Arduino, and logging the data to an InfluxDB database.

## Table of Contents
1. [Raspberry Pi Setup](#raspberry-pi-setup)
2. [InfluxDB Configuration](#influxdb-configuration)
3. [Building and Running the Docker Container](#building-and-running-the-docker-container)
4. [Arduino Setup](#arduino-setup)
5. [Hardware Setup](#hardware-setup)
6. [Setting a Fixed IP Address for Raspberry Pi](#setting-a-fixed-ip-address-for-raspberry-pi)

## Raspberry Pi Setup

1. **Create a directory for InfluxDB data:**
    ```sh
    mkdir -p /home/pi/influxdb/data
    ```

2. **Generate the InfluxDB configuration file:**
    ```sh
    docker run --rm influxdb:2.0 influxd print-config > /home/pi/influxdb/config.yml
    ```

3. **Create a `docker-compose.yml` file:**
    ```yaml
    version: '3.1'

    services:
      influxdb:
        image: influxdb:2.0
        container_name: influxdb
        ports:
          - "8086:8086"
        volumes:
          - /home/pi/influxdb/data:/var/lib/influxdb2
          - /home/pi/influxdb/config.yml:/etc/influxdb2/influxdb2.conf
    ```

4. **Start the InfluxDB container:**
    ```sh
    docker compose up -d influxdb
    ```

## InfluxDB Configuration

1. **Access the InfluxDB web interface:**
    - Open a browser and navigate to: `http://<rpi-url>:8086`

2. **Set up InfluxDB:**
    - Follow the on-screen instructions to set up the InfluxDB instance, create an initial user, and set up the database.

## Building and Running the Docker Container (Smart Guardian)

1. **Create a `requirements.txt` file:**
    ```txt
    picamera2
    influxdb
    requests
    openai
    langchain
    ```

2. **Create a Dockerfile:**
    ```Dockerfile
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
    ENV INFLUXDB_USER=user
    ENV INFLUXDB_PASSWORD=password
    ENV INFLUXDB_DATABASE=sensors
    ENV INFLUXDB_MEASUREMENT=environment

    # Run the script
    CMD ["python", "your_script.py"]
    ```

3. **Build and run the Docker container:**
    ```sh
    docker build -t smart_guardian .
    docker run --privileged -e INFLUXDB_HOST=<your_host> -e INFLUXDB_PORT=<your_port> -e INFLUXDB_USER=<your_user> -e INFLUXDB_PASSWORD=<your_password> -e INFLUXDB_DATABASE=<your_database> -e INFLUXDB_MEASUREMENT=<your_measurement> smart_guardian
    ```

## Arduino Setup

1. **Install required libraries:**
    - DHT sensor library: [DHT library](https://github.com/adafruit/DHT-sensor-library)
    - Ethernet library (included with the Arduino IDE)
    - HTTP client library: [ArduinoHttpClient](https://github.com/arduino-libraries/ArduinoHttpClient)

2. **Upload the Arduino script**

## Hardware Setup

1. **Connect the sensors to the Arduino:**
    - **DHT11 Sensor:**
        - VCC to 5V
        - GND to GND
        - Data pin to digital pin 2
    - **Moisture Sensor:**
        - VCC to 5V
        - GND to GND
        - Analog output to analog pin A0

2. **Connect the Arduino to the Ethernet shield/module.**

3. **Ensure the Raspberry Pi and Arduino are on the same network.**

## Setting a Fixed IP Address for Raspberry Pi

1. **Edit the `dhcpcd.conf` file:**
    ```sh
    sudo nano /etc/dhcpcd.conf
    ```

2. **Add the following lines at the end of the file:**
    ```sh
    interface eth0
    static ip_address=192.168.1.100/24
    static routers=192.168.1.1
    static domain_name_servers=192.168.1.1
    ```

    Replace `192.168.1.100` with the desired IP address for your Raspberry Pi and `192.168.1.1` with your router’s IP address.

3. **Restart the DHCP service:**
    ```sh
    sudo systemctl restart dhcpcd
    ```

4. **Reboot the Raspberry Pi:**
    ```sh
    sudo reboot
    ```

After following these steps, your Smart Guardian system should be set up and running, with sensor data being captured and stored in InfluxDB, ready for further analysis or monitoring.
