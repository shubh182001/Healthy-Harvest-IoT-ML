#include <dht.h>        // Include library
#define outPin A0        // Defines pin number to which the sensor is connected
const int sensor_pin = A1;

const int threshold = 20;
int pH_Value;
float Voltage;

dht DHT;                // Creates a DHT object

void setup() {
  Serial.begin(9600);
  pinMode(pH_Value, INPUT);
}

void loop() {
  // dht11 code start
  int readData = DHT.read11(outPin);

  float t = DHT.temperature;        // Read temperature
  float h = DHT.humidity;           // Read humidity

//  Serial.print("Temperature = ");
//  Serial.print(t);
//  Serial.print("°C | ");
//  Serial.print((t * 9.0) / 5.0 + 32.0);  // Convert celsius to fahrenheit
//  Serial.println("°F ");
//  Serial.print("Humidity = ");
//  Serial.print(h);
//  Serial.println("% ");
//  Serial.println("");

  String tempval = String(t);
  String humidval = String(h);

  

  // delay(2000); // wait two seconds

  // Soil moisture sensor starts:

  float moisture_percentage;
  int sensor_analog;
  sensor_analog = analogRead(sensor_pin);
  moisture_percentage = ( 100 - ( (sensor_analog / 1023.00) * 100 ) );
//   Serial.print("Moisture Percentage = ");
//   Serial.print(moisture_percentage);
//   Serial.print("%\n\n");
//   Serial.print("Sensor value = ");
//   Serial.print(sensor_analog);

   String moistval = String(sensor_analog);


  //  ph sensor
  pH_Value = analogRead(A2);
  Voltage = pH_Value * (5.0 / 1023.0);
  // Serial.println(Voltage);

  String phval = String(pH_Value);

  String FinalVal = tempval+","+humidval+","+moistval+","+Voltage+",";
  Serial.println(FinalVal);

  delay(1000);
}