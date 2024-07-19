from picamera2 import Picamera2
from influxdb import InfluxDBClient
import base64
import openai
import datetime

#Functions for image understranding
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def image_summarize(img_base64,prompt):
    ''' 
    Image summary
    Takes in a base64 encoded image and prompt (requesting an image summary)
    Returns a response from the LLM (image summary) 
    '''
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_base64}",
                },
                },
            ],
            }
        ],
        max_tokens=150,
    )
    content = response.choices[0].message.content
    return content

# Function to capture an image using Picamera2
def capture_image(image_path):
    picam2 = Picamera2()
    picam2.start_and_capture_file(image_path)
    picam2.close()

# Function to read data from InfluxDB
def read_sensor_data(client, database, measurement, fields):
    client.switch_database(database)
    query = f'SELECT {", ".join(fields)} FROM {measurement} ORDER BY time DESC LIMIT 1'
    result = client.query(query)
    points = list(result.get_points())
    if points:
        return points[0]
    return None

# Main function to create the prompt
def create_prompt(image_path, sensor_data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prompt = (
        f"Image captured at {timestamp}: {image_path}\n"
        f"Temperature: {sensor_data['temperature']} °C\n"
        f"Moisture: {sensor_data['moisture']} %\n"
        f"Humidity: {sensor_data['humidity']} %\n"
    )
    return prompt

# Define parameters
image_path = "Desktop/new_image.jpg"
influxdb_host = 'localhost'
influxdb_port = 8086
influxdb_user = 'user'
influxdb_password = 'password'
influxdb_database = 'sensors'
influxdb_measurement = 'environment'
influxdb_fields = ['temperature', 'moisture', 'humidity']

# Capture the image
capture_image(image_path)

# Connect to InfluxDB and read sensor data
client = InfluxDBClient(host=influxdb_host, port=influxdb_port, username=influxdb_user, password=influxdb_password)
sensor_data = read_sensor_data(client, influxdb_database, influxdb_measurement, influxdb_fields)

# Create the prompt for the LLM
if sensor_data:
    prompt = create_prompt(image_path, sensor_data)
    print(prompt)
else:
    print("No sensor data available")

#send the prompt and the image to the LLM
img_base64 = encode_image(image_path)
response = image_summarize(img_base64, prompt)

#send the response to the 2nd LLM with output parser
#TODO