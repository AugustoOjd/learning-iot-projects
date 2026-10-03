# Índice de proyectos

Los nueve casos de uso del laboratorio. La numeración sigue la semana del
[roadmap](../roadmap_v2_kit.md), con huecos donde la semana no produce firmware propio.

🔵 Arduino (C++) · 🐍 MicroPython

| # | Proyecto | Semana | Lenguaje | Técnica central | Estado |
|---|---|---|---|---|---|
| **s01** | [Panel de alarma](s01-panel-alarma/index.md) | 1 | 🔵🐍 | Máquina de estados sin bloqueo | ✅ completado |
| **s02** | [Monitor de umbrales](s02-monitor-umbrales/index.md) | 2 | 🐍 | ADC, divisor de tensión, histéresis | ⬜ |
| **s03** | [Telemetría a la nube](s03-telemetria-nube/index.md) | 3 | 🔵🐍 | WiFi + MQTT + LWT | ⬜ |
| **s04** | [Datalogger de frío](s04-datalogger-frio/index.md) | 4 | 🔵 | I2C, NVS, store-and-forward | ⬜ |
| **s05** | [Control de tanque](s05-control-tanque/index.md) | 5 | 🔵 | Actuadores con fallas seguras | ⬜ |
| **s06** | [Control de acceso](s06-control-acceso/index.md) | 6 | 🔵 | SPI, lógica crítica local | ⬜ |
| **s07** | [Panel indicador](s07-panel-indicador/index.md) | 7 | 🔵 | Expansión de I/O, multiplexado | ⬜ |
| **s09** | [Nodo a batería](s09-nodo-bateria/index.md) | 9 | 🔵🐍 | Deep sleep, presupuesto energético | ⬜ |
| **s11** | [Red multi-nodo](s11-red-multinodo/index.md) | 11 | 🔵 | ESP-NOW, topología gateway | ⬜ |

**Semanas sin carpeta:** la 8 (robustez: FreeRTOS, watchdog, backoff) y la 10 (OTA y TLS)
endurecen el código de [`shared/`](../shared/). La 12 le da gabinete al proyecto elegido.

**Extensiones fuera del roadmap base:** Modbus, LoRaWAN y TinyML en
[`docs/extensiones.md`](../docs/extensiones.md).

---

## Acceso directo

### s01 — Panel de alarma
Detector de incendio con sirena y luces.
[**índice**](s01-panel-alarma/index.md) · [README](s01-panel-alarma/README.md) ·
[**Instrucciones físicas**](s01-panel-alarma/INSTRUCCIONES_FISICAS.md) ·
[🔵 código](s01-panel-alarma/arduino/src/main.cpp) ·
[🐍 código](s01-panel-alarma/micropython/main.py)

### s02 — Monitor de umbrales
Sala de servidores o heladera de farmacia.
[**índice**](s02-monitor-umbrales/index.md) · [README](s02-monitor-umbrales/README.md) ·
instrucciones físicas ⬜ ·
[🐍 código](s02-monitor-umbrales/micropython/)

### s03 — Telemetría a la nube
El dato en un gráfico que abrís desde el celular. **Hito: a partir de acá todo se enchufa acá.**
[**índice**](s03-telemetria-nube/index.md) · [README](s03-telemetria-nube/README.md) ·
instrucciones físicas ⬜ ·
[🔵 código](s03-telemetria-nube/arduino/) ·
[🐍 código](s03-telemetria-nube/micropython/)

### s04 — Datalogger de cadena de frío
Registro con hora real que sigue funcionando sin internet.
[**índice**](s04-datalogger-frio/index.md) · [README](s04-datalogger-frio/README.md) ·
instrucciones físicas ⬜ ·
[🔵 código](s04-datalogger-frio/arduino/)

### s05 — Control de tanque
Bomba de agua automática y persiana motorizada.
[**índice**](s05-control-tanque/index.md) · [README](s05-control-tanque/README.md) ·
instrucciones físicas ⬜ ·
[🔵 código](s05-control-tanque/arduino/)

### s06 — Control de acceso
Fichaje RFID de oficina o gimnasio.
[**índice**](s06-control-acceso/index.md) · [README](s06-control-acceso/README.md) ·
instrucciones físicas ⬜ ·
[🔵 código](s06-control-acceso/arduino/)

### s07 — Panel indicador
Tablero de estado industrial.
[**índice**](s07-panel-indicador/index.md) · [README](s07-panel-indicador/README.md) ·
instrucciones físicas ⬜ ·
[🔵 código](s07-panel-indicador/arduino/)

### s09 — Nodo a batería
Sensor en un lugar sin enchufe cerca.
[**índice**](s09-nodo-bateria/index.md) · [README](s09-nodo-bateria/README.md) ·
instrucciones físicas ⬜ ·
[🔵 código](s09-nodo-bateria/arduino/) ·
[🐍 código](s09-nodo-bateria/micropython/)

### s11 — Red multi-nodo
Sensores dispersos en una casa o un campo. Dos binarios distintos.
[**índice**](s11-red-multinodo/index.md) · [README](s11-red-multinodo/README.md) ·
instrucciones físicas ⬜ ·
[🔵 nodo sensor](s11-red-multinodo/nodo-sensor/arduino/) ·
[🔵 gateway](s11-red-multinodo/gateway/arduino/)

---

## Los tres puntos de comparación entre lenguajes

Hacer el mismo proyecto dos veces no es redundancia: cada par mide algo distinto.

| | Qué compara |
|---|---|
| **s01** | Sintaxis y ciclo de desarrollo, con hardware simple que no distrae |
| **s03** | El stack de red: `PubSubClient` vs `umqtt.simple`, JSON, reconexión |
| **s09** | **Consumo medido con el multímetro.** MicroPython arranca más lento y eso cuesta meses de autonomía. Un número, no una opinión |

En **s07 MicroPython directamente no puede**: el multiplexado necesita refrescar 8 filas a
más de 60 Hz y el intérprete no llega.

## Estructura de cada proyecto

| Archivo | Para qué |
|---|---|
| `index.md` | Punto de entrada: por dónde empezar y checklist de cierre |
| `README.md` | Caso real, técnica, dónde más se aplica, criterio de terminado |
| `INSTRUCCIONES_FISICAS.md` | Componentes, cómo se ven, cómo se conectan, en qué orden |
| `arduino/` · `micropython/` | El código |
| `media/` | Foto y video — **antes de desarmar** |

## Navegación

[⬅ README del repo](../README.md) ·
[Mapa de transferencia](../docs/patrones.md) ·
[Inventario del kit](../docs/inventario.md) ·
[Extensiones](../docs/extensiones.md) ·
[Infraestructura](../infra/README.md)
