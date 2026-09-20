# Nodo a batería

> **Semana 9** del [roadmap](../../roadmap_v2_kit.md) · Estado: ⬜ sin empezar
> **Framework:** 🔵 Arduino (C++) · 🐍 MicroPython — **los dos**

Punto de comparación #3, y el más interesante: **medí con el multímetro cuánto consume cada uno.** MicroPython tarda más en arrancar, y eso se traduce en menos meses de autonomía. Es un número concreto, no una opinión.

## Caso real

Sensor en un lugar sin enchufe cerca. Cambia por completo cómo se diseña el firmware.

## Dónde más se usa este patrón

_(Completar al terminar. 3-5 industrias o productos donde la misma técnica aparece, y
agregá la fila en [`docs/patrones.md`](../../docs/patrones.md).)_

-
-
-

## Técnica central

Deep sleep y presupuesto energético

## Cómo lo reconstruyo

**Componentes:** ESP32, LM35 o DHT11, batería, multímetro

| Componente | Pin | Nota |
|---|---|---|
| | | |

Pines en [`pinout.h`](../../shared/config/pinout.h) / [`pinout.py`](../../shared/config/pinout.py).

📷 Foto del cableado y video de 20s en [`media/`](media/) — **sacalos antes de desarmar.**

## Criterio de terminado

_(Copiar del roadmap, "Criterio de terminado — Semana 9".)_

- [ ]
- [ ]
- [ ] Foto y video en `media/` antes de desarmar
- [ ] Fila agregada en `docs/patrones.md`

## Qué me costó

_(Lo que falló, cuánto tardé, qué lo resolvió.)_
