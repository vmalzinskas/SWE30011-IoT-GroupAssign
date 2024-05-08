#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <DHT.h>

#define DHTPIN 7     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);  // Initialize DHT sensor object

Servo valveServo;
int valvePin = 8;
int valveClosedAngle = 0;
int valveOpenAngle = 90;

//int motorPin = A5;
int motorPin = 3;

int tempPin = A0;

#define RFID_SS_PIN 10
#define RFID_RST_PIN 9

MFRC522 rfid(RFID_SS_PIN, RFID_RST_PIN); // Create MFRC522 instance

unsigned long previousMillis = 0;
const long interval = 1000;  // Interval between readings in milliseconds

void setup() {
  Serial.begin(9600);
  SPI.begin(); // Initialize SPI bus
  rfid.PCD_Init(); // Initialize RFID module
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
    float temperature = dht.readTemperature();
    //float temperature = readTemp(tempPin);

    if (isnan(humidity) || isnan(temperature)) {
      //Serial.println(F("Failed to read from DHT sensor!"));
      return;
    }

    // Read RFID tag data
    String rfidTag = readRFIDTag();

    // Format time stamp
    unsigned long seconds = currentMillis / 1000;
    unsigned long minutes = seconds / 60;
    unsigned long hours = minutes / 60;
    String time_str = String(hours % 24) + ":" + String(minutes % 60) + ":" + String(seconds % 60);

    // Send data over serial
    Serial.print(time_str);
    Serial.print(",");
    Serial.print(temperature);
    Serial.print(",");
    Serial.print(humidity);
    Serial.print(",");
    Serial.print("20"); // Additional data (replace with actual value)
    Serial.print(",");
    Serial.print("75"); // Additional data (replace with actual value)
    Serial.print(",");
    if (rfidTag != "") {
      Serial.println(rfidTag);
    } else {
      Serial.println("N/A"); // No RFID tag detected
    }
  }

  // Check for incoming serial commands
  if (Serial.available() > 0) {
    char incomingByte = Serial.read(); // Read the incoming byte
    if (incomingByte == '0') {
      openValve(); // Command to open the valve
    } else if (incomingByte == '1') {
      closeValve(); // Command to close the valve
    } else if (incomingByte == 'h') {
      motorHigh(); // Command to set motor to high speed
    } else if (incomingByte == 'm') {
      motorMed(); // Command to set motor to high speed
    } else if (incomingByte == 'l') {
      motorLow(); // Command to set motor to high speed
    } else if (incomingByte == 's') {
      motorStop(); // Command to stop the motor
    } else {
      //Serial.println("Invalid Command.");
    }
  }
}

String readRFIDTag() {
  // Check if a new RFID card is present
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    String rfidTag = "";
    // Read RFID tag UID
    for (byte i = 0; i < rfid.uid.size; i++) {
      rfidTag += (rfid.uid.uidByte[i] < 0x10 ? "0" : "");
      rfidTag += String(rfid.uid.uidByte[i], HEX);
    }
    rfid.PICC_HaltA(); // Halt PICC
    rfid.PCD_StopCrypto1(); // Stop encryption on PCD
    return rfidTag;
  } else {
    return ""; // No RFID tag detected
  }
}

float readTemp(int TempPin) {
  float value = analogRead(TempPin);
  float temp = value * (5000 / 1024.0);
  return temp / 10;
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
void motorMed() {
  analogWrite(motorPin, 125);
  //Serial.println("Motor Med.");
}
void motorLow() {
  analogWrite(motorPin, 50);
  //Serial.println("Motor low.");
}
void motorStop() {
  analogWrite(motorPin, 0);
  //Serial.println("Motor Stopped.");
}
