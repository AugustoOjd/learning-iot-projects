# Infraestructura

```bash
cd infra && docker compose up -d
```

| Servicio | Puerto | Desde | Para qué |
|---|---|---|---|
| Mosquitto | 1883 · 9001 · 8883 | s03 | Broker MQTT |
| Node-RED | [1880](http://localhost:1880) | s03 | Dashboard rápido, flow visual |
| InfluxDB | 8086 | s12 | Series temporales (comentado) |
| Grafana | [3000](http://localhost:3000) | s12 | Gráficos (comentado) |

Probar que el broker anda, sin el ESP32:

```bash
docker exec -it mosquitto mosquitto_sub -t 'casa/#' -v
docker exec -it mosquitto mosquitto_pub -t 'casa/sala/telemetria' -m '{"temp":22.5}'
```

---

## ⚠️ WSL2: el ESP32 no va a poder conectarse (y no es tu firmware)

Estás en WSL2, que por defecto corre detrás de NAT: la IP que ves dentro de WSL **no es una
IP de tu red local**, así que el ESP32 no puede alcanzarla. Vas a ver timeouts de conexión
MQTT y vas a culpar al código.

Primero, confirmá el síntoma:

```bash
hostname -I              # IP de WSL, típicamente 172.x.x.x  ← el ESP32 NO la alcanza
# En PowerShell de Windows:
#   ipconfig              → la IP 192.168.x.x de tu PC es la que necesitás
```

### Opción A — Networking en modo espejo (recomendado)

Windows 11 22H2+. Crear o editar `C:\Users\<vos>\.wslconfig`:

```ini
[wsl2]
networkingMode=mirrored
```

Después `wsl --shutdown` en PowerShell y volver a abrir. WSL pasa a compartir la interfaz de
red de Windows: la IP de tu PC llega directo al broker y `MQTT_HOST` es esa IP.

### Opción B — Port proxy (si estás en Windows 10)

En PowerShell **como administrador**:

```powershell
netsh interface portproxy add v4tov4 `
  listenport=1883 listenaddress=0.0.0.0 `
  connectport=1883 connectaddress=(wsl hostname -I).Trim()

New-NetFirewallRule -DisplayName "MQTT 1883" -Direction Inbound `
  -LocalPort 1883 -Protocol TCP -Action Allow
```

Ojo: la IP de WSL **cambia en cada reinicio**, así que el portproxy hay que rehacerlo. Es la
razón principal para preferir la opción A.

### Opción C — Broker público, solo para probar

`broker.hivemq.com:1883`. Sin instalar nada, pero **todo tu tráfico es público**: cualquiera
puede leer tus datos y publicar comandos falsos. Solo para el primer "¿llega el mensaje?".

### Verificación

Desde otra máquina de tu red (o el celular con una app MQTT), suscribite a `casa/#` usando la
IP **de Windows**. Si ves mensajes, el ESP32 también va a poder.
