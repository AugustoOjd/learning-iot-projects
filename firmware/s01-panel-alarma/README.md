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

### Montaje 1 — LED y botón ✅ verificado

| # | Desde | Hasta | Qué es |
|---|---|---|---|
| 1 | `j6` | riel `−` de arriba | GND de la placa |
| 2 | LED pata **larga** | `e30` | ánodo |
| 3 | LED pata **corta** | `e31` | cátodo |
| 4 | `d31` | riel `−` **de arriba** | masa del LED ⚠️ |
| 5 | Resistencia 220Ω | `d30` → `d34` | en serie con el LED |
| 6 | `c34` | `j5` | señal — **GPIO 13** |
| 7 | Botón | columnas **40 y 42**, a caballo del canal | patas en `e40`,`e42`,`h40`,`h42` |
| 8 | `d40` | `a8` | señal — **GPIO 16** |
| 9 | `j42` | riel `−` | masa del botón ⚠️ |

⚠️ **Las dos que me costaron una tarde** (ver [bitácora del 2026-09-20](documentation-days/2026-09-20.md)):

- **`d31` va al riel de arriba**, el mismo que `j6`. Los rieles de arriba y abajo son
  independientes. Puenteálos al empezar y deja de importar.
- **La masa del botón va en la columna 42, no en la 40.** Los switches de 12×12 de este kit
  emparejan las patas *a lo largo* del canal, así que los dos jumpers salen de columnas
  distintas — al revés de lo que aplica a los tácticos de 6×6.

### Montaje 2 — Buzzers ⬜

| Componente | Pin | Nota |
|---|---|---|
| Buzzer activo | GPIO 25 | `digitalWrite` |
| Buzzer pasivo | GPIO 26 | `tone()` / PWM |

### Montaje 3 — Panel completo ⬜

| Componente | Pin | Nota |
|---|---|---|
| Sensor de llama (`DO`) | GPIO 35 | VCC a **3.3V**, no 5V |
| Botón silencio/rearme | GPIO 16 | |
| LED verde + 220Ω | GPIO 27 | |
| LED amarillo + 220Ω | GPIO 14 | |
| LED rojo + 220Ω | GPIO 13 | |
| Buzzer pasivo | GPIO 26 | sirena bitonal |

Pines en [`pinout.h`](../../shared/config/pinout.h) / [`pinout.py`](../../shared/config/pinout.py).
Montaje paso a paso en [`INSTRUCCIONES_FISICAS.md`](INSTRUCCIONES_FISICAS.md).
Columnas de cada pin de mi placa en [`docs/pinout-placa.md`](../../docs/pinout-placa.md).

📷 Foto del cableado y video de 20s en [`media/`](media/) — **sacalos antes de desarmar.**

## Criterio de terminado

_(Copiar del roadmap, "Criterio de terminado — Semana 1".)_

- [ ]
- [ ]
- [ ] Foto y video en `media/` antes de desarmar
- [ ] Fila agregada en `docs/patrones.md`

## Qué me costó

_(Lo que falló, cuánto tardé, qué lo resolvió.)_
