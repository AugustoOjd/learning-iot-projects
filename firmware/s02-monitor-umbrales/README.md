# Monitor de umbrales

> **Semana 2** del [roadmap](../../roadmap_v2_kit.md) · Estado: 🟡 en curso
> **Framework:** 🐍 MicroPython
>
> 📑 [Índice de este proyecto](index.md)

El REPL es ideal acá: calibrás umbrales en vivo, moviendo el potenciómetro y leyendo valores, sin recompilar.

> 🔧 **Para armarlo: [`INSTRUCCIONES_FISICAS.md`](INSTRUCCIONES_FISICAS.md)**: qué es cada
> componente, cómo se ve, cómo se conecta y en qué orden. Cuatro montajes incrementales.

## Caso real

Monitor de heladera de farmacia: la temperatura de las vacunas y los medicamentos, y una
alarma si la puerta queda abierta. El LM35 mide la temperatura. La fotorresistencia vigila la
puerta: adentro de una heladera cerrada está oscuro, así que luz quiere decir puerta abierta.

El mismo circuito sirve para una sala de servidores: temperatura alta, o luz encendida cuando
no debería haber nadie.

## Dónde más se usa este patrón

- **Termostatos y aire acondicionado.** Prenden a una temperatura y apagan a otra: es la
  histéresis de este proyecto con un relay en lugar de un buzzer. Sin la banda muerta, el
  compresor arranca y para varias veces por minuto y se rompe.
- **Alumbrado público y luces de jardín.** Una fotorresistencia en divisor de tensión con
  umbral e histéresis, para que la luz no parpadee al atardecer, cuando la luz ambiente ronda
  el umbral.
- **Cadena de frío de vacunas y alimentos.** Heladeras con alarma de puerta abierta por tiempo
  y registro de temperatura. Es lo que sigue en s04, cuando el monitor agrega hora real y
  memoria.
- **Medición de batería.** Un divisor de tensión baja el voltaje de la batería al rango del
  ADC. Es lo mismo que se hace en s09.
- **Riego automático.** El sensor de humedad de suelo es resistivo y se lee con el mismo
  divisor, promediado y con umbral.

## Técnica central

ADC, divisor de tensión e histéresis

| Técnica | Qué aprendí con mis propias mediciones |
|---|---|
| **Límites del ADC** | Con `ATTN_11DB` el rango útil es ~150 mV a ~3.15V, no 0 a 3.3V. `crudo=0` quiere decir "debajo de ~140 mV" |
| **Calibración de fábrica** | La fórmula lineal `crudo × 3300 / 4095` se queda corta hasta 184 mV. `read_uv()` usa la curva grabada en el chip |
| **Divisor de tensión** | Convierte resistencia en voltaje. La resistencia fija se elige: `R ≈ √(R_oscuro × R_claro)` |
| **Atenuación según la señal** | El LM35 da ~250 mV. Con `ATTN_0DB` el ruido baja de ±0.28 a ±0.09°C |
| **Promedio de lecturas** | 16 lecturas bajan el ruido ~3 veces (la teoría dice √16 = 4) |
| **Histéresis** | La alarma se activa a 28.0°C y se libera a 26.5°C. Tarda ~39 s en liberarse después de sacar la mano |

## Cómo lo reconstruyo

**Componentes:** LM35DZ, fotorresistencia, potenciómetro 10K, resistencia 10K, resistencia
220Ω, LED rojo, buzzer activo.

USB del lado de la columna 1: el pin #n del [pinout](../../docs/pinout-placa.md) cae en la
**columna 20−n**. Todo el circuito vive en la mitad de arriba de la protoboard.

### Alimentación

| Desde | Hasta | Qué es |
|---|---|---|
| `j19` | riel `+` de arriba | **3V3** |
| `j6` | riel `−` de arriba | **GND**, del mismo lado que el 3V3: sin puente entre rieles |
| `j1` | `j34` (LM35) | **5V**, cable directo, **sin riel** |

### Sensores y actuadores

