/*******************************************************************************
                              Includes
*******************************************************************************/
#include <Arduino.h>
#ifdef ESP8266
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <string.h>
#include <Espalexa.h>
#include <WiFiClientSecure.h>
#include <string.h>
#else
#include <WiFi.h>
#endif
/*******************************************************************************
                              defines
*******************************************************************************/
#define ESPALEXA_DEBUG
#define ESPALEXA_MAXDEVICES   5
#define APPLIANCE_LED          4          // GPIO 4 (On board: D2)
#define CENTRAL_APPLIANCE_LED  5          // GPIO 5 (On board: D1) 
#define MSG_BUFFER_SIZE       (50)
/*******************************************************************************
                             Global Variables
*******************************************************************************/
void LightOne(EspalexaDevice* dev);
void LightTwo(EspalexaDevice* dev);
WiFiClient espClient;
PubSubClient client(espClient);
WiFiClientSecure net_ssl;
EspalexaDevice* Device1;
EspalexaDevice* Device2;
Espalexa espalexa;
bool interruptflag = true;
const char* ssid = "Gopalmath";
const char* password = "Skrillex@123";
//const char* ssid = "dlink-2C2C";
//const char* password = "hxjmi80946";
const char* mqtt_server = "192.168.0.111";
unsigned long lastMsg = 0;
char msg[MSG_BUFFER_SIZE];
int value = 0;
int i = 0;

/*******************************************************************************
  Function    : setup
  Description : This function will Initialize the MQTT server, Connect ESP8266
                to Internet(via WiFi). Also, Initialize Alexa with ESP
  Input       : NA
  Output      : NA
  Return      : NA
*******************************************************************************/
void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);              // Initialize the LED_BUILTIN pin as an output
  pinMode(APPLIANCE_LED, OUTPUT);             // Initialize the APPLIANCE_LED pin as an output
  pinMode(CENTRAL_APPLIANCE_LED, OUTPUT);     // Initialize the CENTRAL_APPLIANCE_LED pin as an output
  pinMode(14, INPUT_PULLUP);
  Serial.begin(115200);                      // Set Baud Rate to 115200
  Serial.println('\n');
  WiFi.begin(ssid, password);                // Connect ESP8266 to WiFi using ssid and password
  Serial.println("Connecting.....");         // Print "Connecting....." on Serial Monitor
  client.setServer(mqtt_server, 1883);       // Set MQTT Server 
  client.setCallback(callback);              // Initialize callback func. of MQTT

  while (WiFi.status() != WL_CONNECTED )     // Check whether ESP8266 is connected to WiFi
  {
    delay(500);
    Serial.println("Not connected");
  }

  if (WiFi.status() == WL_CONNECTED)         // Once ESP8266 is connected to WiFi
  {
    Serial.println('\n');
    Serial.println("Connected to :- ");      // Print "Connected" to connected ssid on Serial Monitor
    delay(1000);
    Serial.println("IP address is:- ");      // Print "IP Address of ESP8266" on Serial Monitor
    Serial.println(WiFi.localIP());
    Serial.println(WiFi.macAddress());

    Serial.println("Let's add devices");

    // Add Device 1 setup
    Device1 = new EspalexaDevice("Light 1", LightOne, EspalexaDeviceType::onoff);
    espalexa.addDevice(Device1);

    // Add Device 2 setup
    Device2 = new EspalexaDevice("Light 2", LightTwo, EspalexaDeviceType::color);
    espalexa.addDevice(Device2);

    espalexa.begin();                         // Initialize ESP_ALEXA
    Serial.println("Device added");
  }
  else
  {
    Serial.println("outside");
  }
  Serial.flush();
  client.subscribe("lighting_control/central/appliance/Rpi"); // Subscribe to "lighting_control/central/Rpi"
  client.subscribe("lighting_control/central/lighting/PC");   // Subscribe to "lighting_control/central/PC" 
}

/*******************************************************************************
  Function    : loop
  Description : This function will execute the MQTT server and ESP_ALEXA
                indefinitely.
  Input       : NA
  Output      : NA
  Return      : NA
*******************************************************************************/
void loop()
{
  espalexa.loop();                                  // Execute Alexa loop
  if (!client.connected())                          // Reconnect the ESP8266 to MQTT server if not connected
  {
    reconnect();
  }
  client.loop();                                    // Execute MQTT Server to Publish/ Subscribe
}

