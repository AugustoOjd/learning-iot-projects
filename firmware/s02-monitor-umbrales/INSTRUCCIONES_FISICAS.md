# Instrucciones físicas — Monitor de umbrales

Todo lo que pasa fuera del código: qué es cada componente, cómo se ve, cómo se conecta y en
qué orden armarlo.

Tenela abierta al lado de la protoboard. La semana se arma en **cuatro montajes** que se van
sumando sin desarmar nada: no pases al siguiente sin que ande el anterior.

| | |
|---|---|
| **Código** | [`micropython/`](micropython/): un script de prueba por montaje + [`main.py`](micropython/main.py) |
| **Números de pin** | [`shared/config/pinout.py`](../../shared/config/pinout.py) |
| **Columnas de mi placa** | [`docs/inventario.md`](../../docs/inventario.md) |
| **Teoría de la semana** | [roadmap, Semana 2](../../roadmap_v2_kit.md) |
| **Qué pasó al armarlo** | Bitácora: [día 1](documentation-days/2026-10-11.md) · [día 2](documentation-days/2026-10-25.md) |

---

## Parte 1 — Los componentes

### Potenciómetro 10K

Una resistencia de tres patas con un contacto que se desliza. Entre las dos patas de los
extremos hay siempre 10K; la del medio (el *wiper*) recorre la pista cuando girás y la parte
en dos tramos que suman 10K.

```
   pata 1 ─────[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓]───── pata 3
                       ▲
                     wiper (pata 2)
```

Con un extremo a 3.3V y el otro a GND, el wiper entrega cualquier voltaje entre 0 y 3.3V. Es
**el sensor perfecto para probar un ADC**: vos controlás el voltaje con la mano y sabés qué
esperar.

Si invertís los extremos no se rompe nada: solo cambia el sentido de giro.

### Fotorresistencia (LDR)

En el kit figura como **"Foto Resistencias"** (vienen 3). Es un disco chato de ~5 mm con un
**zigzag naranja** en la cara y dos patas iguales. **No tiene polaridad.**

**No genera voltaje: cambia su resistencia con la luz.** Medido en mi cuarto:

| Condición | Resistencia |
|---|---|
| Tapada con el dedo | ~200K o más |
| Luz del cuarto | ~56K |
| Linterna del celular | ~4K |

No confundir con un LED, que es una cúpula con una pata más larga que la otra.

### Resistencias

| Valor | Bandas | Para qué esta semana |
|---|---|---|
| **10K** | marrón · negro · **naranja** · dorado | Divisor de la fotorresistencia |
| **220Ω** | rojo · rojo · marrón · dorado | Limitar la corriente del LED |
| 1K | marrón · negro · **rojo** · dorado | No se usa. Ojo: se confunde con la 10K |

Lo que separa la 10K de la 1K es la **tercera banda**.

### LM35DZ

**Parece un transistor:** cápsula negra semicircular de 3 patas (TO-92). La única forma de
estar seguro es leer lo impreso en la cara plana: `LM35DZ`.

```
   cara plana hacia vos, patas abajo
          ┌─────────┐
          │ LM35DZ  │
          └─┬──┬──┬─┘
           5V OUT GND
```

- Entrega **10 mV por °C**: a 25°C, 250 mV. Sin librería, sin protocolo.
- **Necesita mínimo 4V**, así que no anda con 3.3V: va a **5V**.
- Su **salida** no pasa de 1.5V ni a 150°C, así que el pin del ESP32 nunca ve 5V.

> 🔥 **Al revés se calienta.** A los 10 segundos de enchufar, tocalo. Si está caliente,
> desenchufá ya.

### LED rojo

La pata **larga** es el ánodo (+) y la corta el cátodo (−). Siempre con una resistencia en
serie, porque un LED no limita su propia corriente.

### Buzzer activo

Cilindro negro igual al pasivo. Para distinguirlos:

1. **Por abajo:** el activo está **sellado**; el pasivo muestra el circuito verde.
2. **Definitiva:** con el USB enchufado, apoyá la pata larga en el riel `+` y la corta en el
   `−`. El **activo pita** solo; el pasivo hace un click y nada más.

