# Pinout de mi placa — NodeMCU ESP-32S (38 pines)

Transcrito de la serigrafía de **mi** placa y verificado contra el layout estándar del
NodeMCU-32S. Los 19 pines de cada lado, numerados **desde el extremo opuesto al USB**.

```
        ┌─────────────────────┐
     1  │ 3V3             GND │  1
     2  │ EN              P23 │  2
     3  │ SVP             P22 │  3
     4  │ SVN              TX │  4
     5  │ P34              RX │  5
     6  │ P35             P21 │  6
     7  │ P32             GND │  7
     8  │ P33             P19 │  8
     9  │ P25             P18 │  9
    10  │ P26              P5 │ 10
    11  │ P27             P17 │ 11
    12  │ P14             P16 │ 12
    13  │ P12             P4  │ 13
    14  │ GND             P0  │ 14
    15  │ P13             P2  │ 15
    16  │ SD2             P15 │ 16
    17  │ SD3             SD1 │ 17
    18  │ CMD             SD0 │ 18
    19  │ 5V              CLK │ 19
        │      ╔═══════╗      │
        └──────╢  USB  ╟──────┘
               ╚═══════╝
```

---

## Lado izquierdo

| # | Rótulo | GPIO | Notas | Columna protoboard |
|---|---|---|---|---|
| 1 | `3V3` | — | Salida del regulador. **Nunca alimentes por acá** | |
| 2 | `EN` | — | Reset (activo bajo) | |
| 3 | `SVP` | 36 | ADC1 · **solo entrada, sin pull-up** | |
| 4 | `SVN` | 39 | ADC1 · **solo entrada, sin pull-up** | |
| 5 | `P34` | 34 | ADC1 · **solo entrada, sin pull-up** | |
| 6 | `P35` | 35 | ADC1 · **solo entrada, sin pull-up** | |
| 7 | `P32` | 32 | ADC1 · entrada/salida | |
| 8 | `P33` | 33 | ADC1 · entrada/salida | |
| 9 | `P25` | 25 | ADC2 ⚠️ · DAC1 | |
| 10 | `P26` | 26 | ADC2 ⚠️ · DAC2 | |
| 11 | `P27` | 27 | ADC2 ⚠️ | |
| 12 | `P14` | 14 | ADC2 ⚠️ | |
| 13 | `P12` | 12 | 🚫 **Strapping: no usar.** En HIGH al bootear, el chip no arranca | |
| 14 | **`GND`** | — | Masa | |
| 15 | **`P13`** | 13 | ADC2 ⚠️ · **LED de s01** | |
| 16 | `SD2` | 9 | ❌ Flash interna | |
| 17 | `SD3` | 10 | ❌ Flash interna | |
| 18 | `CMD` | 11 | ❌ Flash interna | |
| 19 | `5V` | — | **Entrada** de alimentación (VIN), 5-12V | |

## Lado derecho

| # | Rótulo | GPIO | Notas | Columna protoboard |
|---|---|---|---|---|
| 1 | `GND` | — | Masa | |
| 2 | `P23` | 23 | SPI MOSI | |
| 3 | `P22` | 22 | **I2C SCL** | |
| 4 | `TX` | 1 | UART0 TX — la consola serie. No usar como GPIO | |
| 5 | `RX` | 3 | UART0 RX — la consola serie. No usar como GPIO | |
| 6 | `P21` | 21 | **I2C SDA** | |
| 7 | `GND` | — | Masa | |
| 8 | `P19` | 19 | SPI MISO | |
| 9 | `P18` | 18 | SPI SCK | |
| 10 | `P5` | 5 | SPI CS · strapping leve | |
| 11 | `P17` | 17 | Libre | |
| 12 | **`P16`** | 16 | **Botón de s01** | |
| 13 | `P4` | 4 | ADC2 ⚠️ | |
| 14 | `P0` | 0 | ⚠️ Strapping: es el botón `BOOT` | |
| 15 | `P2` | 2 | **LED onboard** · strapping leve | |
| 16 | `P15` | 15 | ADC2 ⚠️ · strapping leve | |
| 17 | `SD1` | 8 | ❌ Flash interna | |
| 18 | `SD0` | 7 | ❌ Flash interna | |
| 19 | `CLK` | 6 | ❌ Flash interna | |

---

## Leyenda

| | Qué significa |
|---|---|
| ❌ **Flash interna** | GPIO 6-11. Conectados a la memoria del chip. Usarlos = la placa no arranca |
| 🚫 **Strapping crítico** | GPIO 12. Si está en alto al bootear, el chip configura mal el voltaje de flash |
| ⚠️ **ADC2** | Deja de funcionar en cuanto llamás `WiFi.begin()`. Nada analógico acá |
| **Solo entrada** | GPIO 34, 35, 36, 39. No pueden ser salida y **no tienen pull-up interno** |

**Para sensores analógicos usá solo ADC1: 32, 33, 34, 35, 36, 39.**

## Pines realmente libres

Descontando flash, strapping, UART0 y los buses reservados, lo que queda para usar sin
pensarlo: **13, 14, 16, 17, 25, 26, 27, 32, 33** y, como entradas analógicas,
**34, 35, 36, 39**.

Es exactamente lo que asigna [`shared/config/pinout.h`](../shared/config/pinout.h).

---

## Cómo llegar a un pin en mi protoboard

El ESP32 ocupa las **columnas 1 a 19**, con los pines en las filas **`b`** e **`i`**.
Cada pin cae en su propia columna.

| Pin en la fila… | Metés el jumper en… |
|---|---|
| `i` | `j<columna>` |
| `b` | `a<columna>` |

Las filas `c` a `h` quedan tapadas por el módulo. Ver
[`docs/inventario.md`](inventario.md) para el detalle del banco.

> Completá la columna "Columna protoboard" de las tablas de arriba la primera vez que
> montes la placa. Mientras no la muevas, esos números no cambian.

---

[⬅ README del repo](../README.md) · [Inventario del kit](inventario.md) ·
[Pinout del proyecto](../shared/config/pinout.h)
