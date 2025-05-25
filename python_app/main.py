import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

from bluetooth_manager import BluetoothManager
from game_profiles.minecraft_profile import MinecraftProfile
from game_profiles.lfs_profile import LFSProfile

class HapticGloveAppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Haptic Glove Control")
        self.geometry("400x300")

        self.bt_manager = BluetoothManager(device_name="HapticGlove_Static")
        self.active_profile = None
        self.profiles = {
            "Minecraft": MinecraftProfile,
            "Life for Speed": LFSProfile,
        }

        self._create_widgets()
        self._connect_bluetooth_on_start()

        # Pastikan Bluetooth terputus saat jendela ditutup
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_widgets(self):
        # Frame untuk koneksi Bluetooth
        bt_frame = ttk.LabelFrame(self, text="Bluetooth Connection")
        bt_frame.pack(padx=10, pady=10, fill="x")

        self.bt_status_label = ttk.Label(bt_frame, text="Status: Disconnected")
        self.bt_status_label.pack(pady=5)

        self.connect_button = ttk.Button(bt_frame, text="Connect Bluetooth", command=self._connect_bluetooth)
        self.connect_button.pack(pady=5)

        # Frame untuk pemilihan Game Profile
        game_frame = ttk.LabelFrame(self, text="Game Profiles")
        game_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.profile_var = tk.StringVar(self)
        self.profile_var.set("Select a Game") # Nilai default

        profile_options = list(self.profiles.keys())
        self.profile_dropdown = ttk.OptionMenu(game_frame, self.profile_var, "Select a Game", *profile_options, command=self._on_profile_selected)
        self.profile_dropdown.pack(pady=5)

        self.start_profile_button = ttk.Button(game_frame, text="Start Profile", command=self._start_profile, state=tk.DISABLED)
        self.start_profile_button.pack(pady=5)

        self.stop_profile_button = ttk.Button(game_frame, text="Stop Profile", command=self._stop_profile, state=tk.DISABLED)
        self.stop_profile_button.pack(pady=5)
        
        self.current_profile_label = ttk.Label(game_frame, text="Active Profile: None")
        self.current_profile_label.pack(pady=5)

    def _connect_bluetooth_on_start(self):
        # Coba konek Bluetooth di thread terpisah agar UI tidak freeze
        threading.Thread(target=self._connect_bluetooth, daemon=True).start()

    def _connect_bluetooth(self):
        self.bt_status_label.config(text="Status: Connecting...")
        self.connect_button.config(state=tk.DISABLED) # Disable tombol saat mencoba konek

        if self.bt_manager.connect():
            self.bt_status_label.config(text="Status: Connected!")
            self.connect_button.config(text="Reconnect Bluetooth") # Ubah teks tombol
            self.start_profile_button.config(state=tk.NORMAL) # Aktifkan tombol start profile
        else:
            self.bt_status_label.config(text="Status: Failed to Connect!")
            messagebox.showerror("Connection Error", "Could not connect to ESP32. Check if it's paired and powered on.")
        
        self.connect_button.config(state=tk.NORMAL) # Aktifkan kembali tombol

    def _on_profile_selected(self, selected_profile_name):
        # Aktifkan tombol Start Profile jika Bluetooth sudah terkoneksi
        if self.bt_manager.ser and self.bt_manager.ser.is_open:
            self.start_profile_button.config(state=tk.NORMAL)
        else:
            self.start_profile_button.config(state=tk.DISABLED)
        self.stop_profile_button.config(state=tk.DISABLED) # Pastikan tombol stop dinonaktifkan

    def _start_profile(self):
        profile_name = self.profile_var.get()
        if profile_name == "Select a Game":
            messagebox.showwarning("Selection Error", "Please select a game profile first.")
            return

        if self.active_profile:
            messagebox.showwarning("Profile Active", f"'{self.current_profile_label.cget('text').replace('Active Profile: ', '')}' is already running. Please stop it first.")
            return

        ProfileClass = self.profiles.get(profile_name)
        if ProfileClass:
            print(f"Starting {profile_name} profile...")
            self.active_profile = ProfileClass(self.bt_manager)
            self.active_profile.start()
            
            self.current_profile_label.config(text=f"Active Profile: {profile_name}")
            self.start_profile_button.config(state=tk.DISABLED)
            self.stop_profile_button.config(state=tk.NORMAL)
            messagebox.showinfo("Profile Started", f"'{profile_name}' profile is now active. Start playing the game!")
        else:
            messagebox.showerror("Error", "Invalid profile selected.")

    def _stop_profile(self):
        if self.active_profile:
            print(f"Stopping active profile...")
            self.active_profile.stop()
            self.active_profile = None
            self.current_profile_label.config(text="Active Profile: None")
            self.stop_profile_button.config(state=tk.DISABLED)
            # Aktifkan kembali tombol start jika BT masih terkoneksi
            if self.bt_manager.ser and self.bt_manager.ser.is_open:
                self.start_profile_button.config(state=tk.NORMAL)
            messagebox.showinfo("Profile Stopped", "Current profile has been stopped.")
        else:
            messagebox.showinfo("No Profile Active", "No game profile is currently active.")

    def _on_closing(self):
        if self.active_profile:
            self.active_profile.stop()
        if self.bt_manager:
            self.bt_manager.disconnect()
        self.destroy() # Tutup jendela Tkinter

if __name__ == "__main__":
    app = HapticGloveAppGUI()
    app.mainloop()