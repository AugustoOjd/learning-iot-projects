# Inventario de mi kit

Los datos que son únicos de **tu** kit y que el roadmap te hace averiguar en cuatro semanas
distintas. Tenerlos acá te ahorra horas de volver a probar.

---

## Mi protoboard y el montaje del ESP32

Protoboard de **830 puntos**: columnas **1 a 60**, filas **a** a **j**, con rieles `+`/`−`
arriba y abajo.

**Orientación tal como la veo:** la fila `j` queda arriba y la `a` abajo.

```
─────────  riel + / −
  j   ← acceso a los pines de arriba
  i   ● pines del ESP32
  h  ┐
  g  ├─ tapadas por el módulo
  f  ┘
═════════  canal
  e  ┐
  d  ├─ tapadas por el módulo
  c  ┘
  b   ● pines del ESP32
  a   ← acceso a los pines de abajo
─────────  riel + / −
```

| Dato | Valor |
|---|---|
| El ESP32 de 38 pines ocupa | **columnas 1 a 19** |
| Sus pines caen en las filas | **`b`** e **`i`** |
| Filas accesibles para cablear a un pin | **`j`** (para los de `i`) y **`a`** (para los de `b`) |
| Filas tapadas por el módulo | `c` a `h` |
| Zona libre para armar circuitos | **columnas 20 a 60** |

**Regla para llegar a un pin:** buscá la etiqueta serigrafiada, mirá en qué columna cae, y
metés el jumper en `j<columna>` si el pin está en la fila `i`, o en `a<columna>` si está en
la fila `b`.

Recordá que `j-i-h-g-f` de una columna son un punto eléctrico y `e-d-c-b-a` son otro: el
canal los separa.

### Columnas de los pines que más uso

_(Completar a medida que los ubiques)_

| Pin | Columna | Fila | Se accede por |
|---|---|---|---|
| GND | | | |
| GPIO 13 | | | |
| GPIO 16 | | | |
| GPIO 25 | | | |
| GPIO 26 | | | |
| GPIO 27 | | | |
| 3V3 | | | |

> ⚠️ ¿Los rieles `+`/`−` están cortados al medio? Mirá si la línea roja/azul se interrumpe
> en el centro. Si sí, hay que puentear las dos mitades con un jumper.
> **Resultado:** _(completar)_

---

## Verificaciones pendientes (hacelas antes de la semana 4)

Contá los pines. Cambian el código y la lista de compras:

- [ ] **LCD 1602** → ¿4 pines (`GND`,`VCC`,`SDA`,`SCL`) o 16?
  - 4 = backpack I2C, librería `LiquidCrystal_I2C` ✅
  - 16 = paralelo crudo, gasta 6 GPIO → comprar backpack PCF8574 (~$2)
  - **Resultado:** _(completar)_
- [ ] **Matriz 8x8** → ¿5 pines (`DIN`,`CS`,`CLK`,`VCC`,`GND`) o 16?
  - 5 = chip MAX7219, librería `LedControl` ✅
  - 16 = cruda → **necesita dos 74HC595 y el kit trae uno** (comprar el segundo, ~$1)
  - **Resultado:** _(completar)_
- [ ] **Display 4 dígitos** → ¿4 pines (`CLK`,`DIO`,`VCC`,`GND`) o 12?
  - 4 = chip TM1637 ✅ · 12 = crudo, multiplexado a mano
  - **Resultado:** _(completar)_
- [ ] **Módulo RTC** → ¿dice DS3231 (±2 min/año) o DS1307 (±20 min/mes)?
  - **Resultado:** _(completar)_
- [ ] **Pila CR2032 del RTC** → ¿vino puesta? Sacale el plástico aislante o pierde la hora en cada corte
- [ ] **RC522** → ¿la tira de pines viene soldada o suelta en la bolsita?
- [ ] **Display 1 dígito** → ¿cátodo o ánodo común? (tester en modo diodo)
- [ ] **Módulo RGB** → ¿cátodo o ánodo común? ¿trae resistencias integradas?
- [ ] **Relay** → ¿activa con `HIGH` o con `LOW`? Anotar y definir `RELAY_ACTIVO`
- [ ] **Buzzers** → distinguir activo de pasivo (tester en `Ω`: el pasivo mide ~8-16Ω)
- [ ] **Protoboard** → ¿las filas `+`/`−` están partidas al medio? Si sí, puentearlas

## Datos de mi kit

| Dato | Valor | Dónde lo usé |
|---|---|---|
| Dirección I2C del LCD | `0x__` | s04 |
| Dirección I2C del RTC | `0x__` | s04 |
| Chip del RTC | | s04 |
| Relay activo en | `HIGH` / `LOW` | s05 |
| UID llavero RFID | | s06 |
| UID tarjeta RFID | | s06 |
| MAC del ESP32 #1 | | s11 |
| MAC del ESP32 #2 (gateway) | | s11 |
| Canal WiFi del router | | s11 (ESP-NOW debe coincidir) |

## Códigos del control remoto IR

Corré el sketch de s05 e imprimí `IrReceiver.decodedIRData.command` para cada tecla.

| Tecla | Código |
|---|---|
| ▲ | `0x__` |
| ▼ | `0x__` |
| OK | `0x__` |

## Calibraciones

| Sensor | Valor medido | Condición |
|---|---|---|
| Nivel de agua — vacío | | s05 |
| Nivel de agua — lleno | | s05 |
| LM35 vs termómetro real | | s02 |

## Compras pendientes

| Ítem | Para | Precio | Estado |
|---|---|---|---|
| Multímetro | Todo, desde el día 1 | ~$5 | ⬜ |
| Fuente 5V 2A | s05 (servo, stepper) | ~$8 | ⬜ |
| Segundo ESP32 | s11 (ESP-NOW) | ~$10 | ⬜ |
| Backpack I2C | s04, solo si el LCD tiene 16 pines | ~$2 | ⬜ |
| Segundo 74HC595 | s07, solo si la matriz es cruda | ~$1 | ⬜ |
| 18650 + TP4056 | s09 (la pila de 9V no sirve para autonomía) | ~$5 | ⬜ |
| Perfboard, estaño, capacitores 470µF | s12 | ~$6 | ⬜ |
