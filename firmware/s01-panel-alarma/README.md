# Panel de alarma

> **Semana 1** del [roadmap](../../roadmap_v2_kit.md) · Estado: 🟡 en curso
> **Framework:** 🔵 Arduino (C++) · 🐍 MicroPython — **los dos**
>
> 📑 [Índice de este proyecto](index.md)

Punto de comparación #1: la misma lógica en los dos lenguajes. Es donde ves la diferencia de sintaxis y de ciclo de desarrollo sin que el hardware complique nada.

> 🔧 **Para armarlo: [`INSTRUCCIONES_FISICAS.md`](INSTRUCCIONES_FISICAS.md)** — qué es cada
> componente, cómo se ve, cómo se conecta y en qué orden. Tres montajes incrementales.

## Caso real

Detector de incendio con sirena y luces. Es literalmente lo que hace un panel de alarma comercial, con menos certificaciones.

## Dónde más se usa este patrón

_(Completar al terminar. 3-5 industrias o productos donde la misma técnica aparece, y
agregá la fila en [`docs/patrones.md`](../../docs/patrones.md).)_

-
-
-

## Técnica central

Máquina de estados sin bloqueo

## Cómo lo reconstruyo

**Componentes:** Sensor de llama, sensor de sonido, 3 LEDs, 2 buzzers, 2 botones, módulo RGB

| Componente | Pin | Nota |
|---|---|---|
| | | |

Pines en [`pinout.h`](../../shared/config/pinout.h) / [`pinout.py`](../../shared/config/pinout.py).
Montaje paso a paso en [`INSTRUCCIONES_FISICAS.md`](INSTRUCCIONES_FISICAS.md).

📷 Foto del cableado y video de 20s en [`media/`](media/) — **sacalos antes de desarmar.**

## Criterio de terminado

_(Copiar del roadmap, "Criterio de terminado — Semana 1".)_

- [ ]
- [ ]
- [ ] Foto y video en `media/` antes de desarmar
- [ ] Fila agregada en `docs/patrones.md`

## Qué me costó

_(Lo que falló, cuánto tardé, qué lo resolvió.)_
