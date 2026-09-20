"""Copiá este archivo como secrets.py y completalo.

    cp shared/config/secrets.example.py shared/config/secrets.py
    mpremote cp shared/config/secrets.py :

secrets.py está en .gitignore y no debe commitearse nunca.
"""

WIFI_SSID = "TU_RED"
WIFI_PASSWORD = "TU_PASSWORD"

MQTT_HOST = "192.168.1.100"   # IP del broker en tu LAN (ver infra/README.md si estás en WSL2)
MQTT_PORT = 1883              # 8883 con TLS
MQTT_USER = ""
MQTT_PASSWORD = ""
