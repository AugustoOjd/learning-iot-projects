# s11 — Red multi-nodo

> **Semana 11** · 🔵 Arduino (C++) · Estado: ⬜ sin empezar

Cinco sensores en una casa o un campo, donde no todos llegan al WiFi. Los nodos despiertan
5 ms, mandan y duermen: duran años. El gateway está enchufado y traduce a MQTT.

**Técnica central:** ESP-NOW y topología gateway + nodos dormidos.

> ⚠️ Este proyecto tiene **dos binarios distintos** y necesita **dos ESP32** (el segundo es
> compra extra, ~$10).

---

## Por dónde empezar

1. **[README.md](README.md)** — el caso real, la técnica y el criterio de terminado
2. **INSTRUCCIONES_FISICAS.md** — se escribe al llegar a esta semana ⬜
3. **El código** — primero el [🔵 gateway](gateway/arduino/), después el [🔵 nodo sensor](nodo-sensor/arduino/)
4. **[media/](media/)** — foto y video **antes de desarmar**
5. **Cerrar** — las tareas de abajo

El orden importa: el nodo necesita la **MAC del gateway** hardcodeada, así que el gateway
tiene que existir primero. Anotala en [`docs/inventario.md`](../../docs/inventario.md).

## Archivos de esta carpeta

| Archivo | Para qué | Estado |
|---|---|---|
| [`README.md`](README.md) | Caso real, dónde más se aplica, criterio de terminado | |
| `INSTRUCCIONES_FISICAS.md` | Componentes, cómo se ven, cómo se conectan | ⬜ pendiente |
| [`gateway/`](gateway/arduino/) | Enchufado. Recibe ESP-NOW y republica en MQTT | |
| [`nodo-sensor/`](nodo-sensor/arduino/) | A batería. Despierta, manda y duerme | |
| [`media/`](media/) | Foto del cableado y video de 20s | ⬜ |

## La trampa de esta semana

ESP-NOW y WiFi **comparten la misma radio**, así que el gateway tiene que estar en el **mismo
canal** que tu router. Si no coinciden, los paquetes se pierden **en silencio**: sin error,
sin log, sin nada. Es el bug más frustrante de ESP-NOW.

Fijá el canal en el router, o leelo con `WiFi.channel()` y configurá los nodos igual.

## Antes de desarmar

- [ ] Foto del cableado de los dos nodos en [`media/`](media/)
- [ ] Video de 20 segundos con datos llegando al dashboard
- [ ] Tabla de componentes del [README](README.md) completa

## Al cerrar el proyecto

- [ ] Sección "Dónde más se usa este patrón" del [README](README.md)
- [ ] Fila nueva en [`docs/patrones.md`](../../docs/patrones.md)
- [ ] MACs y canal WiFi en [`docs/inventario.md`](../../docs/inventario.md)
- [ ] Autonomía calculada en [`hardware/mediciones/`](../../hardware/mediciones/)
- [ ] Estado actualizado acá, en [`firmware/index.md`](../index.md) y en el [README raíz](../../README.md)

## Siguiente paso natural

La misma arquitectura a escala de kilómetros es **LoRaWAN** — ver
[`docs/extensiones.md`](../../docs/extensiones.md).

## Navegación

[⬅ Índice de proyectos](../index.md) ·
[Pinout](../../shared/config/pinout.h) ·
[Roadmap, semana 11](../../roadmap_v2_kit.md) ·
[Mapa de transferencia](../../docs/patrones.md)
