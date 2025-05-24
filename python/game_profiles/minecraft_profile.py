import socket
import threading
import time

class MinecraftProfile:
    def __init__(self, bt_manager):
        self.bt_manager = bt_manager
        self.udp_port = 12345 # Port yang sama dengan di mod Java Minecraft
        self.udp_socket = None
        self.listener_thread = None
        self.running = False

    def start(self):
        print(f"Starting Minecraft profile. Listening for UDP on port {self.udp_port}...")
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.bind(("", self.udp_port)) # Bind ke semua interface
            self.running = True
            self.listener_thread = threading.Thread(target=self._listen_udp)
            self.listener_thread.daemon = True # Agar thread berhenti saat main program berhenti
            self.listener_thread.start()
            print("Minecraft UDP listener started.")
        except Exception as e:
            print(f"Failed to start Minecraft UDP listener: {e}")
            self.running = False
            if self.udp_socket:
                self.udp_socket.close()

    def _listen_udp(self):
        while self.running:
            try:
                data, addr = self.udp_socket.recvfrom(1024) # Buffer size 1024 bytes
                message = data.decode('utf-8').strip()
                print(f"Received from Minecraft: {message}")

                # Logika pemicu getaran statis
                if message == "HIT" or message == "EXPLOSION":
                    self.bt_manager.send_command("VIBRATE")
                    print("Sending Vibrate")
                    # Untuk getaran singkat, Anda bisa menambahkan delay dan STOP
                    threading.Timer(0.5, self.bt_manager.send_command, args=["STOP"]).start()
                # else: # Jika Anda ingin motor mati saat tidak ada event spesifik
                #     self.bt_manager.send_command("STOP")

            except socket.timeout:
                continue # Lanjutkan jika timeout (tidak ada data)
            except Exception as e:
                if self.running: # Hanya cetak error jika masih berjalan
                    print(f"Error in Minecraft UDP listener: {e}")
                break # Keluar dari loop jika ada error

    def stop(self):
        print("Stopping Minecraft profile...")
        self.running = False
        if self.udp_socket:
            self.udp_socket.close() # Menutup socket akan menghentikan recvfrom
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=1) # Tunggu thread berhenti
        self.bt_manager.send_command("STOP") # Pastikan motor mati
        print("Minecraft profile stopped.")