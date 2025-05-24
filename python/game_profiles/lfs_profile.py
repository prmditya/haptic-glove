import socket
import threading
import time
import struct

class LFSProfile:
    def __init__(self, bt_manager):
        self.bt_manager = bt_manager
        # Pastikan ini sesuai dengan 'OutGauge Port' di LFS/cfg.txt Anda
        self.udp_port = 30000 
        self.udp_socket = None
        self.listener_thread = None
        self.running = False
        self.profile_name = "Live for Speed (OutGauge Haptics)"

        self.last_vibrate_time = 0
        self.vibration_cooldown = 0.2
        self.vibration_active = False
        self.last_gear = 0 # Untuk deteksi ganti gigi

        # --- FORMAT STRING BERDASARKAN DOKUMENTASI OUTGAUGE (89 bytes) ---
        # Ini adalah format string yang Anda berikan dari contoh code
        self.LFS_OUTGAUGE_FORMAT = '<I3sxH2B7f2I3f15sx15sx'
        # Ukuran paket yang diharapkan adalah 89 byte
        self.EXPECTED_PACKET_SIZE = struct.calcsize(self.LFS_OUTGAUGE_FORMAT)
        
    def start(self):
        if hasattr(self.bt_manager, 'is_connected') and not self.bt_manager.is_connected():
            print(f"[{self.profile_name} Profile] Bluetooth not connected. Please connect first.")
            return False

        print(f"[{self.profile_name} Profile] Starting. Listening for UDP on port {self.udp_port}...")
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Bind ke '0.0.0.0' agar bisa menerima dari IP mana saja di port ini
            self.udp_socket.bind(("0.0.0.0", self.udp_port)) 
            self.udp_socket.settimeout(0.1) # Timeout kecil agar thread bisa dihentikan gracefully
            self.running = True
            self.listener_thread = threading.Thread(target=self._listen_udp, daemon=True)
            self.listener_thread.start()
            print(f"[{self.profile_name} Profile] UDP listener started successfully.")
            return True
        except OSError as e: # Tangani error jika port sudah terpakai
            print(f"[{self.profile_name} Profile] Port {self.udp_port} might be in use or unavailable: {e}")
            self.running = False
            return False
        except Exception as e:
            print(f"[{self.profile_name} Profile] Failed to start UDP listener: {e}")
            self.running = False
            if self.udp_socket:
                self.udp_socket.close()
            return False

    def _listen_udp(self):
        print(f"[{self.profile_name} Profile] Inside _listen_udp thread. Loop starting...")
        while self.running:
            try:
                # Menerima data dengan buffer cukup besar untuk 89 byte
                data, addr = self.udp_socket.recvfrom(self.EXPECTED_PACKET_SIZE + 10) # sedikit lebih besar untuk jaga-jaga
                
                print(f"[{self.profile_name} Profile] Received {len(data)} bytes from {addr}. Data (hex): {data.hex()}") 

                if len(data) == self.EXPECTED_PACKET_SIZE: # Pastikan ukuran paket sesuai
                    telemetry_data = self._parse_outgauge_data(data)
                    if telemetry_data: # Hanya proses jika parsing berhasil
                        self._handle_haptics(telemetry_data)
                else:
                    print(f"[{self.profile_name} Profile] WARNING: Received unexpected packet size: {len(data)} bytes. Expected {self.EXPECTED_PACKET_SIZE} for OutGauge.")
                    pass # Abaikan paket dengan ukuran yang salah

            except socket.timeout:
                # Ketika tidak ada data yang masuk, pastikan getaran berhenti jika aktif
                if self.vibration_active and (time.time() - self.last_vibrate_time) > self.vibration_cooldown:
                    self.bt_manager.send_command("STOP")
                    self.vibration_active = False
                continue
            except Exception as e:
                if self.running: # Hanya print error jika masih running (bukan karena stop)
                    print(f"[{self.profile_name} Profile] CRITICAL ERROR in UDP listener loop: {e}")
                break

        print(f"[{self.profile_name} Profile] UDP listener thread stopping.")

    def _parse_outgauge_data(self, raw_data):
        parsed_data = {}
        try:
            outgauge_pack = struct.unpack(self.LFS_OUTGAUGE_FORMAT, raw_data)

            # Mapping field berdasarkan indeks yang Anda berikan:
            # Time dan Car tidak kita gunakan untuk haptics, tapi bisa disimpan jika perlu
            parsed_data['time'] = outgauge_pack[0]
            parsed_data['car'] = outgauge_pack[1].decode('ascii').strip('\0') # Decode string byte
            parsed_data['flags'] = outgauge_pack[2]

            # Data yang relevan untuk haptics:
            parsed_data['gear'] = outgauge_pack[3]
            # outgauge_pack[4] adalah PLID (Player ID), tidak kita gunakan
            parsed_data['speed_mps'] = outgauge_pack[5] # Kecepatan dalam m/s (sebagai float)
            parsed_data['rpm_raw'] = outgauge_pack[6]   # RPM mentah (sebagai float)

            # Field lain yang Anda cantumkan (opsional untuk ditampilkan di debug)
            parsed_data['turbo'] = outgauge_pack[7]
            parsed_data['engtemp'] = outgauge_pack[8]
            parsed_data['fuel'] = outgauge_pack[9]
            parsed_data['oilpressure'] = outgauge_pack[10]
            parsed_data['oiltemp'] = outgauge_pack[11]
            parsed_data['dashlights'] = outgauge_pack[12]
            parsed_data['showlights'] = outgauge_pack[13]
            parsed_data['throttle'] = outgauge_pack[14]
            parsed_data['brake'] = outgauge_pack[15]
            parsed_data['clutch'] = outgauge_pack[16]
            parsed_data['display1'] = outgauge_pack[17].decode('ascii').strip('\0')
            parsed_data['display2'] = outgauge_pack[18].decode('ascii').strip('\0')

            # Konversi dan skala RPM
            # Jika 'rpm_raw' adalah float dan sudah dalam RPM, kita bisa langsung pakai.
            # Jika RPM Anda "1000" dan seharusnya 10000, maka perlu dikali 10
            # Jika "1000" dan itu sudah 1000, tidak perlu diubah.
            # Untuk amannya, kita asumsikan sudah dalam RPM yang sebenarnya.
            parsed_data['rpm'] = int(parsed_data['rpm_raw']) # Konversi ke int

            # --- DEBUGGING LENGKAP ---
            print(f"[{self.profile_name} Profile] Parsed OutGauge data:")
            print(f"  Speed: {parsed_data['speed_mps'] * 3.6:.2f} km/h (raw m/s: {parsed_data['speed_mps']:.2f})")
            print(f"  RPM: {parsed_data['rpm']} (raw: {parsed_data['rpm_raw']:.2f})")
            print(f"  Gear: {parsed_data['gear']}")
            print(f"  Throttle: {parsed_data['throttle']:.2f}, Brake: {parsed_data['brake']:.2f}, Clutch: {parsed_data['clutch']:.2f}")

            return parsed_data

        except struct.error as e:
            print(f"[{self.profile_name} Profile] ERROR: Struct unpack failed for OutGauge (format mismatch?): {e} - Raw len: {len(raw_data)}")
            print(f"Raw data hex: {raw_data.hex()}")
            return None
        except IndexError as e:
            print(f"[{self.profile_name} Profile] ERROR: Index out of bounds in OutGauge parsing: {e}")
            return None
        except Exception as e:
            print(f"[{self.profile_name} Profile] GENERAL PARSING ERROR for OutGauge: {e}")
            return None

    def _handle_haptics(self, data):
        current_time = time.time()
        should_vibrate = False

        if data is None:
            if self.vibration_active:
                self.bt_manager.send_command("STOP")
                self.vibration_active = False
            return

        # --- Pemicu Getaran Berdasarkan RPM Tinggi ---
        rpm_high_threshold = 7000 # Sesuaikan ambang batas ini sesuai keinginan Anda
        if 'rpm' in data and data['rpm'] > rpm_high_threshold:
            print(f"[{self.profile_name}] RPM Tinggi ({data['rpm']}) -> VIBRATE")
            should_vibrate = True
        
        # --- Pemicu Getaran Berdasarkan Ganti Gigi ---
        # Gear: 0=Netral, 1=Gigi 1, 2=Gigi 2, dst. Mundur biasanya 255 atau -1.
        if 'gear' in data and data['gear'] != self.last_gear:
            # Hindari getaran saat dari atau ke Netral/Mundur secara tidak sengaja jika tidak diinginkan
            # Jika Anda ingin getaran saat masuk netral juga, hapus data['gear'] != 0
            if data['gear'] != 0 and data['gear'] != 255: 
                print(f"[{self.profile_name}] Ganti Gigi ke {data['gear']} -> VIBRATE")
                should_vibrate = True
            # Jika gigi berubah ke 0 (Netral) atau 255 (Mundur) dari gigi maju, bisa juga pemicu
            elif (self.last_gear != 0 and self.last_gear != 255) and (data['gear'] == 0 or data['gear'] == 255):
                 print(f"[{self.profile_name}] Ganti Gigi ke Netral/Mundur ({data['gear']}) -> VIBRATE")
                 should_vibrate = True

        self.last_gear = data.get('gear', self.last_gear) # Selalu update last_gear

        # --- Pengiriman Perintah Getar atau Berhenti ---
        if should_vibrate:
            if not self.vibration_active:
                self.bt_manager.send_command("VIBRATE")
                self.vibration_active = True
                self.last_vibrate_time = current_time
        else:
            # Hentikan getaran setelah cooldown jika sudah tidak ada pemicu
            if self.vibration_active and (current_time - self.last_vibrate_time) > self.vibration_cooldown:
                self.bt_manager.send_command("STOP")
                self.vibration_active = False

    def stop(self):
        if self.running:
            print(f"[{self.profile_name} Profile] Stopping...")
            self.running = False
            if self.udp_socket:
                self.udp_socket.close()
            if self.listener_thread and self.listener_thread.is_alive():
                self.listener_thread.join(timeout=1) # Ber