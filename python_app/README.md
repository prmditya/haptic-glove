# Haptic Glove Control Application (Python) 💻🖐️

This directory contains the Python desktop application that serves as the control center for your Haptic Glove. It manages the Bluetooth communication with the ESP32 firmware, houses the game-specific profiling logic, and provides a user-friendly Tkinter GUI.

## Features

* **Bluetooth Serial Connection Management:** Automatically discovers and connects to the ESP32 Haptic Glove via Bluetooth COM port.
* **Game Profiling System:** Dynamically loads and runs specialized profiles for different games, allowing for tailored haptic feedback based on in-game events.
    * **Live for Speed (LFS) Profile:** Listens to LFS's OutGauge UDP telemetry to trigger haptics for RPM, gear changes, etc.
    * **Minecraft Profile:** Works in conjunction with a custom Minecraft mod to receive and process in-game events for haptic feedback.
* **Command Sending:** Sends clear haptic commands (e.g., "VIBRATE", "STOP") to the ESP32.
* **User-Friendly GUI:** A simple Tkinter interface for easy control and monitoring.

## Getting Started

### Requirements

* **Python 3.x:** (Tested with Python 3.8+)
* **Paired ESP32 Haptic Glove:** Your ESP32 must be flashed with the [firmware](/firmware/README.md) and paired as a Bluetooth Serial Port (COM port) on your system.
* **Required Python Libraries:**
    * `pyserial`
    * `tkinter` (usually built-in with Python)
    * `socket` (built-in)
    * `threading` (built-in)
    * `time` (built-in)
    * `struct` (built-in, for LFS)


## Setup & Running the Application

1.  **Navigate to the Directory:**
    Open your terminal or command prompt and change your current directory to `python_app/`:
    ```bash
    cd HapticGlove_Project/python_app/
    ```

2.  **Install Python Dependencies:**
    Make sure you have all necessary Python libraries installed.
    ```bash
    pip install -r requirements.txt
    ```
    *(If you encounter issues with `tkinter`, ensure your Python installation includes Tk/Tcl support. On some Linux distributions, you might need to install `python3-tk`.)*

3.  **Ensure ESP32 Bluetooth is Paired:**
    Before running the app, confirm your ESP32 Haptic Glove is paired with your computer and appears as a Bluetooth COM port (e.g., COM8, COM9, COMx) in your operating system's Device Manager. The application will attempt to automatically find the correct port.

4.  **Run the Application:**
    ```bash
    python main.py
    ```
    A GUI window titled "Haptic Glove Control" should appear.


## Using the Application

The GUI provides straightforward controls:

* **"Connect Bluetooth" Button:** Initiates the connection to your ESP32 Haptic Glove. The application will try to find the correct COM port. Status messages will appear in the console.
* **"Disconnect Bluetooth" Button:** Closes the active Bluetooth serial connection.
* **Game Profile Selection:** A dropdown menu or radio buttons (depending on `main.py`'s implementation) to select which game profile you want to activate.
    * Once selected, click "Start Profile" to begin listening for game events.
    * Click "Stop Profile" to deactivate the current game profile.
* **Console Output:** Monitor the terminal/console where you ran `main.py` for detailed logging and status updates from both the `BluetoothManager` and the active game profiles.

## Game Profiles Details

The `game_profiles/` directory contains the logic for integrating with specific games.

### `lfs_profile.py` (Live for Speed)

* **Functionality:** This profile listens for UDP packets on **port 30000** (default for LFS OutGauge). It parses telemetry data like RPM, speed, and gear changes, then sends appropriate "VIBRATE" or "STOP" commands to the glove via the `BluetoothManager`.
* **LFS In-Game Setup:**
    1.  Launch Live for Speed.
    2.  Go to `Options > Display > OutGauge`.
    3.  Check `OutGauge Packet`.
    4.  Set `IP Address` to `127.0.0.1` (localhost).
    5.  Set `Port` to `30000`.
    6.  Set `Interval` to `10ms` or `20ms` for optimal responsiveness.
    * **Important:** LFS must be running and sending OutGauge data for this profile to function.

### `minecraft_profile.py` (Minecraft)

* **Functionality:** This profile listens for UDP packets on **port 25566** from a custom Minecraft mod. It expects simple string events (e.g., "DAMAGE", "BLOCK\_BREAK", "JUMP") and translates them into specific haptic feedback commands.
* **Minecraft In-Game Setup:**
    1.  Ensure you have correctly [installed the custom Minecraft mod](/minecraft_mod/README.md) into your Minecraft client.
    2.  Launch Minecraft with the mod loaded.
    * **Important:** The Minecraft mod must be running and configured to send events to `127.0.0.1:25566` for this profile to function. Check your firewall if events aren't being received.

## Troubleshooting

* **"Bluetooth not connected. Please connect first."**: Click the "Connect Bluetooth" button in the GUI.
* **"No COM port found" / "Failed to open serial port"**:
    * Ensure your ESP32 is powered on and paired.
    * Verify the Bluetooth COM port in Device Manager.
    * Try restarting the Python app or your computer.
* **No haptic feedback in game**:
    * Ensure the Python app is connected to the ESP32.
    * Ensure the correct game profile is selected and "Start Profile" is clicked.
    * Verify the in-game settings for telemetry (LFS OutGauge) or that the Minecraft mod is correctly installed and running.
    * Check for any firewall rules blocking UDP ports (30000 for LFS, 25566 for Minecraft).
* **Error messages in console**: Read the error messages carefully; they often indicate the root cause.