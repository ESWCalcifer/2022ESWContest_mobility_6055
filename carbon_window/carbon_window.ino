/*  
  MQ7_Example.ino
  Example sketch for MQ7 carbon monoxide detector.
    - connect analog input 
    - set A_PIN to the relevant pin
    - connect device ground to GND pin 
    - device VC to 5.0 volts
  Created by Fergus Baker
  22 August 2020
  Released into the public domain.
*/


#include "MQ7.h"
#include <Stepper.h>

#define A_PIN 2
#define VOLTAGE 5



// init MQ7 device
MQ7 mq7(A_PIN, VOLTAGE);



const int stepsPerRevolution = 200; //회전수  1.8이니까
Stepper myStepper(stepsPerRevolution, 8,9,10,11);
const int gasPin = A2; 
int gas1=8;
//int gas2=400;
boolean window = false;   //false -> 닫혀있는상태
                          //true -> 열려있는상태

                      

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial connection
  }

  Serial.println("");   // blank new line

  Serial.println("Calibrating MQ7");
  mq7.calibrate();    // calculates R0
  Serial.println("Calibration done!");

  myStepper.setSpeed(60);
  Serial.print("Window : ");
 if(window==false) Serial.println("Close");
 else if(window==true) Serial.println("Open");
 Serial.println("=============================================== ");
 Serial.println();
  


}


 void sensor_open(){
    Serial.println("open");
    myStepper.step(stepsPerRevolution);
    Serial.println("stop");
    window = true;

    Serial.print("Window Status : ");
    Serial.println(window);
    Serial.println();

 }

 void sensor_close()
 {
    Serial.println("Close");
    myStepper.step(-stepsPerRevolution);
    window = false;

    Serial.print("Window Status : ");
    Serial.println(window);
    Serial.println();
}

void loop() {
  Serial.print("PPM = "); Serial.println(mq7.readPpm());

  Serial.println("");   // blank new line
  delay(1000);

 int value = digitalRead(2);

 Serial.print("Now : ");

 Serial.print("current gas : ");
 Serial.println(analogRead(gasPin));
 Serial.println();
 Serial.print("Window : ");
 if(window==false) Serial.println("Close");
 else if(window==true) Serial.println("Open");
 Serial.println("=============================================== ");
 Serial.println();
 
 if(window == false) //창문이 닫혀있고 비가 안오는 상태
 {
    if(analogRead(gasPin)>=gas1)
    {
      sensor_open();
    }
    
    else if(analogRead(gasPin)<=gas1)
    {
      sensor_close();
    }
    
 }
 

 
 else if(window == true) //창문이열려있고 비가 안오는 상태
 {
    if(analogRead(gasPin)<=gas1)
    {
      sensor_close();
    }
    else if(analogRead(gasPin)>=gas1)
    {
      sensor_open();
    }
    
 }
 

 
  delay(500);
  
  
}
