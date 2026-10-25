# Panel indicador

> **Semana 7** del [roadmap](../../roadmap_v2_kit.md) · Estado: ⬜ sin empezar
> **Framework:** 🔵 Arduino (C++)
>
> 📑 [Índice de este proyecto](index.md)

**Acá MicroPython directamente no puede.** El multiplexado necesita refrescar 8 filas a más de 60Hz; el intérprete no llega y la matriz parpadea visiblemente.

## Caso real

Tablero de estado industrial. Y la respuesta a "me quedé sin pines".

## Dónde más se usa este patrón

_(Completar al terminar. 3-5 industrias o productos donde la misma técnica aparece, y
agregá la fila en [`docs/patrones.md`](../../docs/patrones.md).)_

-
-
-

## Técnica central

Expansión de I/O y multiplexado

## Cómo lo reconstruyo

**Componentes:** 74HC595, matriz 8x8, display 4 dígitos, display 1 dígito, LEDs

| Componente | Pin | Nota |
|---|---|---|
| | | |

Pines en [`pinout.h`](../../shared/config/pinout.h) / [`pinout.py`](../../shared/config/pinout.py).

📷 Foto del cableado y video de 20s en [`media/`](media/) — **sacalos antes de desarmar.**

## Criterio de terminado

_(Copiar del roadmap, "Criterio de terminado — Semana 7".)_

- [ ]
- [ ]
- [ ] Foto y video en `media/` antes de desarmar
- [ ] Fila agregada en `docs/patrones.md`

## Qué me costó

_(Lo que falló, cuánto tardé, qué lo resolvió.)_
