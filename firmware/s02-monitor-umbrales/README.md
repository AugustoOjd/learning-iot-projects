# Monitor de umbrales

> **Semana 2** del [roadmap](../../roadmap_v2_kit.md) · Estado: ⬜ sin empezar
> **Framework:** 🐍 MicroPython
>
> 📑 [Índice de este proyecto](index.md)

El REPL es ideal acá: calibrás umbrales en vivo, moviendo el potenciómetro y leyendo valores, sin recompilar.

## Caso real

Monitor de sala de servidores o de heladera de farmacia: temperatura y luz con alerta por umbral.

## Dónde más se usa este patrón

_(Completar al terminar. 3-5 industrias o productos donde la misma técnica aparece, y
agregá la fila en [`docs/patrones.md`](../../docs/patrones.md).)_

-
-
-

## Técnica central

ADC, divisor de tensión e histéresis

## Cómo lo reconstruyo

**Componentes:** LM35DZ, 3 fotorresistencias, potenciómetro 10K, resistencias 10K

| Componente | Pin | Nota |
|---|---|---|
| | | |

Pines en [`pinout.h`](../../shared/config/pinout.h) / [`pinout.py`](../../shared/config/pinout.py).

📷 Foto del cableado y video de 20s en [`media/`](media/) — **sacalos antes de desarmar.**

## Criterio de terminado

_(Copiar del roadmap, "Criterio de terminado — Semana 2".)_

- [ ]
- [ ]
- [ ] Foto y video en `media/` antes de desarmar
- [ ] Fila agregada en `docs/patrones.md`

## Qué me costó

_(Lo que falló, cuánto tardé, qué lo resolvió.)_
