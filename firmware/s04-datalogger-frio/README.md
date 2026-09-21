# Datalogger de cadena de frío

> **Semana 4** del [roadmap](../../roadmap_v2_kit.md) · Estado: ⬜ sin empezar
> **Framework:** 🔵 Arduino (C++)
>
> 📑 [Índice de este proyecto](index.md)

Las librerías I2C de Arduino (RTClib, LiquidCrystal_I2C) están mucho más maduras que sus equivalentes en MicroPython.

## Caso real

Registro con hora real que sigue funcionando sin internet. Regulatorio en farmacia y gastronomía.

## Dónde más se usa este patrón

_(Completar al terminar. 3-5 industrias o productos donde la misma técnica aparece, y
agregá la fila en [`docs/patrones.md`](../../docs/patrones.md).)_

-
-
-

## Técnica central

I2C, NVS y store-and-forward

## Cómo lo reconstruyo

**Componentes:** LCD 1602, módulo RTC, DHT11, resistencia 10K

| Componente | Pin | Nota |
|---|---|---|
| | | |

Pines en [`pinout.h`](../../shared/config/pinout.h) / [`pinout.py`](../../shared/config/pinout.py).

📷 Foto del cableado y video de 20s en [`media/`](media/) — **sacalos antes de desarmar.**

## Criterio de terminado

_(Copiar del roadmap, "Criterio de terminado — Semana 4".)_

- [ ]
- [ ]
- [ ] Foto y video en `media/` antes de desarmar
- [ ] Fila agregada en `docs/patrones.md`

## Qué me costó

_(Lo que falló, cuánto tardé, qué lo resolvió.)_
