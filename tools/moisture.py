from langchain_core.tools import tool
from influxdb import InfluxDBClient
import datetime
import influxdb_client
from dotenv import load_dotenv
load_dotenv(override=True)
import os

# Define parameters
now = datetime.datetime.now()  
influxdb_host = os.getenv('INFLUXDB_HOST')
token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
url = os.environ.get("INFLUXDB_HOST")
influx_bucket=os.environ.get("INFLUXDB_BUCKET")
measurement='humidity of the soil'
field='moistures'

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# Function to read data from InfluxDB
def read_sensor_data(client, org, measurement):

    query = f"""from(bucket: "{org}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "{measurement}")"""

    query_api = client.query_api()
    tables = query_api.query(query, org="home")

    results = []
    for table in tables:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    return results[-3:]

@tool
def moisture(command: str) -> str:
    """
    Useful tool to get the moisture of the soil
    """
    points=read_sensor_data(client, org, measurement)
    return points
    
    
    