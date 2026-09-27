# Instrucciones físicas — Panel de alarma

Todo lo que pasa fuera del código: qué es cada componente, cómo se ve, cómo se conecta y en
qué orden armarlo.

Tenela abierta al lado de la protoboard. La semana se arma en **tres montajes** que se van
sumando — no saltes al 3 sin que ande el 1.

| | |
|---|---|
| **Código Arduino** | [`arduino/src/main.cpp`](arduino/src/main.cpp) |
| **Código MicroPython** | [`micropython/main.py`](micropython/main.py) |
| **Números de pin** | [`shared/config/pinout.h`](../../shared/config/pinout.h) · [`pinout.py`](../../shared/config/pinout.py) |
| **Qué anotar de tu kit** | [`docs/inventario.md`](../../docs/inventario.md) |
| **Teoría de la semana** | [roadmap, Semana 1](../../roadmap_v2_kit.md) |

---

## Parte 1 — Los componentes

### El ESP32 NodeMCU de 38 pines

```
       ┌─┬────────────────┬─┐
   ────┤ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ├────    ← módulo metálico (el chip + la radio)
   ────┤ │ ▓▓ antena ▓▓▓▓ │ ├────
   ────┤ └────────────────┘ ├────
   ────┤   [EN]     [BOOT]  ├────    ← dos botoncitos
   ────┤      ╔══════╗      ├────
       └──────╢ USB  ╟──────┘
              ╚══════╝
```

Placa negra larga con un módulo metálico cuadrado y una antena serigrafiada en la punta.
Es la computadora: microcontrolador de dos núcleos, WiFi, Bluetooth.

**Lo que tenés que saber ahora:**

- Los números de pin están **serigrafiados en la placa**, al lado de cada uno. **Leé los
  rótulos, no cuentes pines** — la numeración no es secuencial ni simétrica.
- Los dos botones: `EN` (o `RST`) reinicia. `BOOT` se mantiene apretado si la subida de código
  falla.
- Pines que **no existen** para vos: GPIO 6, 7, 8, 9, 10 y 11 (están conectados a la memoria
  flash interna). Aparecen en el header pero usarlos hace que la placa no arranque.
- **No uses GPIO 12** en todo el kit. Si está en alto al arrancar, el chip configura mal el
  voltaje de flash y no bootea.

### Protoboard de 830 puntos

```
 ┌──────────────────────────────────────────┐
 │ + ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●  │ ← toda la fila unida (alimentación)
 │ − ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●  │ ← toda la fila unida (GND)
 │                                          │
 │ a ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●    │ ┐
 │ b ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●    │ │ las 5 de una COLUMNA
 │ c ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●    │ │ están unidas entre sí
 │ d ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●    │ │ (a-b-c-d-e)
 │ e ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●    │ ┘
 │════════════ canal central ═══════════════│ ← separa los dos lados
 │ f ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●    │ ┐ otro grupo
 │ g ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●    │ ┘ (f-g-h-i-j)
 └──────────────────────────────────────────┘
```

Placa blanca con agujeritos que conecta componentes sin soldar.

**Lo único que hay que entender:** los 5 agujeros de una columna son **el mismo punto
eléctrico**. Dos patas en `a5` y `c5` están conectadas. En `a5` y `a6`, no.

### ⚠️ Los rieles: la falla que más tiempo cuesta

**Hay cuatro rieles independientes, no dos.** El `−` de arriba y el `−` de abajo tienen el
mismo símbolo y el mismo color de línea, pero **nunca vienen conectados de fábrica**. Son dos
nodos eléctricos distintos.

```
┌──────────────────────────────┐
│ +  ●●●●●●●●●●●●●●●●●●●●●●●  │ ← riel 1
│ −  ●●●●●●●●●●●●●●●●●●●●●●●  │ ← riel 2
│         (filas j … a)        │
│ −  ●●●●●●●●●●●●●●●●●●●●●●●  │ ← riel 3  NO es el mismo que el 2
│ +  ●●●●●●●●●●●●●●●●●●●●●●●  │ ← riel 4
└──────────────────────────────┘
```

Y además **cada riel puede estar cortado al medio a lo largo**: mirá si la línea roja o azul
se interrumpe en el centro.

**Paso 0 de todo montaje, sin excepción:**

```
jumper:  riel − de arriba  →  riel − de abajo
```

Un solo cable. Después usás el riel que te quede más cerca y deja de importar. En este
proyecto, olvidarlo causó dos fallas distintas: el LED rojo el primer día y los LEDs verde y
amarillo el segundo, ambas veces con el circuito perfectamente cableado en todo lo demás.

