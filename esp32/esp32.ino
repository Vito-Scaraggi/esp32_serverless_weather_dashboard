//here certificates and Wifi password are defined
#include "secrets.h"

//libraries
#include <WiFiClientSecure.h>
#include <MQTTClient.h>
#include <ArduinoJson.h>
#include "WiFi.h"
#include "DHT.h"
#include <analogWrite.h>
#include <EEPROM.h>

//pin numbers
#define PHOTO_PIN "<pin number here>"
#define DHT_PIN "<pin number here>"
#define RGB_RED "<pin number here>"
#define RGB_GREEN "<pin number here>"
#define RGB_BLUE "<pin number here>"

// The MQTT topics that this device should publish/subscribe
#define AWS_IOT_PUBLISH_TOPIC   "esp32/pub"
#define AWS_IOT_SUBSCRIBE_TOPIC "esp32/sub"

//useful constants
#define DHT_TYPE DHT11
#define FAIL -1000.0
#define EEPROM_SIZE 2
#define LED_BRIGHTNESS 32
#define BLINK_TIME 100
#define ULONG_MAX 4294967295
#define CONNECT_ATTEMPTS 6
#define PING_TIME 20
enum STATE{ RED, YELLOW, GREEN, BLUE, WHITE};

//global variables
unsigned short sleep_mins;
unsigned long previous_data;
unsigned long previous_ping;
WiFiClientSecure net = WiFiClientSecure();
MQTTClient client = MQTTClient(256);
DHT dht(DHT_PIN, DHT_TYPE);

//write analog signals on RGB led pins
void RGB(int r, int g, int b){
  analogWrite(RGB_RED, r);
  analogWrite(RGB_GREEN, g);
  analogWrite(RGB_BLUE, b);
}

//change RGB led color
void changeState(STATE state){
    switch(state){
      case RED:
           RGB(LED_BRIGHTNESS,0,0);
      break;
      case YELLOW:
           RGB(LED_BRIGHTNESS,LED_BRIGHTNESS,0);
      break;
      case GREEN:
          RGB(0,LED_BRIGHTNESS,0);
      break;
      case BLUE:
          RGB(0,0,LED_BRIGHTNESS);
      break;
      case WHITE:
          RGB(LED_BRIGHTNESS, LED_BRIGHTNESS, LED_BRIGHTNESS);
      break;
    }
}

//read temperature
float readTemp(){
  float t = dht.readTemperature();
  if(isnan(t))
      return FAIL;
  return t;
}

//read humidity
float readHumid(){
  float h = dht.readHumidity();
  if(isnan(h))
      return FAIL;
  return h;
}

//read brightness
int readLum(){
  return analogRead(PHOTO_PIN);
}

//decide if it's time to perform an action
bool itsTime(unsigned long sleep_seconds, unsigned long previous_millis){
  return (millis() - previous_millis + ULONG_MAX) % ULONG_MAX  >= sleep_seconds * 1000;
}

//connects to wifi
void connectWIFI(){
  
  if(WiFi.status() != WL_CONNECTED){
    
    changeState(RED);

    int n = sizeof(WIFI_SSID) / sizeof(WIFI_SSID[0]);

    for(int i=0; i<n; i++){
      
      Serial.print("Trying ");
      Serial.println(WIFI_SSID[i]);    
      
      WiFi.begin(WIFI_SSID[i], WIFI_PASSWORD[i]);

      for(int j=0; j < CONNECT_ATTEMPTS && WiFi.status() != WL_CONNECTED; j++){
        delay(500);
        Serial.print(".");
      }

      if(WiFi.status() == WL_CONNECTED){
        changeState(YELLOW);
        return;
      }
    }

  }
  
}

//connects to AWS
void connectAWS(){
  
  if(WiFi.status() == WL_CONNECTED && !client.connected()){
    
    changeState(YELLOW);
    
    // Connect to the MQTT broker on the AWS endpoint we defined earlier
    client.begin(AWS_IOT_ENDPOINT, 8883, net);
  
    Serial.print("Connecting to AWS IOT");

    for(int i=0; i < CONNECT_ATTEMPTS && !client.connect(THING_NAME); i++){
      Serial.print(".");
      delay(500);
    }
  
    if(client.connected()){
      // Subscribe to a topic
      client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC); 
      Serial.println("AWS IoT Connected!");
      changeState(GREEN);
    }
    
  }
  
}

//publishes message to esp32/pub MQTT topic
void publishMessage(){
  
  if( itsTime(sleep_mins * 60, previous_data) && client.connected()){
    Serial.println("it's time");
    StaticJsonDocument<200> doc;
    JsonObject weather = doc.createNestedObject("weather");
    JsonObject info = doc.createNestedObject("info");
    char jsonBuffer[512];
    float t = readTemp();
    float h = readHumid();
    doc["type"] = "data";
    if(t != FAIL)
      weather["temp"] = t;
    else
      weather["temp"] = "Fail to read";
    
    if(h != FAIL)
      weather["humid"] = h;
    else
      weather["humid"] = "Fail to read";
      
    weather["lum"] = readLum();
    
    info["rate"] = int (sleep_mins);
    serializeJson(doc, jsonBuffer);

    if(client.connected()){
      client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);
      changeState(BLUE);
      previous_data = millis();
      changeState(GREEN);
    }
    else
      Serial.println("but i've lost connection");
    
  }
}


//handles messages received on esp32/sub MQTT topic
void messageHandler(String &topic, String &payload) {
  changeState(WHITE);
  Serial.println("incoming: " + topic + " - " + payload);
  StaticJsonDocument<200> doc;
  deserializeJson(doc, payload);
  sleep_mins = (unsigned short) doc["rate"];
  Serial.println(sleep_mins);
  EEPROM.write(0, sleep_mins);
  EEPROM.commit();

  StaticJsonDocument<200> ack;
  ack["type"] = "ack";
  ack["rate"] = sleep_mins;
  char ackBuffer[512];
  serializeJson(ack, ackBuffer);
  client.publish(AWS_IOT_PUBLISH_TOPIC, ackBuffer);
  changeState(GREEN);
}

//setup
void setup() {
  pinMode(RGB_RED,OUTPUT);
  pinMode(RGB_GREEN,OUTPUT);
  pinMode(RGB_BLUE,OUTPUT);
  dht.begin();
  Serial.begin(9600);
  EEPROM.begin(EEPROM_SIZE);
  WiFi.mode(WIFI_STA);
  // Create a message handler
  client.onMessage(messageHandler);
  // Configure WiFiClientSecure to use the AWS IoT device credentials
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);
  sleep_mins = EEPROM.read(0);
  previous_data = 0;
  previous_ping = 0;
}

//main loop
void loop() {
  connectWIFI();
  connectAWS();
  publishMessage();
  client.loop();
}