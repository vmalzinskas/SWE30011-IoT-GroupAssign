#include <Servo.h>
#include <DHT.h>  // Include DHT sensor library

#define DHTPIN 7     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);  // Initialize DHT sensor object

Servo valveServo;
int valvePin = 8;
int valveClosedAngle = 0;
int valveOpenAngle = 90;

int motorPin = A5;

int tempPin = A0;

unsigned long previousMillis = 0;
const long interval = 1000;  // Interval between readings in milliseconds

void setup() {
  Serial.begin(9600);
  dht.begin();  // Initialize DHT sensor
  valveServo.attach(valvePin);  // Attaches the servo to the pin
  pinMode(motorPin, OUTPUT);
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Read humidity and temperature from DHT sensor
    float humidity = dht.readHumidity();
    //float temperature = dht.readTemperature();
    float temperature = readTemp(tempPin);

    if (isnan(humidity) || isnan(temperature)) {
      //Serial.println(F("Failed to read from DHT sensor!"));
      return;
    }

    // Format time stamp
    unsigned long seconds = currentMillis / 1000;
    unsigned long minutes = seconds / 60;
    unsigned long hours = minutes / 60;
    String time_str = String(hours % 24) + ":" + String(minutes % 60) + ":" + String(seconds % 60);

    // Send time and temperature data over serial
    Serial.print(time_str);
    Serial.print(",");
    Serial.print(temperature);
    Serial.print(",");
    Serial.println(humidity);
  }

  if (Serial.available() > 0) {
    char incomingByte = Serial.read(); // Read the incoming byte
    if (incomingByte == '0') {
      openValve(); // Command to open the valve
    }
    else if (incomingByte == '1') {
      closeValve(); // Command to close the valve
    }
    else if (incomingByte == 'h') {
      motorHigh(); // Command to set motor to high speed
    }
    else if (incomingByte == 's') {
      motorStop(); // Command to stop the motor
    }
    else {
      //Serial.println("Invalid Command.");
    }
  }
}
float readTemp(int TempPin)
{
    float value = analogRead(TempPin);
    float temp = value*(5000/1024.0);
    return temp/10;
}

void closeValve() {
  valveServo.write(valveClosedAngle);
  //Serial.println("Valve Closed.");
}

void openValve() {
  valveServo.write(valveOpenAngle);
  //Serial.println("Valve Opened.");
}

void motorHigh() {
  analogWrite(motorPin, 255);
  //Serial.println("Motor High.");
}

void motorStop() {
  analogWrite(motorPin, 0);
  //Serial.println("Motor Stopped.");
}
