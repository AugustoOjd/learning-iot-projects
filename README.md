# Laboratorio IoT — ESP32

Nueve casos de uso sobre un NodeMCU ESP-32S y el kit HEMMEL TEK-002, siguiendo
[`roadmap_v2_kit.md`](roadmap_v2_kit.md). No son ejercicios sueltos: comparten esqueleto
(`shared/`) y todos se enchufan al pipeline de telemetría que nace en s03.

**Dos lenguajes a propósito**: Arduino (C++) y MicroPython, con tres proyectos hechos en
ambos para poder compararlos de verdad.

## Casos de uso

| # | Proyecto | Caso real | Técnica central | Lenguaje | Estado |
|---|---|---|---|---|---|
| s01 | [Panel de alarma](firmware/s01-panel-alarma/) | Detector de incendio con sirena | Máquina de estados sin bloqueo | 🔵🐍 | ⬜ |
| s02 | [Monitor de umbrales](firmware/s02-monitor-umbrales/) | Sala de servidores / heladera de farmacia | ADC, divisor de tensión, histéresis | 🐍 | ⬜ |
| s03 | [Telemetría a la nube](firmware/s03-telemetria-nube/) | Monitoreo remoto | WiFi + MQTT + LWT | 🔵🐍 | ⬜ |
| s04 | [Datalogger de frío](firmware/s04-datalogger-frio/) | Cadena de frío con hora real | I2C, NVS, store-and-forward | 🔵 | ⬜ |
| s05 | [Control de tanque](firmware/s05-control-tanque/) | Bomba de agua + persiana | Actuadores con fallas seguras | 🔵 | ⬜ |
| s06 | [Control de acceso](firmware/s06-control-acceso/) | Fichaje RFID de oficina | SPI, lógica crítica local | 🔵 | ⬜ |
| s07 | [Panel indicador](firmware/s07-panel-indicador/) | Tablero industrial | Expansión de I/O, multiplexado | 🔵 | ⬜ |
| s09 | [Nodo a batería](firmware/s09-nodo-bateria/) | Sensor sin enchufe cerca | Deep sleep, presupuesto energético | 🔵🐍 | ⬜ |
| s11 | [Red multi-nodo](firmware/s11-red-multinodo/) | Sensores dispersos en campo | ESP-NOW, topología gateway | 🔵 | ⬜ |

🔵 Arduino (C++) · 🐍 MicroPython

Las semanas 8, 10 y 12 no tienen carpeta: la 8 (robustez) y la 10 (OTA/TLS) endurecen el
código de `shared/`, y la 12 le da gabinete al proyecto que más te haya enganchado.

### Por qué cada proyecto está en el lenguaje que está

**Los tres con ambos** son puntos de comparación deliberados:

| | Qué compara |
|---|---|
| **s01** | Sintaxis y ciclo de desarrollo, con hardware simple que no distrae |
| **s03** | El stack de red: `PubSubClient` vs `umqtt.simple`, JSON, reconexión |
| **s09** | **Consumo medido con el multímetro.** MicroPython arranca más lento y eso se traduce en menos meses de autonomía. Un número, no una opinión |

**s02 en MicroPython** porque el REPL es ideal para calibrar umbrales en vivo sin recompilar.

**s04-s07 y s11 en Arduino** por madurez de librerías (RC522, RTClib, LCD I2C) y por timing.
En **s07 MicroPython directamente no puede**: el multiplexado necesita refrescar 8 filas a
más de 60 Hz y el intérprete no llega — la matriz parpadea visiblemente.

## Mapa de transferencia

👉 **[`docs/patrones.md`](docs/patrones.md)** — el índice inverso: qué técnica aprendiste y
en qué otros dominios se aplica. Es lo que hace que esto sea aprendizaje transferible y no
nueve demos.

## Cómo compilar

### Arduino — requiere [PlatformIO](https://platformio.org/install/cli)

```bash
cd firmware/s01-panel-alarma/arduino
pio run -t upload && pio device monitor
```

### MicroPython — requiere `esptool` y `mpremote`

```bash
pip install esptool mpremote

# Una sola vez por chip: flashear el intérprete
esptool.py --chip esp32 erase_flash
esptool.py --chip esp32 write_flash -z 0x1000 ESP32_GENERIC-*.bin

# Por proyecto
cd firmware/s01-panel-alarma/micropython
mpremote cp ../../../shared/config/pinout.py :
mpremote cp main.py : + repl
```

Antes de cualquier proyecto con red, copiá los secretos (ambos están en `.gitignore`):

```bash
cp shared/config/secrets.example.h  shared/config/secrets.h
cp shared/config/secrets.example.py shared/config/secrets.py
```

## Infraestructura

Broker MQTT, Node-RED y Grafana en [`infra/`](infra/). Desde s03: `cd infra && docker compose up -d`

## Antes de empezar

- [ ] Leer "Antes de enchufar nada" del roadmap (las 6 reglas que evitan quemar componentes)
- [ ] Completar [`docs/inventario.md`](docs/inventario.md) — variantes de tu kit, 20 minutos
- [ ] Conseguir un multímetro

## Documentación

| Archivo | Para qué |
|---|---|
| [`docs/patrones.md`](docs/patrones.md) | Técnica → dónde más se usa |
| [`docs/extensiones.md`](docs/extensiones.md) | **Modbus, LoRaWAN y TinyML**: casos, usos y cuándo valen la pena |
| [`docs/backend.md`](docs/backend.md) | Go/Python: puntos de conexión (fuera de alcance por ahora) |
| [`docs/decisiones.md`](docs/decisiones.md) | Por qué elegí cada cosa |
| [`docs/inventario.md`](docs/inventario.md) | Los datos únicos de tu kit: direcciones I2C, UIDs, variantes |
| [`hardware/mediciones/`](hardware/mediciones/) | Consumos medidos, presupuesto energético |