**Marcalo con cinta apenas lo identifiques.** Tiene polaridad: pata larga o `+` marcado.

---

## Parte 2 — Reglas antes de empezar

**0. Todos los comandos se corren desde `micropython/`:**
`cd firmware/s02-monitor-umbrales/micropython`

**1. Desenchufá el USB antes de mover un cable.** Hay una sola excepción, en la sección "Si no
anda": usar la punta de una **entrada** del ADC para medir puntos de 0 a 3.3V.

**2. Ubicá los pines con la regla de la columna.** El USB queda del lado de la **columna 1**.
El pin #n del [pinout](../../docs/pinout-placa.md), contado desde el extremo opuesto al USB,
cae en la **columna 20−n**. El lado izquierdo del pinout queda en la fila `i` (acceso por
`j`) y el derecho en la `b` (acceso por `a`). **Confirmá siempre con la serigrafía.**

| Pin | Columna | Acceso | Para |
|---|---|---|---|
| 5V | 1 | `j1` | LM35 |
| GPIO 13 | 5 | `j5` | LED |
| GND | 6 | `j6` | riel `−` |
| GPIO 25 | 11 | `j11` | buzzer |
| GPIO 34 | 15 | `j15` | potenciómetro |
| GPIO 39 | 16 | `j16` | fotorresistencia |
| GPIO 36 | 17 | `j17` | LM35 |
| 3V3 | 19 | `j19` | riel `+` |

**3. Todo en la mitad de arriba.** El 3V3 (`j19`) y un GND (`j6`) están del mismo lado, así
que no hace falta bajar a los rieles de abajo ni puentearlos.

**4. El riel `+` es de 3.3V, y el 5V no va por ningún riel.** Un solo cable directo de `j1` al
LM35. Así es imposible conectar un sensor al riel equivocado y meterle 5V a un pin.

**5. Tres señales en columnas pegadas.** `j15`, `j16` y `j17` están juntas. Un cable corrido
una columna lee el sensor equivocado **sin dar ningún error**.

**6. Contá los retornos antes de enchufar.** Cada componente necesita su propio camino a
GND. En el circuito completo son seis: el GND del chip, el potenciómetro, la resistencia de
10K, el LM35, el LED y el buzzer.

---

## Parte 3 — Montaje 1: el potenciómetro

Ver el ADC moverse con la mano, y descubrir dónde deja de medir.

**Necesitás:** potenciómetro 10K · 4 cables

| Paso | Pieza | De | A |
|---|---|---|---|
| 1 | Cable rojo | `j19` (3V3) | riel `+` de arriba |
| 2 | Cable negro | `j6` (GND) | riel `−` de arriba |
| 3 | Potenciómetro | patas en `f22`, `f24`, `f26` | |
| 4 | Cable | `j22` (pata izquierda) | riel `+` |
| 5 | Cable | `j26` (pata derecha) | riel `−` |
| 6 | Cable de señal | `j24` (wiper) | `j15` (GPIO 34) |

```
  + ━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━   3.3V
  − ━━━━●━━━━━━━━━━━━━━━━━━━━━━━━━━●━━━   GND
       j6       j15 ◄──┐   j22 j24 j26
                       │    │   │   │
                       └────┼───┘   │
                            └[POT]──┘
```

```bash
mpremote cp ../../../shared/config/pinout.py :
mpremote run prueba_pot.py
```

**Qué vas a observar:** de tope a tope, `crudo` va de 0 a 4095, pero `mV` va de **142 a
3155**, no de 0 a 3300. En el medio, la fórmula lineal se queda corta ~150-185 mV contra la
calibración.

---

## Parte 4 — Montaje 2: la fotorresistencia

El mismo divisor que el potenciómetro, pero el tramo de arriba lo mueve la luz.

**Necesitás:** fotorresistencia · resistencia **10K** · 2 cables

```
3.3V ── fotorresistencia ──┬── GPIO 39
                           │
                          10K
                           │
                          GND
```

