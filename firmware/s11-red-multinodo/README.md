# Red multi-nodo

> **Semana 11** del [roadmap](../../roadmap_v2_kit.md) · Estado: ⬜ sin empezar
> **Framework:** 🔵 Arduino (C++)

Dos binarios distintos: [`nodo-sensor/`](nodo-sensor/) duerme y transmite,
[`gateway/`](gateway/) está enchufado y traduce ESP-NOW a MQTT.

Arduino por madurez de la API de ESP-NOW. MicroPython tiene el módulo `espnow` y funciona,
pero el nodo va a batería y acá el tiempo de arranque del intérprete se paga en autonomía
(lo vas a haber medido en s09).

## Caso real

Cinco sensores en una casa o un campo, donde no todos llegan al WiFi. Los nodos despiertan
5 ms, mandan y duermen: duran años. El gateway está enchufado y mantiene WiFi permanente.

Esta topología es la respuesta correcta al 80% de los proyectos IoT reales y no aparece en
ningún roadmap de principiante.

## Dónde más se usa este patrón

_(Completar al terminar, y agregar la fila en [`docs/patrones.md`](../../docs/patrones.md).)_

-
-
-

## Técnica central

ESP-NOW y topología gateway + nodos dormidos.

## Cómo lo reconstruyo

**Componentes:** 2× ESP32 (uno es compra extra, ~$10), sensores de las semanas anteriores,
divisor de tensión con 2× 10K para medir batería.

| Componente | Pin | Nota |
|---|---|---|
| | | |

⚠️ **La trampa**: ESP-NOW y WiFi comparten radio, así que el gateway tiene que estar en el
**mismo canal** que tu router. Si no coinciden, los paquetes se pierden en silencio — sin
error, sin nada. Anotá el canal en [`docs/inventario.md`](../../docs/inventario.md).

📷 Foto del cableado y video de 20s en [`media/`](media/) — **sacalos antes de desarmar.**

## Criterio de terminado

- [ ] Dos nodos mandando por ESP-NOW al gateway
- [ ] El gateway los reenvía a MQTT y aparecen en el dashboard
- [ ] Los nodos duermen entre envíos y calculaste su autonomía
- [ ] Alerta de batería baja funcionando
- [ ] Entendés por qué los canales tienen que coincidir
- [ ] Foto y video en `media/` antes de desarmar
- [ ] Fila agregada en `docs/patrones.md`

## Siguiente paso natural

La misma arquitectura a escala de kilómetros es LoRaWAN — ver
[`docs/extensiones.md`](../../docs/extensiones.md).

## Qué me costó

_(Lo que falló, cuánto tardé, qué lo resolvió.)_
