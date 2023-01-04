#include <Servo.h>
#include<SoftwareSerial.h>

Servo myservo;

//SoftwareSerial bluetooth(10,11);

int IN1 = 4; //ON Kiri
int EN1 = 5; //Motor Kiri
int EN2 = 6; //Motor Kanan
int IN2 = 7; //ON Kanan

void setup() {
  Serial.begin(115200);
//  bluetooth.begin(115200);
  myservo.attach(9);
  pinMode(EN1, OUTPUT);
  pinMode(EN2, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
}

void servoOn() {
  myservo.write(90);             
  delay(5000);                       
  myservo.write(0);
}

//void right() {
//  // function untuk roda bergerak maju
//  analogWrite(EN1, 255);
//  analogWrite(EN2, 0);
//  digitalWrite(IN1, HIGH);
//  digitalWrite(IN2, HIGH);
//}

//void left() {
//  // function untuk roda bergerak maju
//  analogWrite(EN1, 0);
//  analogWrite(EN2, 255);
//  digitalWrite(IN1, HIGH);
//  digitalWrite(IN2, HIGH);
//}

void forward() {
  // function untuk roda bergerak maju
//  analogWrite(EN1, 255);
//  analogWrite(EN2, 255);
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, HIGH);
}


void backward() {
  analogWrite(EN1, 255);
  analogWrite(EN2, 255);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}


void stopf() {
  analogWrite(EN1, 0);
  analogWrite(EN2, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}

void loop() {
  String perintah = "";
//  while (bluetooth.available() > 0){
  while (Serial.available() > 0) {
//    char karakter = bluetooth.read();
    char karakter = Serial.read();
    perintah = perintah + karakter;
    delay(20);
  }

  if (perintah.equals("")) {
    return;
  } else if (perintah.equals("1")) {
    forward();
  } else if (perintah.equals("2")) {
    servoOn();
  } else if (perintah.equals("3")) {
    backward();
  } else if (perintah.equals("4")) {
    stopf();
  }

}
