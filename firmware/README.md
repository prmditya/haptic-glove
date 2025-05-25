# Firmware for Haptic Glove (ESP32) 🤖✨

This directory contains the Arduino sketch and associated files for the **ESP32 microcontroller**, which serves as the brain of the Haptic Glove. This firmware is responsible for establishing a Bluetooth Serial connection, receiving commands from the Python application, and controlling the haptic actuators (vibration motors).

## Features

* **Bluetooth Serial Communication:** Enables wireless data exchange with the host Python application.
* **Command Parsing:** Interprets simple string commands (e.g., "VIBRATE", "STOP") sent from the Python app.
* **Haptic Actuator Control:** Activates and deactivates the vibration motors on the glove based on received commands.
* **Initialization Sequence:** Includes a brief startup vibration to confirm power and functionality.

## Getting Started

### Requirements

* **ESP32 Development Board:** (e.g., ESP32 Dev Kit C, NodeMCU-32S, etc.)
* **Arduino IDE** or **PlatformIO IDE** (recommended for better project management).
* **ESP32 Boards Manager:** Installed in your Arduino IDE.
* **Haptic Actuators:** Connected to the appropriate GPIO pins on your ESP32 as defined in the code.

## Setup Instructions

### 1. Preparing your ESP32

1.  **Install ESP32 Boards Manager:**
    * In Arduino IDE, go to `File > Preferences`.
    * In "Additional Boards Manager URLs", add: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
    * Go to `Tools > Board > Boards Manager...` and search for "ESP32" and install the "esp32 by Espressif Systems" package.
2.  **Install Libraries:** This firmware typically only relies on built-in libraries like `BluetoothSerial.h`. Ensure your ESP32 board support package is up-to-date.

### 2. Uploading the Firmware

1.  **Open the Project:**
    * **Arduino IDE:** Open the `esp32_haptic_glove.ino` file directly from the `firmware/esp32_haptic_glove/` directory.
    * **PlatformIO:** Open the `firmware/esp32_haptic_glove/` folder as a project in PlatformIO.
2.  **Select Your Board:** Go to `Tools > Board > ESP32 Arduino` and select the specific ESP32 development board you are using (e.g., `ESP32 Dev Module`).
3.  **Select the COM Port:** Go to `Tools > Port` and select the COM port connected to your ESP32.
4.  **Upload:** Click the "Upload" button (right arrow icon) in Arduino IDE or the "Upload" task in PlatformIO.

Once uploaded, your ESP32 should start advertising its Bluetooth name (default: "HapticGlove\_Static") and be ready to pair with your computer.

## Code Structure (Simplified)

The main `esp32_haptic_glove.ino` file generally contains:

* **Global Variables:** For BluetoothSerial object, motor pins, etc.
* **`setup()` function:** Initializes Bluetooth, serial communication for debugging, and configures GPIO pins for motors.
* **`loop()` function:** Continuously checks for incoming Bluetooth data, parses commands, and controls the motors accordingly.

## Customization

* **Bluetooth Device Name:** You can change `device_name` string in `setup()` if you want a different Bluetooth name for your glove.
* **Motor Pins:** Adjust the `int motorPin = ...` (or similar definitions) to match the actual GPIO pins your vibration motors are connected to on the ESP32.
* **Haptic Patterns:** You can expand the command parsing (`if/else if` statements) in the `loop()` function to support more complex vibration patterns (e.g., "VIBRATE_STRONG", "VIBRATE_PULSE", "VIBRATE_SHORT") that can be triggered by the Python app.


## Troubleshooting

* **"Could not open port..." / "Permission denied"**: Ensure the correct COM port is selected and no other program is currently using it (e.g., Serial Monitor from a previous session).
* **"Failed to connect to ESP32"**: Make sure your ESP32 is powered on and in programming/normal mode, and that you have the correct board selected.
* **No Bluetooth advertisement**: Double-check your `setup()` function for `BluetoothSerial.begin()`.
* **No vibration**: Verify wiring, motor power supply, and that your `loop()` logic correctly activates the `digitalWrite()` commands for your motor pins.