/*******************************************************************************
  Function    : LightOne
  Description : This function will control APPLIANCE_LED (GPIO 4 (On board: D2))
                via Alexa's inputs.
  Input       : Alexa's Device1
  Output      : NA
  Return      : NA
*******************************************************************************/
void LightOne(EspalexaDevice* Device1)
{
  uint8_t LightOne_Status = Device1->getValue();              // Get Device1 value from Alexa and store in LightOne_Status
  Serial.println();
  Serial.print("LightOne_Status_Alexa_Input: ");
  Serial.print(LightOne_Status);                              // Print LightOne_Status on serial monitor
  if (Device1 == nullptr)                                     // If NULL (nothing) is received from Alexa
  {
    return;                                                   // Exit the function
  }
  if (LightOne_Status)                                        // If ON is received from Alexa
  {
    digitalWrite(LED_BUILTIN, LOW);
    digitalWrite(APPLIANCE_LED, HIGH);                        // Turn the APPLIANCE_LED on
    snprintf (msg, MSG_BUFFER_SIZE, "ON");                    // Create "ON" message to be published
    Serial.println();
    Serial.print("Publish message: ");
    Serial.print(msg);                                        // Print the created message on serial monitor
    client.publish("lighting_control/central/appliance/esp8266", msg);  // Publish "ON" message through MQTT
  }
  else                                                        
  {
    digitalWrite(LED_BUILTIN, HIGH);
    digitalWrite(APPLIANCE_LED, LOW);                          // Turn the APPLIANCE_LED off
    snprintf (msg, MSG_BUFFER_SIZE, "OFF");                    // Create "OFF" message to be published
    Serial.println();
    Serial.print("Publish message: ");
    Serial.print(msg);                                         // Print the created message on serial monitor
    client.publish("lighting_control/central/appliance/esp8266", msg);  // Publish "OFF" message through MQTT
  }
}

/*******************************************************************************
  Function    : LightTwo
  Description : This function will control CENTRAL_APPLIANCE_LED (GPIO 5
                (On board: D1)) via Alexa's inputs.
  Input       : Alexa's Device2
  Output      : NA
  Return      : NA
*******************************************************************************/
void LightTwo(EspalexaDevice* Device2)
{
  uint8_t LightTwo_Status = Device2->getValue();              // Get Device2 value from Alexa and store in LightTwo_Status
  Serial.println();
  Serial.print("LightTwo_Status_Alexa_Input: ");
  Serial.print(LightTwo_Status);                              // Print LightTwo_Status on serial monitor
  if (Device2 == nullptr)                                     // If NULL (nothing) is received from Alexa
  {
    return;                                                   // Exit the function
  }
  if (LightTwo_Status)                                        // If ON is received from Alexa
  {
    snprintf (msg, MSG_BUFFER_SIZE, "AI");                    // Create "AI" message to be published
    Serial.println();
    Serial.print("Publish message: ");
    Serial.print(msg);                                        // Print the created message on serial monitor
    client.publish("lighting_control/central/lighting/esp8266", msg);  // Publish "AI" message through MQTT
  }
  else
  {
    digitalWrite(CENTRAL_APPLIANCE_LED, LOW);                 // Turn the CENTRAL_APPLIANCE_LED off
    digitalWrite(LED_BUILTIN, HIGH);                          // Turn the LED_BUILTIN off (active low)
    snprintf (msg, MSG_BUFFER_SIZE, "OFF");                   // Create "OFF" message to be published
    Serial.println();
    Serial.print("Publish message: ");
    Serial.print(msg);                                                 // Print the created message on serial monitor
    client.publish("lighting_control/central/lighting/esp8266", msg);  // Publish "OFF" message through MQTT
  }
}

