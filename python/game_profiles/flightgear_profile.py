import socket
import threading
import time

class FlightGearProfile:
    def __init__(self, bt_manager):
        self.bt_manager = bt_manager
        self.udp_port = 5500 # Port yang dikonfigurasi di FlightGear
        self.udp_socket = None
        self.listener_thread = None
        self.running = False

    def start(self):
        print(f"Starting FlightGear profile. Listening for UDP on port {self.udp_port}...")
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.bind(("", self.udp_port))
            # Set timeout agar recvfrom tidak memblokir selamanya saat stop
            self.udp_socket.settimeout(0.5)
            self.running = True
            self.listener_thread = threading.Thread(target=self._listen_udp)
            self.listener_thread.daemon = True
            self.listener_thread.start()
            print("FlightGear UDP listener started.")
        except Exception as e:
            print(f"Failed to start FlightGear UDP listener: {e}")
            self.running = False
            if self.udp_socket:
                self.udp_socket.close()

    def _listen_udp(self):
        while self.running:
            try:
                data, addr = self.udp_socket.recvfrom(2048) # Buffer size
                telemetry_data = data.decode('utf-8').strip()
                # print(f"Received from FlightGear: {telemetry_data}") # Debug

                # Logika pemicu getaran statis:
                # Ini adalah bagian tricky. Anda perlu mengidentifikasi
                # pola dalam 'telemetry_data' yang menandakan event seperti tabrakan, pendaratan keras, dll.
                # Contoh: jika ada string yang mengandung "crash" atau "damage"
                # Atau jika Anda mengkonfigurasi FGFS untuk mengirim nilai 'g_force' atau 'ground_impact_strength'
                # Anda akan mem-parse nilai-nilai ini.

                # Untuk contoh sederhana, kita akan mengasumsikan ada event yang memicu getaran
                # Misal: Jika ada 'g_force' yang tinggi atau 'impact_strength'
                # Ini akan sangat bergantung pada format data output XML Anda di FlightGear.
                # ASUMSI SANGAT SEDERHANA: Jika ada data, getar. (Tidak ideal, tapi ON/OFF)
                # Anda HARUS mengganti ini dengan parsing data yang sebenarnya.
                if "crash" in telemetry_data.lower() or "impact" in telemetry_data.lower() or "ground_impact" in telemetry_data.lower():
                    self.bt_manager.send_command("VIBRATE")
                # else:
                #     self.bt_manager.send_command("STOP")

            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Error in FlightGear UDP listener: {e}")
                break

    def stop(self):
        print("Stopping FlightGear profile...")
        self.running = False
        if self.udp_socket:
            self.udp_socket.close()
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=1)
        self.bt_manager.send_command("STOP")
        print("FlightGear profile stopped.")