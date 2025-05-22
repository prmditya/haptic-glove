package com.example.examplemod;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import net.minecraft.world.entity.player.Player;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.entity.living.LivingHurtEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import java.util.concurrent.CompletableFuture;

@Mod("hapticmod")
public class ExampleMod {

  public ExampleMod() { MinecraftForge.EVENT_BUS.register(this); }

    @SubscribeEvent
    public void onPlayerDamaged(LivingHurtEvent event) {
      if (event.getEntity() instanceof Player player && !player.level().isClientSide()) {
          System.out.println("Player terkena damage! Mengirim sinyal ke glove...");
          CompletableFuture.runAsync(this::sendSignalToESP);
      }
    }

  private void sendSignalToESP() {
    try {
      URL url = new URL(Config.ESP8266_DNS + Config.VIBRATE_ENDPOINT);
      HttpURLConnection connection = (HttpURLConnection)url.openConnection();
      connection.setRequestMethod("GET");
      int responseCode = connection.getResponseCode();
      System.out.println("HTTP Response: " + responseCode);
    } catch (IOException e) {
      System.err.println("Gagal kirim sinyal ke ESP32: " + e.getMessage());
    }
  }
}