| Componente | Pin | Columnas | Nota |
|---|---|---|---|
| Potenciómetro 10K | GPIO 34 (`j15`) | 22 – 24 – 26 | Montaje 1. Extremos a `+` y `−`, wiper al pin |
| Fotorresistencia + 10K | GPIO 39 (`j16`) | 28 – 30 | Fotorresistencia del `+` a la col. 30; 10K de la col. 30 al `−` |
| LM35DZ | GPIO 36 (`j17`) | 34 – 35 – 36 | Cara plana hacia vos: 5V – señal – GND |
| LED rojo + 220Ω | GPIO 13 (`j5`) | 40 – 44 – 45 | Pata larga del LED en la col. 44 |
| Buzzer activo | GPIO 25 (`j11`) | 50 – 53 | `+` en la col. 50 |

⚠️ Las señales de los tres sensores están en **columnas pegadas** (`j15`, `j16`, `j17`). Un
cable corrido una columna lee el sensor equivocado sin dar ningún error.

### Código

| Archivo | Qué hace |
|---|---|
| [`prueba_pot.py`](micropython/prueba_pot.py) | Montaje 1: crudo contra calibrado, recorriendo todo el rango |
| [`prueba_ldr.py`](micropython/prueba_ldr.py) | Montaje 2: voltaje y resistencia despejada de la fotorresistencia |
| [`prueba_lm35.py`](micropython/prueba_lm35.py) | Montaje 3: lectura suelta contra promedio, `ATTN_11DB` contra `ATTN_0DB` |
| [`main.py`](micropython/main.py) | Montaje 4: el monitor completo |

**Umbrales del monitor**, todos salidos de mediciones propias:

| Alarma | Se activa | Se libera | De dónde sale |
|---|---|---|---|
| Temperatura alta | > 28.0°C | < 26.5°C | Ambiente 25.5°C, dedos 31°C, ruido ±0.09°C |
| Puerta (luz) | > 350 mV | < 250 mV | Tapada ~157 mV, cuarto ~500 mV |
| Puerta abierta demasiado | más de 6 s | al cerrarla | Las heladeras comerciales usan ~60 s |

Pines en [`pinout.h`](../../shared/config/pinout.h) / [`pinout.py`](../../shared/config/pinout.py).

📷 Foto del cableado y video de 20s en [`media/`](media/) — **sacalos antes de desarmar.**

## Criterio de terminado

- [x] Podés dibujar el divisor de tensión de memoria y explicar por qué hace falta
- [ ] Tu LM35 coincide con un termómetro real dentro de ±1°C. **Pendiente**: no tengo
      termómetro; espera al multímetro con sonda de temperatura
- [x] Entendés por qué el LM35 va a 5V y no a 3.3V
- [x] Tu alarma tiene histéresis y podés explicar qué pasaría sin ella
- [x] Todos tus sensores analógicos están en GPIO 32-39 (34, 39 y 36)
- [ ] Foto y video en `media/` antes de desarmar
- [x] Fila agregada en `docs/patrones.md`

## Qué me costó

- **Un riel `−` flotando** (día 1). El potenciómetro leía 4095 fijo. Sin camino a GND, el riel
  quedaba en 3.3V a través del propio potenciómetro. Lo encontré **usando el ADC como
  voltímetro**: el cable de la señal se convirtió en punta de prueba. Lo resolví con el GND de
  `j6`, del mismo lado que el 3V3. Es la cuarta falla de retorno a masa en dos proyectos.
- **Suponer valores en vez de medirlos** (día 2). Supuse que la fotorresistencia daba 10K con
  la luz del cuarto y daba 56K. Con eso, oscuro → ambiente usa solo el 11% del ADC.
- **Una corrección propia.** Había anotado que `ATTN_0DB` permitiría medir una heladera
  (2-8°C). No es así: también tiene un piso, de ~100 mV. Debajo de ~10°C este circuito no
  mide con ninguna atenuación.

Detalle completo en la bitácora: [2026-10-11](documentation-days/2026-10-11.md) ·
[2026-10-25](documentation-days/2026-10-25.md).
