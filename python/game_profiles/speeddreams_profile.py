import socket
import threading
import time

class SpeedDreamsProfile:
    def __init__(self, bt_manager):
        self.bt_manager = bt_manager
        self.udp_port = 54321 # Port yang dikonfigurasi di modifikasi C++ game
        self.udp_socket = None
        self.listener_thread = None
        self.running = False

    def start(self):
        print(f"Starting Speed Dreams profile. Listening for UDP on port {self.udp_port}...")
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.bind(("", self.udp_port))
            self.udp_socket.settimeout(0.5)
            self.running = True
            self.listener_thread = threading.Thread(target=self._listen_udp)
            self.listener_thread.daemon = True
            self.listener_thread.start()
            print("Speed Dreams UDP listener started.")
        except Exception as e:
            print(f"Failed to start Speed Dreams UDP listener: {e}")
            self.running = False
            if self.udp_socket:
                self.udp_socket.close()

    def _listen_udp(self):
        while self.running:
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                message = data.decode('utf-8').strip()
                print(f"Received from Speed Dreams: {message}")

                if message == "CRASH":
                    self.bt_manager.send_command("VIBRATE")
                elif message == "NORMAL": # Atau apa pun yang Anda kirim saat tidak ada tabrakan
                    self.bt_manager.send_command("STOP")

            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Error in Speed Dreams UDP listener: {e}")
                break

    def stop(self):
        print("Stopping Speed Dreams profile...")
        self.running = False
        if self.udp_socket:
            self.udp_socket.close()
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=1)
        self.bt_manager.send_command("STOP")
        print("Speed Dreams profile stopped.")