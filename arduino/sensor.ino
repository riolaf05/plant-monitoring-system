#include <SPI.h>
#include <Ethernet.h>
#include <DHT.h>
#include <ArduinoHttpClient.h>

// Define pins for sensors
#define DHTPIN 2
#define DHTTYPE DHT11
#define MOISTUREPIN A0

// Initialize the DHT sensor
DHT dht(DHTPIN, DHTTYPE);

// Network settings
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
char serverAddress[] = "your_influxdb_host";  // Replace with your InfluxDB host
int port = 8086;
char influxDbDatabase[] = "sensors";  // Replace with your InfluxDB database name
char influxDbUser[] = "user";  // Replace with your InfluxDB username
char influxDbPassword[] = "password";  // Replace with your InfluxDB password

// Create an Ethernet client
EthernetClient ethClient;
HttpClient httpClient = HttpClient(ethClient, serverAddress, port);

void setup() {
  // Start the Ethernet connection
  Ethernet.begin(mac);
  Serial.begin(9600);
  while (Ethernet.localIP() == INADDR_NONE) {
    Serial.println("Failed to configure Ethernet using DHCP");
    delay(1000);
  }
  
  // Initialize the DHT sensor
  dht.begin();
  
  Serial.println("Ethernet and sensor initialization complete");
}

void loop() {
  // Read sensor values
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  int moisture = analogRead(MOISTUREPIN);

  // Check if any reads failed and exit early
  if (isnan(humidity) || isnan(temperature) || moisture == 0) {
    Serial.println("Failed to read from sensors");
    return;
  }

  // Prepare data in InfluxDB line protocol format
  String data = "environment";
  data += ",location=arduino";
  data += " temperature=" + String(temperature) + ",";
  data += "humidity=" + String(humidity) + ",";
  data += "moisture=" + String(moisture);

  // Print the data (for debugging)
  Serial.println("Data to send: " + data);

  // Send data to InfluxDB
  httpClient.beginRequest();
  httpClient.post("/write?db=" + String(influxDbDatabase) + "&u=" + String(influxDbUser) + "&p=" + String(influxDbPassword));
  httpClient.sendHeader("Content-Type", "text/plain");
  httpClient.sendHeader("Content-Length", data.length());
  httpClient.beginBody();
  httpClient.print(data);
  httpClient.endRequest();

  // Check the response from the server
  int statusCode = httpClient.responseStatusCode();
  String response = httpClient.responseBody();
  Serial.println("Status code: " + String(statusCode));
  Serial.println("Response: " + response);

  // Wait for a minute before the next reading
  delay(60000);
}
