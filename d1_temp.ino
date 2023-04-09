#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP8266WiFi.h>
#include <WiFiManager.h> // https://github.com/tzapu/WiFiManager

// Data wire is connected to D5
#define ONE_WIRE_BUS D5


// WiFi settings
const char* ssid = "";
const char* password = "";
const char* server = "VPSServerAddress";
const int port = 8888;
const String secret_key = "supersecret"; // match with key in server.py
WiFiManger wifimanager;

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);


// Pass oneWire reference to DallasTemperature library
DallasTemperature sensors(&oneWire);


void setup() {
  Serial.begin(9600);
  wifiManager.autoConnect();
  // Connect to WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");
  // Initialize the DS18B20 sensor
  sensors.begin();
}


void loop() {
  // Request temperature readings from all DS18B20 sensors on the bus
  sensors.requestTemperatures();
  // Get the temperature value from the DS18B20 sensor on D5
  float temperature = sensors.getTempCByIndex(0);
  // Get the username value
  String username = "NameOfSensor-Location";
  // Create the TCP socket and connect to the server
  WiFiClient client;
  if (!client.connect(server, port)) {
    Serial.println("Failed to connect to server");
    return;
  }
  // Send the temperature and username data to the server
  String data = secret_key + "," + username + "," + String(temperature);
  client.print(data);
  // Close the TCP socket
  client.stop();
  Serial.println(temperature);
  ESP.deepSleep(295e6); //Deepsleep for 4min55sec, allow some time to connect to wifi before performing task
}
