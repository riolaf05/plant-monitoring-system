from langchain_core.tools import tool
import datetime

# Function to read data from InfluxDB
def read_sensor_data(client, database, measurement, fields):
    client.switch_database(database)
    query = f'SELECT {", ".join(fields)} FROM {measurement} ORDER BY time DESC LIMIT 1'
    result = client.query(query)
    points = list(result.get_points())
    if points:
        return points[0]
    return None

@tool
def watering(command: str) -> str:
    """
    Used to send commamd1 to the watering system.
    """
    return "Command sent to the watering system."
    
    
    