/*******************************************************************************
  Function    : callback
  Description : This function controls APPLIANCE_LED after receving input through 
                MQTT server.
  Input       : MQTT: subscribed topic, payload from subscribed topic, length of
                payload 
  Output      : NA
  Return      : NA
*******************************************************************************/
void callback(char* topic, byte* payload, unsigned int length)
{
  if (strcmp(topic,"lighting_control/central/lighting/PC")==0)
  {
    Serial.println();
    Serial.print("Message arrived from PC");
    Serial.println();
    Serial.print("Topic: ");
    Serial.print(topic);
    String Light_Status_Received =  String((char*)payload );    // Get payload in LightOne_Status_Received
    
 
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, payload); // Get the JSON object
                                              
    if (error)                                                  // Test if parsing succeeds
    {
      Serial.println(F("deserializeJson() failed: "));
      Serial.print(error.c_str());                              // Print parsing error
    }
    
     
    for (int i = 0; i < length; i++)
    {
      String Light_Status_Received = doc["Central Lighting"];   // Store the string of JSON object(Central_light) sent via MQTT in LightOne_Status_Received
    }

    Serial.println();
    Serial.print("Light_Status_Received: ");
    Serial.print(Light_Status_Received);                        // Print the LightOne_Status_Received 
  
  
    if (Light_Status_Received[23] == 'n' || Light_Status_Received[23] == 'N' )  // Check whether string LightOne_Status_Received is ON(/On) or OFF(/Off)  
    {
      digitalWrite(CENTRAL_APPLIANCE_LED, HIGH);                         // Turn the CENTRAL_APPLIANCE_LED on if LightOne_Status_Received == ON/ On
      digitalWrite(LED_BUILTIN, LOW);
    }
    else
    {
      digitalWrite(CENTRAL_APPLIANCE_LED, LOW);                          // Turn the CENTRAL_APPLIANCE_LED off if LightOne_Status_Received == OFF/ Off
      digitalWrite(LED_BUILTIN, HIGH);
    }
  }
  else if (strcmp(topic,"lighting_control/central/appliance/Rpi")==0)
  {
    Serial.println();
    Serial.print("Message arrived from RPi");
    Serial.println();
    Serial.print("Topic: ");
    Serial.print(topic);
    String Appliance_Status_Received =  String((char*)payload ); // Get payload in LightOne_Status_Received
    
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, payload);  // Get the JSON object
                                              
    if (error)                                                   // Test if parsing succeeds
    {
      Serial.println(F("deserializeJson() failed: "));
      Serial.print(error.c_str());                               // Print parsing error
    }
    
     
    for (int i = 0; i < length; i++)
    {
      String Appliance_Status_Received = doc["Appliance"];       // Store the string of JSON object(Central_light) sent via MQTT in LightOne_Status_Received
    }

    Serial.println();
    Serial.print("Appliance_Status_Received: ");
    Serial.print(Appliance_Status_Received);                     // Print the LightOne_Status_Received 
  
  
    if (Appliance_Status_Received[16] == 'n' || Appliance_Status_Received[16] == 'N' )  // Check whether string LightOne_Status_Received is ON(/On) or OFF(/Off)  
    {
      digitalWrite(APPLIANCE_LED, HIGH);                          // Turn the APPLIANCE_LED on if LightOne_Status_Received == ON/ On
      digitalWrite(LED_BUILTIN, LOW);
    }
    else
    {
      digitalWrite(APPLIANCE_LED, LOW);                          // Turn the APPLIANCE_LED off if LightOne_Status_Received == OFF/ Off
      digitalWrite(LED_BUILTIN, HIGH);
    }
  }
  else
  {
    // Do Nothing
  }
}

/*******************************************************************************
  Function    : reconnect
  Description : This function reconnects the ESP8266 to MQTT server
  Input       : NA
  Output      : NA
  Return      : NA
*******************************************************************************/
void reconnect()
{
  while (!client.connected())                                 // Loop until ESP8266 is connected to MQTT server
  {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client-";                       // Create a random client ID
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str()))                     // Attempt to connect to MQTT server
    {
      Serial.println("Connected to MQTT Server");
      client.publish("lighting_control/central/lighting/esp8266", "Smart Central Lighting"); // Once connected, publish an announcement.
      client.subscribe("lighting_control/central/appliance/Rpi");       // Resubscribe to "lighting_control/central/Rpi"
      client.subscribe("lighting_control/central/lighting/PC"); // Subscribe to "lighting_control/central/Rpi"  
    }
    else
    {
      Serial.print("failed, rc=");                            // Failed to connect to MQTT server
      Serial.print(client.state());                           // Print "client state" on serial monitor
      Serial.println("Trying again in 5 seconds");              
      delay(5000);                                            // Wait 5 seconds before retrying
    }
  }
}

/******************************************************************************
                      End of File
******************************************************************************/
