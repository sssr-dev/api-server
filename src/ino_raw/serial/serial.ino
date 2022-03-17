#include "ArduinoCLI/cli.h"

int LED = 13;

void setup() {

  Serial.begin(9600);
  pinMode(LED, OUTPUT);

  ArduinoCLI()::start(); 

}

void loop() {

  println("sos");
  sos();
      
}
