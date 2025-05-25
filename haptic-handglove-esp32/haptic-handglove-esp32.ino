#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#define VIBRATOR_PIN LED_BUILTIN

const char* authToken = "A7b9!kL3@mN5#pQ8$sT2";

// Daftar SSID dan password
const char* ssids[]     = { "HIFI", "thokayna", "haptic" };
const char* passwords[] = { "11223344", "hasnakamila", "12345678" };
const int networkCount = sizeof(ssids) / sizeof(ssids[0]);

ESP8266WebServer server(80);

void handleVibrate() {
  if (server.header("Authorization") != authToken) {
    server.send(401, "text/plain", "Token Invalid");
    return;
  }

  digitalWrite(VIBRATOR_PIN, LOW);
  delay(500);
  digitalWrite(VIBRATOR_PIN, HIGH);
  server.send(200, "text/plain", "Vibration Triggered");
}

bool connectToWiFi() {
  for (int i = 0; i < networkCount; i++) {
    Serial.printf("Mencoba connect ke SSID: %s\n", ssids[i]);
    WiFi.begin(ssids[i], passwords[i]);

    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 10) {
      delay(500);
      Serial.print(".");
      attempts++;
    }

    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("\nBerhasil connect!");
      Serial.print("IP Address: ");
      Serial.println(WiFi.localIP());
      return true;
    } else {
      Serial.println("\nGagal connect, coba SSID berikutnya...");
    }
  }

  Serial.println("Tidak ada WiFi yang bisa dikoneksi.");
  return false;
}

void setup() {
  pinMode(VIBRATOR_PIN, OUTPUT);
  digitalWrite(VIBRATOR_PIN, HIGH);  // Nonaktifkan vibrator saat start

  Serial.begin(115200);
  delay(1000); // beri waktu serial ready

  connectToWiFi();

  if (WiFi.status() == WL_CONNECTED) {
    if (MDNS.begin("hapticmod")) {
      Serial.println("mDNS responder started! Akses via: http://hapticmod.local");
    }

    server.on("/vibrate", handleVibrate);
    server.begin();
    Serial.println("HTTP server started");
  }
}

void loop() {
  server.handleClient();
  MDNS.update();
}
