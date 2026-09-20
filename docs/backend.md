# Backend: puntos de conexión (fuera de alcance por ahora)

El trabajo de servidor queda **fuera del roadmap de 12 semanas** a propósito: es tu zona de
confort y el objetivo de estas semanas es el hardware. Pero conviene dejar documentado por
dónde se conecta, para que el día que quieras agregarlo no haya que rediseñar nada.

## La frontera es el broker

Todo lo que corre en el servidor se conecta en un solo punto: **se suscribe a MQTT**. El
firmware nunca sabe que el backend existe, y esa independencia es deliberada.

```
ESP32 ──MQTT──> Mosquitto ──┬──> Node-RED        (s03: dashboard rápido)
                            ├──> Telegraf → InfluxDB → Grafana   (s12)
                            └──> [tu servicio]   ← acá enchufa Python o Go
```

Por qué importa que la frontera sea el broker: podés agregar, reemplazar o romper el backend
sin tocar una línea de firmware ni volver a flashear 20 dispositivos.

## El contrato son los topics

Esto es lo único que hay que definir bien **ahora**, porque cambiarlo después implica
reflashear. Esquema sugerido:

```
casa/<zona>/telemetria      → el dispositivo publica lecturas
casa/<zona>/estado          → online/offline (retained, vía LWT)
casa/<zona>/comando         → el dispositivo se suscribe
acceso/eventos              → fichajes (s06)
acceso/alta                 → alta de tarjetas por MQTT (s06)
campo/nodo<N>/telemetria    → nodos vía gateway ESP-NOW (s11)
```

Dos reglas que evitan dolor:

- **Un topic por dispositivo, nunca compartido.** Permite ACLs en el broker: cada sensor
  publica solo en el suyo. Si uno se compromete, no puede falsear a los demás.
- **Payload JSON con campos fijos.** Incluí siempre `heap`, `rssi` y `uptime`: son los que
  te dejan diagnosticar a distancia (s03, s08).

## Qué haría el servicio

Lo que ni Node-RED ni Grafana cubren bien:

| Responsabilidad | Por qué no alcanza con Node-RED |
|---|---|
| **Validar payloads** | Un dispositivo con firmware viejo manda un campo roto y te ensucia la serie histórica |
| **Persistir con esquema** | Timescale/Influx con retención y downsampling pensados |
| **API de consulta** | Para una app propia, no solo un dashboard |
| **Alertas con lógica real** | "Tres lecturas altas en 10 minutos Y el dispositivo online" |
| **Gestión de flota** | Alta de dispositivos, rotación de credenciales, estado de firmware |
| **Alta de tarjetas (s06)** | El endpoint que publica en `acceso/alta` |

## Python vs Go

| | Python (FastAPI + paho-mqtt) | Go (paho.mqtt.golang) |
|---|---|---|
| Velocidad de desarrollo | Más rápido | Más verboso |
| Ecosistema de datos | Pandas, análisis, ML | Más pobre |
| Despliegue | Necesita intérprete y entorno | **Un binario único, sin dependencias** |
| Concurrencia | Asyncio, aceptable | Goroutines, excelente |
| Memoria | ~80 MB | ~15 MB |
| Cuándo | Backend, análisis, prototipado | **Gateway en una Raspberry**, alta concurrencia |

El criterio práctico: **Python para el backend, Go si el servicio va a correr en el borde.**
Un binario de Go en una Raspberry Pi sin runtime ni dependencias es mucho más fácil de
mantener en un tablero industrial que un entorno de Python.

## Cuándo hace falta de verdad

Probablemente no todavía. Para las 12 semanas, **Node-RED (s03) + Grafana (s12) alcanzan** y
te dejan concentrarte en el hardware.

El servicio propio se justifica cuando aparece alguna de estas:

- Más de ~5 dispositivos con gestión de altas y credenciales
- Necesitás una API para una app, no solo un dashboard
- Las alertas necesitan lógica que no entra en un nodo de Node-RED
- Querés correr análisis o ML sobre el histórico

## Si lo agregás

Iría como `backend/` en la raíz, sin tocar `firmware/`:

```
backend/
├── pyproject.toml
├── src/
│   ├── main.py          # FastAPI
│   ├── mqtt_client.py   # suscriptor, valida y persiste
│   ├── models.py        # Pydantic: el esquema del payload
│   └── db.py            # Timescale
└── tests/
```

Son unas 150 líneas para la versión útil. El valor no está en el código —eso ya lo sabés
hacer— sino en que el sistema quede completo de punta a punta, que es lo que lo convierte
en "diseñé un sistema IoT" en vez de "hice un proyecto de Arduino".

## Relacionado

- [`docs/extensiones.md`](extensiones.md) — un gateway Modbus también es un buen candidato a
  escribirse en Go
- [`infra/`](../infra/) — el broker y el stack de datos que ya vas a tener corriendo
