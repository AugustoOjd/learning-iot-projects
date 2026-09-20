# Extensiones: Modbus, LoRaWAN y TinyML

Tres tecnologías que el roadmap base no cubre y que no hay que ignorar. Ninguna necesita
rehacer nada: las tres se enchufan al pipeline MQTT que construís en s03.

Están ordenadas por retorno para el mercado de LATAM.

---

## 1. Modbus RTU sobre RS485

> **La de mayor retorno de las tres.** Es el idioma de la industria instalada, y casi nadie
> que viene de software lo conoce.

### Qué es

Un protocolo maestro-esclavo de 1979 que corre sobre serie (RS485). El maestro pide
"dame el registro 40001 del esclavo 3", el esclavo responde 16 bits. No hay descubrimiento,
ni seguridad, ni nada moderno — y por eso sigue vivo: es trivial de implementar y funciona
sobre dos cables a 1200 metros.

- **Modbus RTU**: sobre serie/RS485. El que te importa.
- **Modbus TCP**: el mismo protocolo sobre Ethernet. Más fácil, menos común en campo.

### Dónde se usa

| Equipo | Qué le podés leer |
|---|---|
| **Medidores de energía** | Consumo, tensión, corriente, factor de potencia, armónicos |
| **Variadores de frecuencia (VFD)** | RPM, torque, fallas, horas de servicio. Y podés comandarlos |
| **PLC** | Cualquier registro que el integrador haya expuesto |
| **Controladores de temperatura** | Setpoint, proceso, estado del lazo |
| **Balanzas industriales, caudalímetros, sensores 4-20mA con cabeza Modbus** | Lectura directa |

### Casos de uso reales

1. **Gateway Modbus → MQTT.** Leés un medidor de energía de un tablero y publicás el consumo
   en tu broker. Esto *es* un producto comercial que se vende hoy: empresas que quieren ver
   su consumo eléctrico sin cambiar el tablero.
2. **Monitoreo de una bomba con variador.** El VFD ya sabe las RPM, la corriente y las fallas;
   vos solo las traducís a MQTT. Cero sensores nuevos.
3. **Modernizar un PLC viejo.** El cliente tiene una línea de producción de 2005 que funciona
   perfecto y no quiere tocarla. Le colgás un ESP32 que lee Modbus y le das un dashboard.
   Riesgo cero para el cliente, valor alto.

### Qué necesitás

| Ítem | Precio | Nota |
|---|---|---|
| Módulo MAX485 | ~$3 | Convierte UART del ESP32 a RS485 diferencial |
| Un esclavo para probar | — | Un medidor barato, o simulá uno con `diagslave` en la PC |

**Librerías:** `ModbusMaster` o `eModbus` (Arduino) · `umodbus` (MicroPython) ·
`pymodbus` (Python, para el lado servidor y para simular esclavos).

### Proyecto propuesto

**s13 — Gateway Modbus→MQTT.** Encaja después de s11. Leés registros de un esclavo por RS485,
los normalizás a JSON y los publicás con el mismo esqueleto de `shared/Conectividad`. Agrega
el patrón *polling con timeout y reintentos*, que es distinto del modelo de eventos que venís
usando.

---

## 2. LoRaWAN

> Cuando el sensor está a kilómetros y no hay WiFi ni electricidad.

### Qué es

Primero, una distinción que confunde a todo el mundo:

- **LoRa** = la modulación de radio. Punto a punto, como ESP-NOW pero con mucho más alcance.
- **LoRaWAN** = la red completa: nodos → gateways → servidor de red → tu aplicación.

Alcance de 2 a 15 km con consumo bajísimo. El precio: **muy poco ancho de banda**. Payloads de
decenas de bytes y límites legales de *duty cycle* (en Europa, 1% del tiempo al aire). Mandás
unos pocos bytes cada varios minutos, y nada más.

### Dónde se usa

| Sector | Caso |
|---|---|
| **Agro** | Humedad de suelo distribuida en hectáreas, estaciones meteorológicas, tranqueras |
| **Smart city** | Parking, alumbrado, contenedores de residuos, calidad de aire |
| **Utilities** | Lectura remota de medidores de agua y gas |
| **Ganadería y logística** | Tracking de animales y de activos |
| **Minería y petróleo** | Sensores en sitios sin infraestructura |

### Cuándo NO usarlo

Video, audio, cualquier cosa que necesite más de ~50 bytes por minuto, o latencia baja. Si
necesitás mandar datos seguido, LoRaWAN es la herramienta equivocada.

### Cómo se compara con lo que ya vas a saber

| | ESP-NOW (s11) | LoRaWAN |
|---|---|---|
| Alcance | 100-200 m | 2-15 km |
| Infraestructura | ninguna | gateway + servidor de red |
| Payload | 250 bytes | ~50 bytes, con duty cycle |
| Costo por nodo | ~$5 | ~$15-20 |
| Cuándo | una casa, un galpón, un patio | un campo, una ciudad |