### Jumpers y cables Dupont

| Tipo | Cómo se ve | Para qué |
|---|---|---|
| **Jumper** (65 en el kit) | Cable rígido de colores, punta metálica en ambos extremos | Protoboard ↔ protoboard |
| **Dupont macho-hembra** (10) | Pin de un lado, conector hueco del otro | Pin del ESP32 o de un módulo ↔ protoboard |

Los colores no significan nada eléctricamente, pero **usá negro para GND y rojo para
alimentación** siempre. Cuando tengas 20 cables, esa disciplina es lo único que te va a
permitir leer tu propio circuito.

> Es normal que 2 o 3 jumpers vengan cortados por dentro de fábrica. Si un circuito no anda
> y todo se ve bien, probá cambiar el cable antes de dudar del código.

### LED

```
      ___
     /   \
    |     |      pata LARGA  = ánodo (+)  → va hacia el GPIO
    |     |      pata CORTA  = cátodo (−) → va a GND
     \___/
      | |
      | |___  pata corta
      |_____  pata larga
```

Un diodo que emite luz. **Tiene polaridad**: al revés no se rompe, simplemente no prende.
Otra pista además del largo de las patas: el borde del plástico está **achatado del lado
del cátodo**.

⚠️ **Nunca sin resistencia.** Un LED conectado directo a 3.3V consume toda la corriente que
pueda y se quema, llevándose puesto el pin del ESP32.

### Resistencia de 220Ω

```
    ──┤▐▐▐▐├──     rojo · rojo · marrón · dorado
```

Cilindro beige con bandas de color. Limita la corriente que pasa. **No tiene polaridad**: va
para cualquier lado.

Las tres que trae el kit:

| Valor | Bandas | Para qué |
|---|---|---|
| **220Ω** | rojo · rojo · marrón · dorado | En serie con cada LED |
| **1KΩ** | marrón · negro · rojo · dorado | Divisores, protección |
| **10KΩ** | marrón · negro · naranja · dorado | Pull-ups, divisores de sensores |

Si dudás, medila con el tester en modo `Ω`. Es más rápido y confiable que leer bandas bajo
luz de lámpara.

### Botón táctil (switch con tope)

```
   1 ●━━━━━━● 2      Las patas 1-2 ya vienen unidas de fábrica.
     ┊      ┊        Las patas 3-4 también.
   3 ●━━━━━━● 4      Apretar une los dos pares entre sí.
```

Cuadradito de 4 patas con capuchón de color. **Tiene 4 patas pero solo 2 contactos**, y esa
es la trampa más común de todo el kit:

- ❌ Cableás entre 1 y 2 → el botón queda "apretado" para siempre
- ✅ Cableás en **diagonal** (1-4 o 2-3) → funciona

Confirmalo con el tester en continuidad: las patas que pitan **sin** apretar son un par, no
las uses juntas.

**Truco de montaje:** ponelo a caballo del canal central de la protoboard. Así las patas de
cada par quedan en lados opuestos y no te podés equivocar.

### Buzzer activo y buzzer pasivo

Los dos son cilindros negros idénticos a simple vista. Tres formas de distinguirlos, de menos
a más confiable:

1. **Mirá abajo**: el pasivo suele mostrar el **circuito verde**; el activo está sellado.
2. **Tester en `Ω`**: el pasivo mide **8-16Ω** (es una bobina). El activo da resistencia alta.
3. **Definitiva**: dale 3.3V directo. El **activo suena**. El **pasivo hace un click** y nada más.

| | Buzzer activo | Buzzer pasivo |
|---|---|---|
| Tiene adentro | Un oscilador | Solo una membrana |
| Para que suene | Basta con darle tensión | Vos tenés que generarle la onda |
| Tono | Fijo, el que traiga | El que vos quieras |
| En el código | `digitalWrite()` | `tone()` / PWM |

**Marcalos con cinta apenas los identifiques.** Los vas a volver a confundir.

**Tienen polaridad**: buscá el `+` marcado en la tapa, o la pata más larga.

### Sensor de llama

```
    ┌──────────────┐
    │  ◣           │   ← elemento oscuro/azulado INCLINADO ~60°
    │   [LM393]    │   ← chip
    │   ▣ pot azul │   ← potenciómetro de ajuste
    └─┬──┬──┬──┬───┘
     VCC GND DO AO
```

Módulo que detecta la luz infrarroja de una llama (760-1100 nm).

