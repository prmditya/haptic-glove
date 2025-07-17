#include "BluetoothSerial.h"

const int VIBRATION_MOTOR_PIN = 5;

BluetoothSerial SerialBT;

const char* bluetoothDeviceName = "HapticGlove_Static";

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 Bluetooth Vibration Control");

  SerialBT.begin(bluetoothDeviceName);
  Serial.print("Bluetooth device '");
  Serial.print(bluetoothDeviceName);
  Serial.println("' started. Ready to pair.");

  pinMode(VIBRATION_MOTOR_PIN, OUTPUT);
  digitalWrite(VIBRATION_MOTOR_PIN, LOW);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  if (SerialBT.available()) {
    String command = SerialBT.readStringUntil('\n');
    command.trim();

    Serial.print("Received command: ");
    Serial.println(command);

    if (command == "VIBRATE") {
      digitalWrite(VIBRATION_MOTOR_PIN, HIGH);
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("Vibration motor ON");

    } else if (command == "STOP") {
      digitalWrite(VIBRATION_MOTOR_PIN, LOW);
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("Vibration motor OFF");

    } else {
      Serial.print("Unknown command: ");
      Serial.println(command);

    }
  }

  delay(10);
}
