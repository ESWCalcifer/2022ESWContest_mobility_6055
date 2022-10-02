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
//const int coco=mq7.readPpm();

int INA = 5;  
int INB = 6;
int gas1=9;   //이거 ppm아니라 ppm200의 역변환계산필요함.
int gas2=8;
boolean window = false;   //false -> 닫혀있는상태
                          //true -> 열려있는상태

                      

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial connection
  }

  pinMode(7, OUTPUT);
  pinMode(INA,OUTPUT); 
  pinMode(INB,OUTPUT); 


  

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
    digitalWrite(7, HIGH); // 
    //delay(1000); // 5. 1000ms동안 대기합니다. 1000ms=1초
    ////digitalWrite(7, LOW); // 6. LOW: 전압이 0V로 설정됩니다.
    //delay(10);
    digitalWrite(INA,HIGH);
    digitalWrite(INB,LOW); 
    
    

    
    //Serial.println("stop");
    window = true;//닫혔다가open이면
   

    Serial.print("Window Status : ");
    Serial.println(window);
    Serial.println();

 }

 void sensor_close()
 {
    Serial.println("Close");
    myStepper.step(-stepsPerRevolution);
    digitalWrite(7, LOW);
    digitalWrite(INA,HIGH);
    digitalWrite(INB,HIGH); 
    window = false;
   

    Serial.print("Window Status : ");
    Serial.println(window);
    Serial.println();
}



void loop() {
  Serial.print("PPM = "); Serial.println(mq7.readPpm());
  //readPpm

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
 
 if(window == false) //창문이 닫혀있을 때
 {
    if(mq7.readPpm()>=gas1)
    {
      sensor_open();
    }
    
   // else if(analogRead(gasPin)<=gas1)
   // {
      
    //}
    
 }
 

 
 else if(window == true) //창문이열려있을 때
 {
    if(mq7.readPpm()<= gas2)
    {
      sensor_close();
    }
   
    
 }
 

 
  delay(100);
  
  
}