> ⚠️ **No lo confundas con el receptor infrarrojo.** Los dos son negros y los dos trabajan con
> IR. El de llama es un **módulo con PCB y potenciómetro azul**; el receptor IR es un
> componente suelto de 3 patas con una **cúpula redonda** y sin chip. **Si tiene potenciómetro
> azul, es el de llama.**

**Salidas:** `DO` es digital (activo-bajo: se pone en 0 cuando detecta). `AO` es analógica,
no la usamos esta semana.

**Calibración:** girá el potenciómetro despacio hasta que el LED del módulo se apague con luz
ambiente y se encienda al acercar un encendedor a ~20 cm.

### Módulo RGB (opcional)

LED grande sobre un PCB chico, 4 pines: un común y tres de color. Antes de usarlo averiguá:

- **Cátodo común**: el pin común va a GND, cada color prende con valor **alto**
- **Ánodo común**: el común va a 3.3V, cada color prende con valor **bajo** (invertido)

Y fijate si trae resistencias integradas — buscá tres cuadraditos negros en el PCB. Si no las
tiene, poné 220Ω en cada color.

Anotá qué tipo te tocó en [`docs/inventario.md`](../../docs/inventario.md).

---

## Parte 2 — Reglas antes de empezar

**1. Desenchufá el USB antes de mover un cable.** Conectar en caliente es como se queman los
componentes y como aparecen los reinicios raros que después vas a buscar en el código.

**2. El GND siempre se une.** Todo lo que participa del circuito tiene que compartir la
referencia de 0V. Es la causa #1 de "no anda y no entiendo por qué".

**3. Esta semana todo va a 3.3V.** No hay nada que se pueda quemar fácil. Es la semana para
agarrar confianza.

**4. El ESP32 de 38 pines es ancho.** Montado a caballo del canal central te tapa casi toda
la protoboard y te deja **una sola columna libre de cada lado**. Es normal. Dos formas de
trabajar con eso:

- **A**: usás esa columna para lo que va directo al ESP32 y armás el resto más a la derecha.
- **B** (más cómodo esta semana): dejás el ESP32 **fuera** de la protoboard y vas de sus pines
  a la placa con los **Dupont macho-hembra**.

Elegí una y no la cambies a mitad del montaje.

---

## Parte 3 — Montaje 1: LED y botón (día 1-2)

El circuito más simple posible. Y aun así acá aparece el error #1 de todo principiante.

> 🖥️ **Podés verlo armado antes de tocar un cable.** En [`arduino/diagram.json`](arduino/diagram.json)
> está este mismo circuito para **Wokwi**, un simulador de ESP32 en el navegador. Abrilo en
> `wokwi.com` (New Project → ESP32 → pegá el contenido en la pestaña `diagram.json`) y vas a
> ver las conexiones dibujadas sobre la placa. También corre el código de verdad, así que
> podés apretar el botón simulado y ver el LED responder.
>
> Sirve para entender el circuito, no para reemplazarlo: el simulador no tiene cables
> cortados, ni patas mal insertadas, ni botones cableados entre patas del mismo par — que es
> justamente lo que vas a aprender a diagnosticar.

**Necesitás:** 1 LED rojo · 1 resistencia 220Ω · 1 botón · 3 jumpers

### Paso a paso

**1. El GND primero.** Un jumper negro desde cualquier pin `GND` del ESP32 hasta la fila `−`
de la protoboard. Todo circuito empieza por acá.

**2. El LED.**
```
pata larga (ánodo)  → columna 10, fila a
pata corta (cátodo) → fila −  (GND)
```

**3. La resistencia**, en serie entre el GPIO y el ánodo:
```
una pata  → columna 10, fila b     (mismo punto que el ánodo)
otra pata → columna 16, fila b
```

**4. El cable al GPIO.** Jumper desde **GPIO 13** hasta `columna 16, fila c`.

**5. El botón**, a caballo del canal central, **en diagonal**:
```
una pata (arriba)     → jumper a GPIO 16
pata diagonal (abajo) → jumper a la fila −  (GND)
```

### Esquema

```
ESP32 GPIO 13 ──── [220Ω] ──── LED(+)
                               LED(−) ──── GND

ESP32 GPIO 16 ──────┬──── botón ──── GND
                    │
             (pull-up interno, activado por software)

ESP32 GND ──── fila − de la protoboard
```

**Fijate que el botón no lleva resistencia.** Es a propósito: el ESP32 tiene una resistencia
de pull-up interna que se activa desde el código con `INPUT_PULLUP` — ver
[`main.cpp`](arduino/src/main.cpp).

### Cargar el código

