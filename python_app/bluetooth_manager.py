import serial.tools.list_ports
import serial
import time
import sys

class BluetoothManager:
    def __init__(self, device_name="HapticGlove_Static", baud_rate=115200):
        self.device_name = device_name
        self.baud_rate = baud_rate
        self.ser = None
        self.port = None

    def find_esp32_port(self):
        print(f"[BT_Manager] Searching for ESP32 Bluetooth COM port: {self.device_name}...")
        
        candidate_ports = ["COM8", "COM9"]
        
        for p_candidate in candidate_ports:
            print(f"[BT_Manager] Attempting direct check for: {p_candidate}")
            try:
                # Coba buka port sebentar dengan timeout sangat rendah
                # Ini akan memverifikasi apakah port bisa diakses tanpa memblokir
                temp_ser = serial.Serial(p_candidate, self.baud_rate, timeout=0.1)
                temp_ser.close()
                self.port = p_candidate
                print(f"[BT_Manager] Confirmed working port: {self.port}")
                return True
            except serial.SerialException as e:
                print(f"[BT_Manager] Port {p_candidate} is not connectable or is busy: {e}")
                continue # Coba port berikutnya
            except Exception as e:
                print(f"[BT_Manager] Unexpected error checking {p_candidate}: {e}")
                continue

        ports = serial.tools.list_ports.comports()
        for p in ports:
            print(f"[BT_Manager] Checking port: {p.device} - {p.description}")
            if self.device_name in p.description or self.device_name in p.name:
                self.port = p.device
                print(f"[BT_Manager] Found ESP32 on port: {self.port} (by description)")
                return True
        
        print(f"[BT_Manager] ESP32 Bluetooth COM port '{self.device_name}' not found.")
        self.port = None
        return False

    def connect(self):
        if self.ser and self.ser.is_open:
            print("[BT_Manager] Already connected.")
            return True

        if not self.port:
            if not self.find_esp32_port():
                print("[BT_Manager] No COM port found to connect to.")
                return False

        try:
            print(f"[BT_Manager] Attempting to open serial port {self.port} at {self.baud_rate} baud...")
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)
            if self.ser.is_open:
                print("[BT_Manager] Serial connection to ESP32 established.")
                return True
            else:
                print(f"[BT_Manager] Failed to open serial port {self.port} (is_open is False).")
                self.ser = None
                return False
        except serial.SerialException as e:
            print(f"[BT_Manager] Failed to open serial port {self.port} due to SerialException: {e}")
            self.ser = None
            return False
        except Exception as e:
            print(f"[BT_Manager] An unexpected error occurred during connection to {self.port}: {e}")
            self.ser = None
            return False

    def send_command(self, command):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(f"{command}\n".encode('utf-8'))
                return True
            except serial.SerialException as e:
                print(f"[BT_Manager] Error sending command: {e}. Attempting to reconnect...")
                self.ser = None # Tandai koneksi sebagai terputus
                if self.connect(): # Coba sambung ulang
                    return self.send_command(command) # Coba kirim lagi setelah reconnect
                return False
            except Exception as e:
                print(f"[BT_Manager] Unexpected error sending command: {e}")
                self.ser = None # Tandai koneksi sebagai terputus
                return False
        else:
            print("[BT_Manager] Serial connection not active. Attempting to reconnect...")
            if self.connect():
                return self.send_command(command) # Coba kirim lagi setelah reconnect
            return False

    def disconnect(self):
        if self.ser and self.ser.is_open:
            print("[BT_Manager] Sending STOP command to ESP32 before disconnecting...")
            try:
                self.send_command("STOP") # Pastikan motor mati
                self.ser.close()
                print("[BT_Manager] Serial connection closed.")
            except Exception as e:
                print(f"[BT_Manager] Error during disconnection: {e}")
        self.ser = None
        self.port = None

# Contoh penggunaan (opsional, untuk testing)
if __name__ == "__main__":
    bt_manager = BluetoothManager()
    if bt_manager.connect():
        print("Test: Sending VIBRATE for 3 seconds...")
        bt_manager.send_command("VIBRATE")
        time.sleep(3)
        print("Test: Sending STOP...")
        bt_manager.send_command("STOP")
        time.sleep(1)
    bt_manager.disconnect()