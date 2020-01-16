
/**************************************************************************/
/*
This code was adapted from the example code for the Adafruit mcp9808
temperature sensor library.
Modified by: Justin Lawrence
Date Last Modified: 11/1/2020
*/
/**************************************************************************/

#include <Wire.h>
#include "Adafruit_MCP9808.h"

// Create the MCP9808 temperature sensor objects
Adafruit_MCP9808 tempsensors[3] = {Adafruit_MCP9808(),Adafruit_MCP9808(),Adafruit_MCP9808()};

void setup() {
  Serial.begin(9600);
  while (!Serial); //waits for serial terminal to be open
  
  // Make sure the sensor is found, you can also pass in a different i2c
  // address with tempsensor.begin(0x19) for example, also can be left in blank for default address use
  // Also there is a table with all addres possible for this sensor, you can connect multiple sensors
  // to the same i2c bus, just configure each sensor with a different address and define multiple objects for that
  //  A2 A1 A0 address
  //  0  0  0   0x18  this is the default address
  //  0  0  1   0x19
  //  0  1  0   0x1A
  //  0  1  1   0x1B
  //  1  0  0   0x1C
  //  1  0  1   0x1D
  //  1  1  0   0x1E
  //  1  1  1   0x1F

  // Initialize all sensors

  for (byte i{0}; i < 3; i++) {
    if(!tempsensors[i].begin(0x18+i)) { // Initializes sensors
      Serial.print("Sensor "); Serial.print(i + 1); Serial.println(" failed to initialize");
      while (true);
    }
    tempsensors[i].setResolution(3); // sets the resolution mode of reading, the modes are defined in the table bellow:
  }
  
  // Mode Resolution SampleTime
  //  0    0.5°C       30 ms
  //  1    0.25°C      65 ms
  //  2    0.125°C     130 ms
  //  3    0.0625°C    250 ms

  for (byte i{0}; i < 3; i++) {
    tempsensors[i].wake(); // Wake up all sensors
  }

  pinMode(5, INPUT);
  delay(10000);
}

void loop() {

  if (digitalRead(5) == LOW) {
    terminationSequence();
  }
  Serial.println(millis());
  for (byte i{0}; i < 3; i++) { // Read and write out temperatures
    float temp = tempsensors[i].readTempC();
    Serial.println(temp);
  }
  delay(30); // 30ms delay for the next reading
  
}

void terminationSequence() {
  while (digitalRead(5) == LOW); // Loop until you need to start recording again
}