| Paso | Pieza | De | A |
|---|---|---|---|
| 1 | Fotorresistencia | `f28` | `f30` |
| 2 | Cable rojo | `j28` | riel `+` |
| 3 | Resistencia 10K | `g30` | riel `−` (la pata directo) |
| 4 | Cable de señal | `j30` | `j16` (GPIO 39) |

La **columna 30** es el punto medio del divisor: ahí se juntan la fotorresistencia, la
resistencia y el cable al pin.

```bash
mpremote run prueba_ldr.py
```

**Antes de correrlo, predecí** con `V = 3300 × 10K / (R + 10K)` qué voltaje va a dar tapada,
con luz del cuarto y con linterna. **Qué vas a observar:** tapada cae en la zona ciega del
ADC, y la resistencia que calcula el script es un techo de medición, no el valor real.

---

## Parte 5 — Montaje 3: el LM35

Temperatura de verdad, y la primera vez que aparece el 5V.

**Necesitás:** LM35DZ · 3 cables

| Paso | Pieza | De | A |
|---|---|---|---|
| 1 | LM35, **cara plana hacia vos** | patas en `f34`, `f35`, `f36` | |
| 2 | Cable rojo o naranja (**5V**) | **`j1`** | `j34` (pata izquierda) |
| 3 | Cable de señal | `j35` (centro) | `j17` (GPIO 36) |
| 4 | Cable negro | `j36` (derecha) | riel `−` |

```
   j1 (5V) ──────────────────────────────┐
   j17 (GPIO 36) ◄─────────────────┐     │
                                  j35   j34   j36 ──→ riel −
                                 [   LM35DZ    ]
                                  f34  f35  f36
```

### Verificación antes de enchufar

- [ ] Dice **LM35DZ** en la cara plana, y la cara plana mira hacia vos
- [ ] El cable de 5V sale de **`j1`**, no de `j19` ni del riel `+`
- [ ] La señal llega a **`j17`**, no a `j15` ni a `j16`

```bash
mpremote run prueba_lm35.py
```

**Qué vas a observar:** la lectura suelta tiembla ±0.8°C, el promedio de 16 con `ATTN_11DB`
±0.28°C y con `ATTN_0DB` ±0.09°C. Sostenelo 30 s entre los dedos y soltalo: sube a ~31°C y
tarda casi 2 minutos en volver (constante de tiempo ~23 s).

---

## Parte 6 — Montaje 4: el monitor completo

Se suman la alarma visual y la sonora. Los sensores no se tocan.

**Necesitás:** LED rojo · resistencia **220Ω** · buzzer activo · 4 cables · algo para tapar
la fotorresistencia (tapita, tubito de papel)

```
LED:     GPIO 13 ──→ [220Ω] ──→ LED (+ → −) ──→ GND
Buzzer:  GPIO 25 ──→ buzzer (+ → −) ──→ GND
```

### LED rojo

| Paso | Pieza | De | A |
|---|---|---|---|
| 1 | Resistencia **220Ω** | `f40` | `f44` |
| 2 | LED: pata **larga** | `g44` (misma columna que la resistencia) | |
| | LED: pata corta | `g45` | |
| 3 | Cable de señal | `j5` (GPIO 13) | `j40` |
| 4 | Cable negro | `j45` | riel `−` |

### Buzzer activo

| Paso | Pieza | De | A |
|---|---|---|---|
| 5 | Buzzer: pata **+** | `f50` | |
| | Buzzer: pata − | `f53` (o donde caiga) | |
| 6 | Cable de señal | `j11` (GPIO 25) | `j50` |
| 7 | Cable negro | `j53` | riel `−` |

### Así queda la mitad de arriba

| Columna | Qué hay |
|---|---|
| 1 | 5V → LM35 |
| 5 | GPIO 13 → LED |
| 6 | GND → riel `−` |
| 11 | GPIO 25 → buzzer |
| 15 / 16 / 17 | señales: potenciómetro / fotorresistencia / LM35 |
| 19 | 3V3 → riel `+` |
| 22 – 26 | potenciómetro |
| 28 – 30 | fotorresistencia + 10K |
| 34 – 36 | LM35 |
| 40 – 45 | 220Ω + LED |
| 50 – 53 | buzzer |

