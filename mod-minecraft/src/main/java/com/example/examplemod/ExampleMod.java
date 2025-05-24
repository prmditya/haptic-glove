// Referensi: https://mcforge.readthedocs.io/en/latest/events/events/
// atau https://fabricmc.net/wiki/tutorial:events

package com.example.examplemod; // Pastikan package ini sesuai dengan struktur folder Anda

import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod.EventBusSubscriber.Bus;
import net.minecraft.world.entity.player.Player; // Perubahan: PlayerEntity sekarang Player di 1.20.x
import net.minecraft.world.damagesource.DamageSource; // Perubahan: Lokasi DamageSource
import net.minecraftforge.event.entity.living.LivingDamageEvent;
import net.minecraftforge.event.level.ExplosionEvent; // Perubahan: Lokasi ExplosionEvent
import net.minecraft.world.phys.Vec3; // Perubahan: Vec3d sekarang Vec3 dan lokasi paketnya

import java.net.DatagramSocket;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.io.IOException;

@Mod(ExampleMod.MODID) // Menggunakan konstanta MODID dari kelas ini sendiri
@Mod.EventBusSubscriber(modid = ExampleMod.MODID, bus = Bus.FORGE)
public class ExampleMod {

    public static final String MODID = "examplemod"; // Sesuaikan MODID dengan nama yang Anda inginkan, tapi pastikan ini yang di build.gradle

    private static final String PYTHON_HOST = "127.0.0.1";
    private static final int PYTHON_PORT = 12345;

    public ExampleMod() {
        System.out.println("HapticMod for Minecraft initialized!");
    }

    // Event saat entitas (termasuk pemain) menerima kerusakan
    @SubscribeEvent
    public static void onLivingDamage(LivingDamageEvent event) {
        if (Player.class.isInstance(event.getEntity())) {
            sendUdpMessage("HIT"); // Kirim "HIT" untuk getaran statis
            System.out.println("[HapticMod] Player took damage!"); // Debug di console game
        }
    }

    @SubscribeEvent
    public static void onExplosion(ExplosionEvent.Detonate event) {
        sendUdpMessage("EXPLOSION"); // Kirim "EXPLOSION"
        System.out.println("[HapticMod] Explosion detected!"); // Debug
    }

    // Fungsi untuk mengirim pesan UDP
    private static void sendUdpMessage(String message) {
        try (DatagramSocket socket = new DatagramSocket()) {
            byte[] buffer = message.getBytes();
            InetAddress address = InetAddress.getByName(PYTHON_HOST);
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length, address, PYTHON_PORT);
            socket.send(packet);
        } catch (IOException e) {
            // e.printStackTrace(); // Cetak error penuh untuk debugging
            System.err.println("[HapticMod] Failed to send UDP message from Minecraft: " + e.getMessage());
        }
    }
}