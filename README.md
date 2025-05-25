# Haptic Glove for Gaming Immersion ✨🎮


*(Replace with a captivating GIF or screenshot of your project in action\! Place it in the `assets/` folder.)*

## Project Overview 🚀

Dive into a new dimension of gaming with the **Haptic Glove for Gaming Immersion**\! This project presents an innovative haptic feedback system, powered by an **ESP32** microcontroller and controlled by a versatile **Python application**. It's designed to bring in-game events to life, translating them into tangible vibrations and sensations directly on the user's hand. Get ready to *feel* your games like never before\!

## Key Features 🌟

  * **ESP32-Powered Hardware:** Utilizes the efficient ESP32 microcontroller for precise control of haptic actuators (e.g., vibration motors), delivering responsive feedback.
  * **Modular Python Application (Tkinter GUI):** A user-friendly desktop application built with Tkinter, offering a intuitive interface to connect the glove and manage game-specific profiles.
  * **Comprehensive Game Profiling System:** Features a robust, modular system for creating tailored haptic feedback logic for various games.
      * **Live for Speed (LFS) Integration:** Connects seamlessly to LFS via its **OutGauge UDP telemetry**, providing dynamic feedback for events like high RPMs and gear changes. 🏎️💨
      * **Minecraft Integration (Custom Mod):** Employs a custom-built Minecraft mod to capture in-game events (e.g., taking damage, breaking blocks) and relay them to the Python app for immersive haptic responses. ⛏️💥
  * **Reliable Bluetooth Communication:** Ensures stable and consistent wireless communication between the Python application and the ESP32-based glove. 📶

## System Architecture 🏗️

The Haptic Glove system is a symphony of hardware and software components working in harmony:

  * **ESP32 Firmware:** The brain of the glove, handling sensor data (if applicable) and executing haptic commands received from the Python app.
  * **Python Application:** The central hub, processing game telemetry/events, applying haptic logic based on the active game profile, and sending commands to the ESP32.
  * **Game Mods (e.g., Minecraft Mod):** Bridges the gap directly within supported games, capturing specific in-game occurrences and forwarding them to the Python application.

*(Replace with the path to your system block diagram in the `assets/` folder.)*

## Getting Started 🏁

Follow these steps to set up and experience the Haptic Glove system.

### 1\. Hardware Requirements 🛠️

  * **ESP32 Development Board** (e.g., ESP32 Dev Module)
  * **Haptic Actuators** (e.g., vibration motors, ideally LRA or ERM)
  * **Sensors** (Optional, e.g., flex sensors for fingers, IMU for hand orientation – *if your glove has these*)
  * **Power Supply** for ESP32 and actuators
  * **Wiring components** (breadboard, jumper wires, etc.)

### 2\. Software Requirements 💻

  * [**Arduino IDE**](https://www.arduino.cc/en/software) or [**PlatformIO**](https://platformio.org/) for ESP32 firmware.
  * **Python 3.x**
  * **Required Python Libraries:** Install them easily via pip:
    ```bash
    pip install -r python_app/requirements.txt
    ```
  * **Minecraft Java Edition** (Required for Minecraft Haptics)
  * **Minecraft Mod Loader** (e.g., [Fabric](https://fabricmc.net/) or [Forge](https://files.minecraftforge.net/)) compatible with your Minecraft version.

## Setup Instructions 🔧

### 1\. Firmware Setup (ESP32)

1.  Navigate to the `firmware/esp32_haptic_glove/` directory.
2.  Open `esp32_haptic_glove.ino` with Arduino IDE (or import the project into PlatformIO).
3.  Ensure you have the ESP32 boards manager installed in your Arduino IDE.
4.  Connect your ESP32 board to your computer via USB.
5.  Select the correct board and COM port.
6.  **Upload the sketch** to your ESP32.

*(See `firmware/README.md` for more detailed firmware flashing instructions. 📖)*

### 2\. Python Application Setup

1.  Navigate to the `python_app/` directory.
2.  Install the necessary Python libraries (if you haven't already):
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ensure your ESP32 Bluetooth is paired** with your computer and appears as a **COM port** (e.g., COM8, COM9). You can verify this in your computer's Device Manager. The application is designed to automatically detect the correct port.
4.  Run the main application:
    ```bash
    python main.py
    ```
    A user-friendly GUI window will pop up, allowing you to connect to the glove and choose your desired game profile.

*(See `python_app/README.md` for more detailed application usage instructions. 📖)*

### 3\. Minecraft Mod Setup

1.  Navigate to the `minecraft_mod/` directory.
2.  Follow the comprehensive instructions provided in `minecraft_mod/README.md` to:
      * **Build the Minecraft mod** (e.g., using `gradlew build`). This process will typically generate a `.jar` file.
      * **Install the mod** into your Minecraft client (usually by placing the generated `.jar` file into your Minecraft `mods` folder).
3.  Ensure your Minecraft instance is running with the mod successfully loaded *before* activating the Minecraft profile in the Haptic Glove Python application.

## Supported Game Profiles 🎮

This system employs dedicated profiles to deliver customized haptic feedback for various games.

### Live for Speed (LFS) Haptics 🏎️

  * **Functionality:** The `lfs_profile.py` module actively listens for **UDP telemetry data** originating from LFS's **OutGauge** feature. It cleverly interprets data such as engine RPM, gear changes, and vehicle speed to trigger corresponding vibrations on the haptic glove, providing a visceral connection to the race.
  * **Setup in LFS:**
    1.  In LFS, navigate to `Options` -\> `Display` -\> `OutGauge`.
    2.  Enable the `OutGauge Packet` option.
    3.  Set the IP address to `127.0.0.1` (localhost).
    4.  Set the port to `30000`.
    5.  For real-time and responsive feedback, set the **interval** to a low value (e.g., `10ms` or `20ms`).
        *(**Important:** Make sure LFS is running and actively sending data before you activate the LFS profile in the Python application.)*

### Minecraft Haptics ⛏️

  * **Functionality:** The `minecraft_profile.py` module seamlessly integrates with the custom Minecraft mod. This mod intelligently detects a variety of in-game events (e.g., player taking damage, breaking specific blocks, jumping, using certain items) and sends simple UDP messages to the Python application. The Python module then translates these events into distinct and meaningful haptic feedback patterns on the glove.
  * **Setup for Minecraft:**
    1.  Ensure you have properly installed the custom Minecraft mod (refer to the "Minecraft Mod Setup" section above).
    2.  Launch your Minecraft game with the mod successfully loaded.
    3.  Activate the "Minecraft" profile within the Haptic Glove Control Python application.
        *(The mod automatically dispatches events to the Python app on UDP port 25566. Please ensure this port is not blocked by your firewall.)*

## License 📜

This project is licensed under the [MIT License](https://www.github.com/prmditya/haptic-glove/blob/main/LICENSE).
