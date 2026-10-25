# Control de tanque

> **Semana 5** del [roadmap](../../roadmap_v2_kit.md) · Estado: ⬜ sin empezar
> **Framework:** 🔵 Arduino (C++)
>
> 📑 [Índice de este proyecto](index.md)

El timing del servo y del stepper necesita precisión que el intérprete de MicroPython no garantiza.

## Caso real

Bomba de agua automática y persiana motorizada. Universal en LATAM: ahorra agua y bombas.

## Dónde más se usa este patrón

_(Completar al terminar. 3-5 industrias o productos donde la misma técnica aparece, y
agregá la fila en [`docs/patrones.md`](../../docs/patrones.md).)_

-
-
-

## Técnica central

Actuadores con fallas seguras

## Cómo lo reconstruyo

**Componentes:** Relay, sensor de nivel, servo SG90, stepper + ULN2003, joystick, receptor IR, sensor de inclinación, sensor de sonido

| Componente | Pin | Nota |
|---|---|---|
| | | |

Pines en [`pinout.h`](../../shared/config/pinout.h) / [`pinout.py`](../../shared/config/pinout.py).

📷 Foto del cableado y video de 20s en [`media/`](media/) — **sacalos antes de desarmar.**

## Criterio de terminado

_(Copiar del roadmap, "Criterio de terminado — Semana 5".)_

- [ ]
- [ ]
- [ ] Foto y video en `media/` antes de desarmar
- [ ] Fila agregada en `docs/patrones.md`

## Qué me costó

_(Lo que falló, cuánto tardé, qué lo resolvió.)_
