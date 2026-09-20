#pragma once

// Copiá este archivo como secrets.h y completalo.
//   cp shared/config/secrets.example.h shared/config/secrets.h
// secrets.h está en .gitignore y no debe commitearse nunca.
//
// Desde la semana 10 esto se reemplaza por credenciales en NVS vía WiFiManager,
// para que el mismo binario sirva en todos los dispositivos.

#define WIFI_SSID       "TU_RED"
#define WIFI_PASSWORD   "TU_PASSWORD"

#define MQTT_HOST       "192.168.1.100"   // IP del broker en tu LAN (ver infra/README.md si estás en WSL2)
#define MQTT_PORT       1883              // 8883 con TLS desde la semana 10
#define MQTT_USER       ""
#define MQTT_PASSWORD   ""

#define OTA_PASSWORD    "cambiar-esto"    // semana 10