```bash
# Arduino
cd arduino && pio run -t upload && pio device monitor

# MicroPython
cd micropython
mpremote cp ../../../shared/config/pinout.py :
mpremote cp main.py : + repl
```

El LED tiene que prender **solo mientras apretás** el botón.

### Si no anda

| Síntoma | Mirá esto |
|---|---|
| El LED nunca prende | ¿Está al revés? La pata larga va hacia la resistencia |
| El LED está siempre prendido | El botón está cableado entre patas del mismo par. Usá la diagonal |
| El botón funciona a veces | Todavía no tiene debounce. Es normal, se arregla en el montaje 3 |
| No pasa nada de nada | ¿El GND llega a la fila `−`? ¿La fila `−` está cortada al medio? |
| No sube el código | Mantené `BOOT` apretado cuando empieza la subida. Si sigue, probá otro cable USB: muchos son de solo carga |
| El monitor serie muestra símbolos raros | Baudrate: tiene que ser 115200 |

---

## Parte 4 — Montaje 2: los dos buzzers (día 3)

Sumá al montaje 1, no desarmes nada.

**Necesitás:** buzzer activo · buzzer pasivo · 2 jumpers

```
Buzzer ACTIVO:   pata +  → GPIO 25      pata −  → GND
Buzzer PASIVO:   pata +  → GPIO 26      pata −  → GND
```

Sin resistencia: consumen poco y el pin del ESP32 los banca.

**Qué vas a observar:** el activo suena con solo darle tensión. El pasivo **no suena** con
`digitalWrite` — es solo una membrana, vos tenés que generarle la onda con `tone()`.

Esa diferencia es PWM: prender y apagar un pin muy rápido. Al buzzer pasivo lo hace vibrar,
a un LED lo atenúa, a un servo le indica un ángulo. Mismo mecanismo, tres usos — lo vas a
reencontrar en s05.

---

## Parte 5 — Montaje 3: panel completo (día 4-7)

El proyecto de la semana. Ahora sí desarmá y rearmá prolijo.

| Componente | Pin | Nota |
|---|---|---|
| Sensor de llama (`DO`) | GPIO 35 | VCC a **3.3V** |
| Botón (silencio/rearme) | GPIO 16 | diagonal, pull-up por software |
| LED verde + 220Ω | GPIO 27 | |
| LED amarillo + 220Ω | GPIO 14 | |
| LED rojo + 220Ω | GPIO 13 | |
| Buzzer pasivo | GPIO 26 | |

### El sensor de llama

```
Sensor de llama          ESP32
  VCC   →   3.3V      ← 3.3V, no 5V
  GND   →   GND
  DO    →   GPIO 35
  AO    →   (sin conectar)
```

**Por qué 3.3V y no 5V:** este módulo entrega en `DO` el mismo voltaje con el que lo
alimentás. Con 5V te manda 5V a un GPIO que tolera 3.3V máximo. Alimentándolo a 3.3V el
problema no existe.

**GPIO 35 es solo entrada y no tiene pull-up interno** — perfecto acá, porque el módulo tiene
salida propia y no necesita ninguno.

### Los tres LEDs

```
GPIO 27 ── [220Ω] ── LED verde(+)     LED(−) ── GND
GPIO 14 ── [220Ω] ── LED amarillo(+)  LED(−) ── GND
GPIO 13 ── [220Ω] ── LED rojo(+)      LED(−) ── GND
```

Usá la fila `−` como GND común de los tres: un solo cable al ESP32.

### Verificación antes de enchufar

- [ ] Ningún cable va a `5V` ni a `VIN`
- [ ] Los tres LEDs tienen su resistencia de 220Ω
- [ ] La pata larga de cada LED mira hacia la resistencia
- [ ] El botón está en diagonal
- [ ] El sensor de llama está a **3.3V**
- [ ] El GND del ESP32 llega a la fila `−`
- [ ] Nada se toca entre sí

---

## Antes de desarmar

📷 **Foto del cableado y video de 20 segundos funcionando**, a [`media/`](media/).

Los componentes se reutilizan la semana que viene, así que este circuito deja de existir.
La foto es lo único que queda — y es lo que va al portfolio.

Después, tres cosas para cerrar:

1. Completar la tabla de componentes del [`README.md`](README.md) de este proyecto
2. Anotar en [`docs/inventario.md`](../../docs/inventario.md) lo que descubriste de tu kit
   (cuál buzzer es cuál, tipo de módulo RGB)
3. Agregar las filas de máquina de estados, debounce y loop no bloqueante en
   [`docs/patrones.md`](../../docs/patrones.md)