### Verificación antes de enchufar

- [ ] La resistencia del LED es la de **220Ω**, no la de 10K
- [ ] La pata larga del LED está en la **columna 44**
- [ ] El buzzer es el **activo**
- [ ] Contaste los **seis retornos** al riel `−`

### Cargar y probar

```bash
mpremote run main.py          # probar sin guardarlo
mpremote cp main.py : + repl  # dejarlo instalado: arranca solo al encender
```

Empezá con la fotorresistencia **tapada** (heladera cerrada).

| # | Hacés | Tiene que pasar |
|---|---|---|
| 1 | Destapar y esperar más de 6 s, después tapar | `Puerta abierta` → a los 6 s `ALARMA` (LED + pitido) → al tapar, `Puerta cerrada` y silencio |
| 2 | Destapar 3 s y tapar | Abre y cierra **sin alarma** |
| 3 | LM35 entre los dedos 30 s, después soltar | Pasa los 28°C → `ALARMA` → **sigue ~40 s** después de soltar, hasta bajar de 26.5°C |

---

## Si no anda

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| `mpremote: no device found` | El USB no está conectado a WSL | `usbipd.exe attach --wsl --busid 1-2 --auto-attach` (ver [README raíz](../../README.md#conectar-la-placa-wsl2)) |
| `ImportError: no module named 'pinout'` | `pinout.py` no está en el chip | `mpremote cp ../../../shared/config/pinout.py :` |
| Un sensor lee **4095 fijo** | Le falta GND: un riel `−` flotando | Usá el ADC como voltímetro (abajo) |
| Un sensor lee **0 fijo** | Le falta el `+`, o el cable de señal está en otra columna | Revisá `j15`/`j16`/`j17` |
| El LM35 da una temperatura absurda | Al revés, o la señal en otra columna | **Tocalo**: si está caliente, desenchufá ya |
| El LED no prende y el buzzer sí | Resistencia de 10K en vez de 220Ω, o el LED al revés | Tercera banda roja → marrón. Pata larga en la col. 44 |
| El buzzer hace un click y no pita | Es el pasivo | Cambialo por el activo |
| La alarma de puerta salta sola | La luz de tu cuarto cambió | Volvé a medir con `prueba_ldr.py` y ajustá `LUZ_ALTO`/`LUZ_BAJO` |

### El ESP32 como voltímetro

Sin multímetro, cualquier entrada del ADC sirve para medir un punto entre 0 y 3.3V. Con el
script corriendo, sacá **una sola punta** del cable de señal (la que va al sensor; la otra
queda en el pin) y tocá con ella:

| Punto | Debería dar |
|---|---|
| `j6` (GND del chip) | ≈0: la punta funciona |
| Riel `+` | 4095 |
| Riel `−` | ≈0. Si da 4095, el riel no tiene GND |

Es seguro porque es una **entrada** tocando puntos de 0 a 3.3V. **Nunca toques el pin `5V`
(`j1`) con esa punta.**

**Por qué un riel sin GND da 4095 y no 0:** un punto sin camino a GND no está en 0V, está en
el valor de lo que tenga al lado. Si lo único que lo toca es un componente unido al `+`, no
circula corriente, no cae tensión, y el punto queda en 3.3V.

---

## Antes de desarmar

📷 **Foto del cableado y video de 20 segundos funcionando**, a [`media/`](media/). En s01 se
perdió: este circuito deja de existir cuando lo desarmes.

- **Foto:** desde arriba, que se lean las columnas y los colores de los cables.
- **Video:** destapar la fotorresistencia → alarma a los 6 s → tapar → silencio.

Para cerrar, revisá:

1. El criterio de terminado del [`README.md`](README.md): queda pendiente el LM35 contra un
   termómetro real
2. Lo que descubriste de tu kit en [`docs/inventario.md`](../../docs/inventario.md)
3. Las filas de la semana en [`docs/patrones.md`](../../docs/patrones.md)
