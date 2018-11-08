#include <Servo.h>
#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>

float A0_LDR = 0;
float Conquistas = 0;
float A1_LM35_Temp = 0;
float D12_sonar = 0;
float D6_Buzzer = 0;
float PIR = 0;
float Interruptor = 0;

void setup(){
Serial.begin(115200); //turn on serial monitor
}


Servo servo_10;
void config (){
  //Serial.println("Teste de Medições");
  servo_10.write(180);
  analogWrite(9,0);
  tone(6,262,0.25*1000);
  delay(250);

}

float getDistance(int trig,int echo){
    pinMode(trig,OUTPUT);
    digitalWrite(trig,LOW);
    delayMicroseconds(2);
    digitalWrite(trig,HIGH);
    delayMicroseconds(10);
    digitalWrite(trig,LOW);
    pinMode(echo, INPUT);
    return pulseIn(echo,HIGH,30000)/58.0;
}
void medir (){
  A0_LDR = abs(analogRead(A0+0));
  //Serial.println(String("LDR: ") + String(A0_LDR));
  A1_LM35_Temp = abs((analogRead(A0+1) * 500) / 1024);
  //Serial.println(String("Temp: ") + String(A1_LM35_Temp));
  D12_sonar = getDistance(12,12);
  //Serial.println(String("Dist: ") + String(D12_sonar));

}





void loop() {


medir();
Serial.print(A0_LDR);
Serial.print(" , ");
Serial.print(A1_LM35_Temp);
Serial.print(" , ");
Serial.println(D12_sonar);

delay(250); //Pause between readings.
}