La arquitectura es **la misma que aprendés en s11**: nodos dormidos que despiertan, mandan
poquito y vuelven a dormir, contra un gateway enchufado. Solo cambia la radio y la escala.

### Qué necesitás

Una placa con SX1276/SX1278 integrado — Heltec WiFi LoRa 32 o TTGO LoRa32 (~$15-20). Traen
ESP32 + radio LoRa + pantalla OLED en la misma plaqueta.

**The Things Network** (TTN) es una red comunitaria gratuita: si hay un gateway cerca tuyo,
publicás sin montar infraestructura. Si no, tu propio gateway sale ~$100.

**Librerías:** `MCCI LoRaWAN LMIC` o `RadioLib` (Arduino).

---

## 3. TensorFlow Lite Micro (TinyML)

> Real, pero mucho más angosto de lo que se vende. Leé primero el baño de realidad.

### Qué es y qué no es

**TensorFlow** entrena modelos y corre en tu PC o en la nube: necesita gigabytes. **Nunca**
corre en un ESP32.

**TensorFlow Lite Micro** ejecuta *inferencia* de un modelo ya entrenado y reducido a
20-200 KB. Eso sí entra en el chip. El flujo completo:

```
Datos etiquetados → entrenás en la PC/nube → cuantizás a int8
                 → exportás como array de C → compila dentro del firmware
```

El dispositivo **no aprende**. Ejecuta un modelo congelado.

### Baño de realidad

**El 95% de los proyectos de IoT no necesitan ML.** Un umbral con histéresis —lo que aprendés
en s02— resuelve la mayoría de lo que la gente cree que necesita una red neuronal. Y un
umbral se explica, se audita y se ajusta; un modelo no.

Vale la pena solo cuando se cumple alguna de estas:

1. **El dato crudo es demasiado para transmitir.** Vibración a 1 kHz o audio no se mandan por
   MQTT. Corrés el modelo local y mandás la conclusión: 2 bytes en vez de 2 MB.
2. **El patrón no se puede expresar como umbral.** "Este motor suena mal" no es un número.
3. **Necesitás decidir sin conectividad y con baja latencia.**

### Casos de uso reales

| Caso | Qué detecta | Sector |
|---|---|---|
| **Mantenimiento predictivo por vibración** ⭐ | Un rodamiento que empieza a fallar cambia su firma de vibración **semanas** antes de romperse | Industrial. El caso estrella |
| **Keyword spotting** | Una palabra clave, sin mandar audio a la nube | Consumo, accesibilidad |
| **Reconocimiento de gestos** | Movimientos con acelerómetro | Wearables, interfaces |
| **Anomalía en series temporales** | Consumo de corriente fuera de patrón | Energía, seguridad |
| **Visión muy simple** (ESP32-CAM) | Presencia, conteo de personas, ocupación | Retail, edificios |

### Qué necesitás con tu kit

⚠️ **Tu módulo de sonido no sirve para esto.** Es un comparador LM393 que dice "hubo ruido
fuerte", no un micrófono que entregue audio muestreado. Para TinyML de audio necesitás un
micrófono I2S real.

| Ítem | Precio | Habilita |
|---|---|---|
| **MPU6050** (acelerómetro + giróscopo) | ~$5 | Vibración y gestos. **El mejor punto de entrada** |
| INMP441 (micrófono I2S) | ~$3 | Audio, keyword spotting |
| ESP32-CAM | ~$8 | Visión |

El MPU6050 ya está en la lista de compras opcionales del roadmap.

### Cómo empezar sin escribir TensorFlow

**[Edge Impulse](https://edgeimpulse.com)** es el camino corto: conectás el dispositivo,
grabás muestras etiquetadas desde el navegador, entrenás con un par de clics y te exporta
una librería de Arduino lista para compilar. Gratis para proyectos personales.

### Proyecto propuesto

**s14 — Detección de falla de bomba por vibración.** Se enchufa directo a s05: ya tenés una
bomba comandada por relay. Pegás el MPU6050 al motor, grabás vibración en estado sano y en
estado forzado, entrenás un clasificador y publicás el veredicto por MQTT.

Es la versión con ML de la **verificación de actuador** que ya hacés en s05 con el sensor de
sonido — y la comparación entre las dos es exactamente el tipo de criterio que se valora:
*cuándo alcanza un umbral y cuándo hace falta un modelo*.

---

## Orden sugerido

Si tuvieras que elegir uno solo: **Modbus**. Es el más barato (~$3), el que más se pide en
LATAM, y el único que te abre la puerta al IoT industrial, donde están los sueldos.

LoRaWAN en segundo lugar si te interesa agro o smart city. TinyML al final — es el más
llamativo y el de menor demanda real.
