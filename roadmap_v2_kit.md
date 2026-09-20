# Roadmap IoT v2 — Kit HEMMEL TEK-002 (NodeMCU ESP-32S)

**Para**: desarrollador de software que arranca en hardware
**Duración**: 12 semanas · 15-20 hs/semana · ~240-300 horas
**Hardware**: tu kit + ~$28 en extras
**Resultado honesto**: sistema IoT completo funcionando end-to-end + portfolio de junior con proyectos propios. No "firmware engineer senior" — eso lleva años.

---

## Índice

1. [Antes de enchufar nada](#antes-de-enchufar-nada)
2. [Pinout maestro](#pinout-maestro)
3. [Por qué el software va en la semana 3](#por-qué-el-software-va-en-la-semana-3)
4. [Semana 1 — Panel de alarma](#semana-1--panel-de-alarma)
5. [Semana 2 — Sensores analógicos](#semana-2--sensores-analógicos)
6. [Semana 3 — Pipeline a la nube](#semana-3--pipeline-a-la-nube)
7. [Semana 4 — I2C: pantalla y reloj](#semana-4--i2c-pantalla-y-reloj)
8. [Semana 5 — Actuadores](#semana-5--actuadores)
9. [Semana 6 — SPI y control de acceso](#semana-6--spi-y-control-de-acceso)
10. [Semana 7 — Expansión de I/O](#semana-7--expansión-de-io)
11. [Semana 8 — Firmware que no se cuelga](#semana-8--firmware-que-no-se-cuelga)
12. [Semana 9 — Energía y autonomía](#semana-9--energía-y-autonomía)
13. [Semana 10 — Producción: OTA y TLS](#semana-10--producción-ota-y-tls)
14. [Semana 11 — Multi-nodo](#semana-11--multi-nodo)
15. [Semana 12 — Producto entregable](#semana-12--producto-entregable)
16. [Compras extra](#compras-extra)
17. [Cuando algo no anda](#cuando-algo-no-anda)
18. [Anexo A — Catálogo del kit](#anexo-a--catálogo-del-kit)

---

## Antes de enchufar nada

Estas seis reglas te ahorran las seis frustraciones más caras. Leelas ahora, no en la semana 6.

### 1. El RC522 (RFID) es 3.3V ÚNICAMENTE

Es el módulo más caro del kit. Conectar su VCC a 5V lo destruye de forma permanente e inmediata. **VCC → 3.3V. Siempre.**

### 2. ADC2 deja de funcionar cuando prende el WiFi

El ESP32 tiene dos conversores analógicos. El ADC2 comparte hardware con la radio WiFi, así que en cuanto llamás `WiFi.begin()`, cualquier `analogRead()` sobre esos pines devuelve basura o cuelga.

```
❌ ADC2 (inutilizables con WiFi): GPIO 0, 2, 4, 12, 13, 14, 15, 25, 26, 27
✅ ADC1 (siempre funcionan):      GPIO 32, 33, 34, 35, 36, 39
```

Todo lo analógico de tu kit (LM35, LDR, nivel de agua, sonido, joystick, potenciómetro) va sobre ADC1. Sin excepción.

### 3. GPIO 34, 35, 36 y 39 son SOLO ENTRADA

No pueden ser salida y **no tienen resistencia pull-up interna**. Un botón conectado ahí no funciona sin una resistencia externa de 10K. Son perfectos para sensores analógicos, inútiles para LEDs.

### 4. GPIO 6, 7, 8, 9, 10 y 11 no existen para vos

Están conectados a la memoria flash del chip. Usarlos hace que la placa no arranque. En el header de 38 pines aparecen, pero ignoralos.

### 5. Pines "strapping": cuidado al bootear

| Pin | Condición al arrancar | Consecuencia si la violás |
|---|---|---|
| GPIO 0 | Debe estar HIGH (libre) | Si está a GND, entra en modo flasheo |
| GPIO 2 | Debe estar LOW o libre | Puede no bootear |
| GPIO 12 | **Debe estar LOW** | Si lo pones HIGH, el chip configura mal el voltaje de flash y no arranca |
| GPIO 15 | Debe estar HIGH | Si está a GND, silencia el log de arranque |

Regla práctica: **no uses GPIO 12 para nada** en este kit. Tenés pines de sobra.

### 6. Motores y relay nunca se alimentan desde el ESP32

Un pin GPIO entrega 40mA. Un servo SG90 en esfuerzo pide 700mA. Un stepper con ULN2003 pide 250mA continuos.

```
Fuente 5V/2A ──┬── VIN del ESP32
               ├── VCC del servo / ULN2003 / relay
               └── GND ─── GND del ESP32  ← el GND SIEMPRE se une
```

El conector de batería de 9V del kit sirve para alimentar el ESP32 solo (por VIN), pero **no** para mover motores. Una pila de 9V colapsa en segundos con un stepper.

---

## Pinout maestro

Esta asignación evita todos los conflictos y strapping. Usala desde el día 1 y no la cambies: cuando llegues a la semana 12 vas a poder tener casi todo conectado a la vez.

### Buses (fijos, no los muevas)

| Función | Pin | Nota |
|---|---|---|
| I2C SDA | GPIO 21 | LCD1602-I2C, RTC |
| I2C SCL | GPIO 22 | mismos dos cables para todos |
| SPI SCK | GPIO 18 | RC522 |
| SPI MISO | GPIO 19 | RC522 |
| SPI MOSI | GPIO 23 | RC522 |
| SPI CS (SDA del RC522) | GPIO 5 | |
| SPI RST | GPIO 17 | |

### Analógicos (ADC1, solo entrada)

| Sensor | Pin | Semana |
|---|---|---|
| LM35DZ (temperatura) | GPIO 36 | 2 |
| Fotorresistencia (LDR) | GPIO 39 | 2 |
| Potenciómetro 10K | GPIO 34 | 2 |
| Sensor nivel de agua | GPIO 34 | 5 (reemplaza al potenciómetro) |
| Sensor de sonido (AO) | GPIO 35 | 5 |
| Joystick VRx / VRy | GPIO 32 / 33 | 5 |

### Digitales

| Componente | Pin | Nota |
|---|---|---|
| LED onboard | GPIO 2 | ya viene soldado |
| LED rojo / amarillo / verde | GPIO 13 / 14 / 27 | con resistencia 220Ω |
| Botón 1 / 2 | GPIO 16 / 4 | `INPUT_PULLUP`, otra pata a GND |
| Buzzer activo | GPIO 25 | `digitalWrite` |
| Buzzer pasivo | GPIO 26 | PWM / `tone()` |
| DHT11 | GPIO 15 | con pull-up 10K a 3.3V |
| Sensor de llama (DO) | GPIO 35 | digital, alternativo al analógico |
| Sensor de inclinación | GPIO 33 | `INPUT_PULLUP` |
| Receptor infrarrojo | GPIO 16 | |
| Relay (IN) | GPIO 27 | VCC del relay a 5V |
| Servo SG90 | GPIO 13 | alimentación externa 5V |
| Stepper ULN2003 IN1-IN4 | GPIO 32, 33, 25, 26 | alimentación externa 5V |
| 74HC595 DS / SHCP / STCP | GPIO 23, 18, 5 | comparte pines con SPI |
| Teclado 4x4 (filas) | GPIO 13, 14, 27, 26 | |
| Teclado 4x4 (columnas) | GPIO 25, 33, 32, 4 | |

Algunos pines se repiten entre semanas — está bien, no vas a tener todo conectado al mismo tiempo hasta la semana 12, y ahí elegís el subconjunto de tu proyecto final.

---

## Por qué el software va en la semana 3

La mayoría de los roadmaps de IoT ponen WiFi y nube en la semana 8. Para vos eso está al revés.

Venís de software: el final del pipeline (broker, base de datos, dashboard, API) es tu zona de confort. Si lo dejás para el final, pasás siete semanas haciendo ejercicios sueltos que no van a ningún lado, y esa es exactamente la etapa donde la gente abandona.

Con este orden, en la semana 3 ya tenés un gráfico de temperatura real, actualizándose solo, en un dashboard. A partir de ahí **cada sensor nuevo que aprendas se enchufa a algo que ya existe y ya funciona**. Todo lo que agregás importa.

El costo es que la semana 3 va a ser fea: código bloqueante, sin reconexión, credenciales hardcodeadas. Está perfecto. La semana 8 existe justamente para volver y arreglar todo eso, y para entonces vas a entender *por qué* cada arreglo es necesario, porque lo vas a haber sufrido.

---

## Semana 1 — Panel de alarma

> **Caso real**: detector de incendio con sirena y luces. Es literalmente lo que hace un panel de alarma comercial, con menos certificaciones.

**Componentes**: sensor de llama, sensor de sonido, 3 LEDs, 2 buzzers, 2 botones, resistencias 220Ω y 10K.

### 1.1 — Blink y el pull-up (día 1-2)

Empezá con el blink de siempre sobre GPIO 2, pero pasá rápido a lo que importa: el botón.

```cpp
const int PIN_LED   = 13;
const int PIN_BOTON = 16;

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_BOTON, INPUT_PULLUP);  // ← clave
}

void loop() {
  // Con INPUT_PULLUP el pin está en HIGH cuando el botón está suelto,
  // y cae a LOW cuando lo apretás (porque conecta el pin a GND).
  bool apretado = (digitalRead(PIN_BOTON) == LOW);
  digitalWrite(PIN_LED, apretado);
  delay(50);
}
```

**Por qué `INPUT_PULLUP` y no `INPUT`**: un pin configurado como `INPUT` sin nada conectado es una antena. Flota entre 0 y 3.3V captando ruido eléctrico y leés valores aleatorios. El pull-up interno lo ancla a 3.3V mediante una resistencia de ~45K, y el botón lo tira a GND. Es el error #1 de todo principiante y la razón por la que "mi botón funciona a veces".

### 1.2 — Los dos buzzers: qué es PWM en 2 minutos (día 3)

Tu kit trae buzzer **activo** y **pasivo**. Probá los dos con el mismo código y vas a entender PWM sin teoría.

```cpp
const int BUZZER_ACTIVO = 25;
const int BUZZER_PASIVO = 26;

void setup() {
  pinMode(BUZZER_ACTIVO, OUTPUT);
  pinMode(BUZZER_PASIVO, OUTPUT);
}

void loop() {
  // El activo tiene un oscilador adentro: con darle 3.3V ya suena.
  digitalWrite(BUZZER_ACTIVO, HIGH);
  delay(500);
  digitalWrite(BUZZER_ACTIVO, LOW);
  delay(500);

  // El pasivo NO tiene oscilador. Con digitalWrite no suena nada:
  // es solo una membrana. Vos tenés que generarle la onda.
  tone(BUZZER_PASIVO, 440);   // La 440 Hz
  delay(500);
  tone(BUZZER_PASIVO, 880);   // La una octava arriba
  delay(500);
  noTone(BUZZER_PASIVO);
  delay(500);
}
```

Eso es PWM: prender y apagar un pin muy rápido. Al buzzer pasivo lo hace vibrar a esa frecuencia; a un LED lo hace verse más tenue; a un servo le indica un ángulo. Mismo mecanismo, tres usos.

> `tone()` está disponible desde el core ESP32 3.x. Si usás el core 2.x, reemplazá por `ledcWriteTone(canal, frecuencia)` previo `ledcSetup`.

### 1.3 — Máquina de estados de alarma (día 4-7)

Acá está el proyecto real de la semana. Cuatro estados: reposo, alerta, alarma disparada, silenciada.

```cpp
const int PIN_LLAMA   = 35;  // salida digital del sensor de llama
const int PIN_BOTON   = 16;  // botón de silencio / rearme
const int LED_VERDE   = 27;
const int LED_AMARILLO= 14;
const int LED_ROJO    = 13;
const int BUZZER      = 26;

enum Estado { REPOSO, ALERTA, DISPARADA, SILENCIADA };
Estado estado = REPOSO;
unsigned long entradaEstado = 0;

// Debounce sin bloquear
bool botonApretado() {
  static unsigned long ultimoCambio = 0;
  static bool ultimoEstado = HIGH;
  static bool estadoEstable = HIGH;

  bool lectura = digitalRead(PIN_BOTON);
  if (lectura != ultimoEstado) {
    ultimoCambio = millis();
    ultimoEstado = lectura;
  }
  if (millis() - ultimoCambio > 50) {
    if (estadoEstable != lectura) {
      estadoEstable = lectura;
      if (estadoEstable == LOW) return true;  // flanco de bajada
    }
  }
  return false;
}

void cambiarA(Estado nuevo) {
  estado = nuevo;
  entradaEstado = millis();
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LLAMA, INPUT);
  pinMode(PIN_BOTON, INPUT_PULLUP);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  cambiarA(REPOSO);
}

void loop() {
  bool hayFuego = (digitalRead(PIN_LLAMA) == LOW);  // el módulo es activo-bajo
  bool boton = botonApretado();
  unsigned long enEstado = millis() - entradaEstado;

  // Apagar todo y que cada estado prenda lo suyo
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_AMARILLO, LOW);
  digitalWrite(LED_ROJO, LOW);

  switch (estado) {
    case REPOSO:
      digitalWrite(LED_VERDE, HIGH);
      noTone(BUZZER);
      if (hayFuego) cambiarA(ALERTA);
      break;

    case ALERTA:
      // Confirmación: el sensor tiene que seguir activo 2 segundos.
      // Esto elimina los falsos positivos por un reflejo o un chispazo.
      digitalWrite(LED_AMARILLO, HIGH);
      if (!hayFuego)          cambiarA(REPOSO);
      else if (enEstado > 2000) cambiarA(DISPARADA);
      break;

    case DISPARADA:
      digitalWrite(LED_ROJO, (millis() / 250) % 2);  // parpadeo sin delay()
      tone(BUZZER, (millis() / 400) % 2 ? 880 : 660);  // sirena bitonal
      if (boton) cambiarA(SILENCIADA);
      break;

    case SILENCIADA:
      digitalWrite(LED_ROJO, HIGH);  // fijo: recordá que hubo un evento
      noTone(BUZZER);
      // Solo vuelve a reposo si el fuego se fue Y alguien rearma
      if (!hayFuego && boton) cambiarA(REPOSO);
      break;
  }
}
```

**Lo que importa acá** no es el código, son tres decisiones de diseño que aparecen en todo producto real:

- **Estado ALERTA con confirmación temporal**: ningún sistema serio dispara con una sola lectura. Un sensor barato tiene falsos positivos; exigir persistencia los filtra.
- **SILENCIADA ≠ REPOSO**: silenciar la sirena no borra el evento. El LED queda fijo hasta que alguien rearma explícitamente. Perder eventos es inaceptable en alarmas.
- **Cero `delay()`**: todo el parpadeo y la sirena salen de `millis()`. Un `delay(250)` acá significa que el botón de silencio no responde durante 250ms. Multiplicá eso por 10 tareas y tenés un dispositivo que se siente roto.

### Criterio de terminado — Semana 1

- [ ] El botón funciona 20 de 20 veces (si no, es debounce o pull-up)
- [ ] La alarma no dispara con un destello corto, sí con fuego sostenido 2s
- [ ] No hay un solo `delay()` en `loop()`
- [ ] Podés explicar la diferencia entre buzzer activo y pasivo
- [ ] Está en GitHub

---

## Semana 2 — Sensores analógicos

> **Caso real**: monitor de sala de servidores / heladera de farmacia. Temperatura y luz, con alerta por umbral.

**Componentes**: LM35DZ, 3 fotorresistencias, potenciómetro 10K, resistencias 10K.

### 2.1 — ADC y el divisor de tensión (día 1-2)

Arrancá con el potenciómetro, que es el sensor analógico más fácil de entender porque lo movés con la mano.

```cpp
const int PIN_POT = 34;  // ADC1

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);          // 0..4095
  analogSetAttenuation(ADC_11db);    // rango completo ~0-3.3V
}

void loop() {
  int   crudo = analogRead(PIN_POT);
  float volts = (crudo / 4095.0) * 3.3;

  Serial.printf("crudo=%4d  volts=%.3f\n", crudo, volts);
  delay(200);
}
```

Ahora la fotorresistencia. Una LDR no genera voltaje: **cambia su resistencia** con la luz (mucha luz → poca resistencia). Para leerla necesitás convertir resistencia en voltaje, y eso es un divisor de tensión:

```
3.3V ──── LDR ────┬──── GPIO 39
                  │
                 10K
                  │
                 GND
```

Cuando hay luz, la LDR baja su resistencia y el punto medio sube hacia 3.3V. Es la Ley de Ohm aplicada, y es el circuito más usado de toda la electrónica: cualquier sensor resistivo (LDR, termistor, sensor de humedad de suelo, tu sensor de nivel de agua) se lee así.

### 2.2 — LM35: temperatura de verdad (día 3-4)

El LM35 es superior al DHT11 para aprender porque es puramente analógico: entrega **10 mV por cada grado Celsius**. A 25°C te da 250mV. Sin librería, sin protocolo, solo física.

```
LM35 (mirándolo de frente, patas hacia abajo):
  pata izquierda  → +5V (VIN)   ← necesita 4V mínimo, NO lo alimentes con 3.3V
  pata central    → GPIO 36
  pata derecha    → GND
```

```cpp
const int PIN_LM35 = 36;

float leerTemperatura() {
  // Promediamos 16 lecturas: el ADC del ESP32 es ruidoso.
  // Esto es un filtro de media móvil, la forma más barata de
  // ganar precisión sin gastar un peso.
  uint32_t suma = 0;
  for (int i = 0; i < 16; i++) {
    suma += analogReadMilliVolts(PIN_LM35);
    delayMicroseconds(200);
  }
  float mv = suma / 16.0;
  return mv / 10.0;  // 10 mV por grado
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.printf("Temperatura: %.2f C\n", leerTemperatura());
  delay(1000);
}
```

**`analogReadMilliVolts()` en vez de `analogRead()`**: el ADC del ESP32 es notoriamente no lineal, sobre todo cerca de 0V y de 3.3V. Espressif graba una curva de calibración en cada chip durante la fabricación, y esta función la usa. Con `analogRead()` crudo tu LM35 puede errar 3-4 grados. Con esta, menos de uno. Es una línea de código y es la diferencia entre un juguete y un instrumento.

### 2.3 — Monitor con umbrales e histéresis (día 5-7)

Junta todo: temperatura + luz + alarma. Y acá aparece el concepto que separa el código de laboratorio del código de producción.

```cpp
const float UMBRAL_ALTO = 28.0;
const float UMBRAL_BAJO = 26.5;  // ← 1.5 grados de diferencia. A propósito.
bool alarmaActiva = false;

void loop() {
  float t = leerTemperatura();

  // HISTÉRESIS: la alarma se prende a 28 pero se apaga recién a 26.5.
  // Sin esto, con la temperatura oscilando alrededor de 28.0 el buzzer
  // se prendería y apagaría varias veces por segundo. En un relay
  // controlando un compresor, eso lo destruye en días.
  if (!alarmaActiva && t > UMBRAL_ALTO) {
    alarmaActiva = true;
    Serial.println("ALARMA: temperatura alta");
  } else if (alarmaActiva && t < UMBRAL_BAJO) {
    alarmaActiva = false;
    Serial.println("Normalizada");
  }

  digitalWrite(LED_ROJO, alarmaActiva);
  delay(1000);
}
```

La histéresis (o "banda muerta") es de esas cosas que no están en los tutoriales y sí en todos los productos. Anotala.

### Criterio de terminado — Semana 2

- [ ] Podés dibujar el divisor de tensión de memoria y explicar por qué hace falta
- [ ] Tu LM35 coincide con un termómetro real dentro de ±1°C
- [ ] Entendés por qué el LM35 va a 5V y no a 3.3V
- [ ] Tu alarma tiene histéresis y podés explicar qué pasaría sin ella
- [ ] Todos tus sensores analógicos están en GPIO 32-39

---

## Semana 3 — Pipeline a la nube

> **Caso real**: telemetría. Esta es la semana donde tu experiencia de software vale oro y donde el proyecto deja de ser un juguete de escritorio.

**Componentes**: solo el ESP32 y el LM35 de la semana pasada.

Objetivo: que la temperatura de tu escritorio aparezca en un gráfico que podés abrir desde el celular.

### 3.1 — WiFi (día 1)

```cpp
#include <WiFi.h>

const char* SSID = "TU_RED";
const char* PASS = "TU_PASSWORD";

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);

  Serial.print("Conectando");
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }
  Serial.printf("\nOK. IP: %s  RSSI: %d dBm\n",
                WiFi.localIP().toString().c_str(), WiFi.RSSI());
}

void loop() {}
```

Mirá el RSSI. Entre -30 y -60 dBm es excelente; por debajo de -80 vas a tener desconexiones constantes. Es tu primer dato de ingeniería de radio y va a explicar el 90% de tus problemas futuros de conectividad.

> Nota: acabás de romper el ADC2. Si tenías algo analógico en GPIO 4, 25, 26 o 27, dejó de funcionar en este preciso momento. Por eso la regla de la semana 0.

### 3.2 — El atajo: ESPHome (día 2)

Antes de escribir MQTT a mano, dedicá una tarde a ver cómo se ve cuando ya está resuelto. Instalá **Home Assistant** (Docker o una Raspberry) y **ESPHome**, y flasheá esto:

```yaml
esphome:
  name: monitor-sala

esp32:
  board: esp32dev

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

api:
logger:
ota:

sensor:
  - platform: adc
    pin: GPIO36
    name: "Temperatura sala"
    update_interval: 30s
    attenuation: 11db
    filters:
      - multiply: 100.0   # 10mV/°C → °C
    unit_of_measurement: "°C"
```

En 20 líneas de YAML tenés: WiFi con reconexión automática, descubrimiento en Home Assistant, gráficos históricos, alertas, y **actualizaciones OTA**. Es el nivel de servicio al que vas a apuntar cuando lo escribas a mano.

No es hacer trampa: es tu línea de base. Ahora escribilo vos y entendé qué hace ESPHome por debajo.

### 3.3 — MQTT a mano (día 3-5)

Levantá un broker Mosquitto local (`docker run -p 1883:1883 eclipse-mosquitto`) o usá `broker.hivemq.com` para probar.

```cpp
#include <WiFi.h>
#include <PubSubClient.h>

const char* SSID = "TU_RED";
const char* PASS = "TU_PASSWORD";
const char* MQTT_HOST = "192.168.1.100";
const int   MQTT_PORT = 1883;

const char* TOPIC_TELEMETRIA = "casa/sala/telemetria";
const char* TOPIC_COMANDO    = "casa/sala/comando";
const char* TOPIC_ESTADO     = "casa/sala/estado";  // LWT

WiFiClient   wifi;
PubSubClient mqtt(wifi);

String clientId;
unsigned long ultimoEnvio = 0;
const unsigned long INTERVALO = 10000;

void onMensaje(char* topic, byte* payload, unsigned int len) {
  String msg;
  for (unsigned int i = 0; i < len; i++) msg += (char)payload[i];
  Serial.printf("[%s] %s\n", topic, msg.c_str());

  if (msg == "led_on")  digitalWrite(LED_ROJO, HIGH);
  if (msg == "led_off") digitalWrite(LED_ROJO, LOW);
}

void conectarMqtt() {
  while (!mqtt.connected()) {
    Serial.print("MQTT...");
    // El Last Will and Testament: si el dispositivo se cae sin avisar,
    // el broker publica "offline" por nosotros. Sin esto no tenés forma
    // de distinguir "está bien pero no tiene novedades" de "se murió".
    if (mqtt.connect(clientId.c_str(), nullptr, nullptr,
                     TOPIC_ESTADO, 1, true, "offline")) {
      Serial.println(" conectado");
      mqtt.publish(TOPIC_ESTADO, "online", true);  // retained
      mqtt.subscribe(TOPIC_COMANDO);
    } else {
      Serial.printf(" falló rc=%d, reintento en 5s\n", mqtt.state());
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_ROJO, OUTPUT);

  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) delay(300);

  clientId = "esp32-" + WiFi.macAddress();
  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setCallback(onMensaje);
}

void loop() {
  if (!mqtt.connected()) conectarMqtt();
  mqtt.loop();  // ← imprescindible: procesa entrantes y mantiene el keepalive

  if (millis() - ultimoEnvio >= INTERVALO) {
    ultimoEnvio = millis();

    char json[160];
    snprintf(json, sizeof(json),
      "{\"temp\":%.2f,\"rssi\":%d,\"uptime\":%lu,\"heap\":%u}",
      leerTemperatura(), WiFi.RSSI(), millis() / 1000, ESP.getFreeHeap());

    mqtt.publish(TOPIC_TELEMETRIA, json);
    Serial.println(json);
  }
}
```

Tres cosas que hacen que esto no sea un ejemplo de tutorial:

- **LWT (Last Will and Testament)**: el broker anuncia tu muerte. Es la única forma de detectar un dispositivo caído sin hacer polling.
- **`heap` en la telemetría**: publicar la memoria libre te deja ver una fuga de memoria en un gráfico. Si el heap baja monótonamente durante días, tenés un bug. Es el diagnóstico más valioso y más barato del firmware embebido.
- **Client ID desde la MAC**: dos dispositivos con el mismo client ID se desconectan mutuamente en loop infinito. Es un bug que tarda horas en diagnosticarse.

### 3.4 — Dashboard (día 6-7)

Elegí uno:

| Stack | Esfuerzo | Cuándo |
|---|---|---|
| **Node-RED** | 1 hora | Lo más rápido. Flow visual, dashboard incluido |
| **Home Assistant** | 2 horas | Si ya lo tenés de ESPHome. Mejor para casa |
| **Telegraf + InfluxDB + Grafana** | 4 horas | El stack profesional. El que va en el CV |

Recomendación: hacé Node-RED ahora para tener el gráfico hoy, y montá el stack de Grafana en la semana 12 como parte del proyecto final.

### Criterio de terminado — Semana 3

- [ ] Ves un gráfico de temperatura de las últimas 24hs desde el celular
- [ ] Podés prender un LED publicando en un topic MQTT
- [ ] Al desenchufar el ESP32, el estado pasa a "offline" solo (LWT)
- [ ] Corrió 24 horas seguidas sin colgarse
- [ ] Miraste el gráfico de heap y es plano, no descendente

**Hito**: tenés un sistema IoT completo. Todo lo que viene se enchufa acá.

---

## Semana 4 — I2C: pantalla y reloj

> **Caso real**: datalogger de cadena de frío con hora real. El dispositivo tiene que saber *cuándo* pasó cada cosa, y mostrarlo sin depender de la nube.

**Componentes**: LCD 1602, módulo RTC, DHT11, resistencia 10K.

### 4.1 — Por qué existe I2C (día 1)

Ya tenés dos periféricos que quieren pantalla y reloj. Con pines paralelos, el LCD1602 solo se come 6 GPIO. I2C resuelve eso: **dos cables para todos los dispositivos**.

```
GPIO 21 (SDA) ──┬──────────┬──────────
GPIO 22 (SCL) ──┼──┬───────┼──┬───────
                │  │       │  │
              LCD1602     RTC       (y todo lo que agregues)
```

Cada dispositivo tiene una dirección única de 7 bits. El maestro (ESP32) grita la dirección al bus; solo el que se reconoce contesta. Es exactamente service discovery, pero en cobre.

**Escaneá el bus antes que nada.** Las direcciones dependen del fabricante y este paso te ahorra horas:

```cpp
#include <Wire.h>

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  Serial.println("Escaneando I2C...");

  int n = 0;
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.printf("  Dispositivo en 0x%02X\n", addr);
      n++;
    }
  }
  Serial.printf("%d dispositivo(s)\n", n);
}

void loop() {}
```

Referencia de lo que deberías ver: LCD I2C en `0x27` o `0x3F`, DS3231 en `0x68`, DS1307 en `0x68`, EEPROM del módulo RTC en `0x57`.

> **Si no aparece nada**: fijate si tu LCD1602 tiene una plaquita soldada atrás con 4 pines (GND, VCC, SDA, SCL). Si tiene 16 pines pelados, es paralelo y no habla I2C — necesitás un backpack PCF8574 (~$2) o conectarlo con la librería `LiquidCrystal` usando 6 GPIO. El backpack vale la pena.

### 4.2 — LCD + RTC (día 2-4)

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>
#include <DHT.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  // usá la dirección que te dio el scanner
RTC_DS3231 rtc;
DHT dht(15, DHT11);                   // ← DHT11, no DHT22

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);

  lcd.init();
  lcd.backlight();

  if (!rtc.begin()) {
    lcd.print("RTC no detectado");
    while (1) delay(100);
  }
  // Solo la primera vez, o si se quedó sin pila:
  if (rtc.lostPower()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  dht.begin();
}

void loop() {
  DateTime ahora = rtc.now();
  float t = dht.readTemperature();
  float h = dht.readHumidity();

  if (isnan(t) || isnan(h)) {
    Serial.println("DHT11 sin respuesta");
    delay(2000);
    return;
  }

  lcd.setCursor(0, 0);
  lcd.printf("%02d/%02d %02d:%02d:%02d",
             ahora.day(), ahora.month(),
             ahora.hour(), ahora.minute(), ahora.second());

  lcd.setCursor(0, 1);
  lcd.printf("%.1fC  %.0f%%   ", t, h);  // espacios finales borran residuos

  delay(2000);  // el DHT11 no acepta más de 1 lectura por segundo
}
```

**Sobre el DHT11**: es el sensor más limitado del kit. Rango 0-50°C con ±2°C de error y humedad 20-80% con ±5%. Para aprender el protocolo está perfecto; para medir en serio usá el LM35 (temperatura) y anotá "cambiar a DHT22 o SHT31" en tu lista de mejoras. Reconocer las limitaciones de tus componentes *es* ingeniería.

### 4.3 — Logging persistente con NVS (día 5-7)

Un datalogger que pierde todo al desenchufarse no es un datalogger. El ESP32 tiene NVS (Non-Volatile Storage), una key-value store en la flash que sobrevive reinicios y cortes.

```cpp
#include <Preferences.h>

Preferences prefs;

struct Registro {
  uint32_t epoch;
  int16_t  tempCentesimas;  // 2534 = 25.34°C. Enteros: la flash es cara.
  uint8_t  humedad;
};

const int MAX_REGISTROS = 200;

void guardarRegistro(const Registro& r) {
  prefs.begin("datalog", false);
  int idx = prefs.getInt("idx", 0);

  char clave[16];
  snprintf(clave, sizeof(clave), "r%d", idx);
  prefs.putBytes(clave, &r, sizeof(r));

  prefs.putInt("idx", (idx + 1) % MAX_REGISTROS);  // buffer circular
  prefs.end();
}
```

Dos decisiones que vas a repetir en cada proyecto embebido:

- **Enteros en vez de float**: guardar centésimas como `int16_t` usa 2 bytes; un `float` usa 4 y trae problemas de precisión. En un dispositivo con memoria contada, esto se nota.
- **Buffer circular**: la flash tiene ~100.000 ciclos de escritura por sector. Un buffer circular reparte el desgaste y nunca se llena. Si escribís cada 10 segundos sin pensar, quemás la flash en meses.

**Integración**: cuando vuelva el MQTT de la semana 3, publicá también los registros guardados mientras estuvo sin conexión. Eso es *store and forward*, y es la diferencia entre un datalogger y un sensor que pierde datos cada vez que se cae el WiFi.

### Criterio de terminado — Semana 4

- [ ] El scanner I2C encuentra tus dos dispositivos y sabés sus direcciones
- [ ] La hora sobrevive al desenchufe (si no, cambiá la pila del RTC)
- [ ] Los últimos registros sobreviven al reinicio
- [ ] Al reconectar, los datos acumulados se envían al broker

---

## Semana 5 — Actuadores

> **Caso real**: control de tanque de agua + persiana motorizada. Dos casos que se venden todos los días.

**Componentes**: relay, sensor de nivel de agua, servo SG90, stepper + ULN2003, joystick, receptor IR + control.

### 5.1 — Relay y control de bomba (día 1-2)

```
Módulo relay:
  VCC → 5V (VIN)      ← no al 3.3V, el electroimán necesita 5V
  GND → GND
  IN  → GPIO 27
```

**Primero averiguá si tu relay es activo-alto o activo-bajo.** Es lo primero que hay que probar y depende del módulo:

```cpp
const int PIN_RELAY = 27;

void setup() {
  Serial.begin(115200);
  pinMode(PIN_RELAY, OUTPUT);
}

void loop() {
  digitalWrite(PIN_RELAY, HIGH);
  Serial.println("Pin en HIGH — ¿escuchás el click? ¿se prendió el LED del módulo?");
  delay(3000);
  digitalWrite(PIN_RELAY, LOW);
  Serial.println("Pin en LOW");
  delay(3000);
}
```

Anotá cuál de los dos activa el relay y definí una constante `RELAY_ACTIVO` para no volver a pensarlo nunca.

Control de tanque completo, con las tres protecciones que necesita:

```cpp
const int PIN_NIVEL = 34;   // ADC1
const bool RELAY_ACTIVO = LOW;  // ajustá según tu módulo

const int NIVEL_BAJO  = 1200;   // calibrá con tu sensor en agua real
const int NIVEL_ALTO  = 2800;
const unsigned long MAX_BOMBEO = 5UL * 60 * 1000;  // 5 minutos

bool bombaEncendida = false;
unsigned long inicioBombeo = 0;
bool bloqueoSeguridad = false;

void setBomba(bool on) {
  digitalWrite(PIN_RELAY, on ? RELAY_ACTIVO : !RELAY_ACTIVO);
  bombaEncendida = on;
  if (on) inicioBombeo = millis();
}

void loop() {
  int nivel = analogRead(PIN_NIVEL);

  if (bloqueoSeguridad) {
    setBomba(false);
    return;  // requiere intervención humana. A propósito.
  }

  // 1. Histéresis: no oscila en el umbral
  if (!bombaEncendida && nivel < NIVEL_BAJO) {
    setBomba(true);
  } else if (bombaEncendida && nivel > NIVEL_ALTO) {
    setBomba(false);
  }

  // 2. Timeout: si bombea 5 minutos sin llenar, algo está mal
  //    (bomba en seco, cañería rota, sensor desconectado).
  //    Una bomba en seco se destruye en minutos.
  if (bombaEncendida && millis() - inicioBombeo > MAX_BOMBEO) {
    bloqueoSeguridad = true;
    Serial.println("SEGURIDAD: timeout de bombeo. Bomba bloqueada.");
  }

  // 3. Sensor desconectado: lectura imposible → no confíes en ella
  if (nivel < 20) {
    bloqueoSeguridad = true;
    Serial.println("SEGURIDAD: sensor desconectado.");
  }

  delay(500);
}
```

Esas tres protecciones son la diferencia entre un proyecto de tutorial y algo que dejarías conectado a una bomba real. **La pregunta que define al ingeniero embebido es "¿qué pasa si esto falla?"**, y las respuestas van en el código.

> El sensor de nivel del kit es resistivo y se corroe si lo dejás energizado sumergido. En un producto real se lo alimenta desde un GPIO que solo se prende para medir. Buen ejercicio: implementalo.

### 5.2 — Servo con joystick (día 3-4)

```cpp
#include <ESP32Servo.h>   // ← NO <Servo.h>, esa librería no compila en ESP32

Servo servo;
const int PIN_SERVO = 13;
const int PIN_JOY_X = 32;  // ADC1

void setup() {
  Serial.begin(115200);
  servo.setPeriodHertz(50);            // los servos analógicos trabajan a 50Hz
  servo.attach(PIN_SERVO, 500, 2400);  // ancho de pulso en microsegundos
}

void loop() {
  int x = analogRead(PIN_JOY_X);           // 0..4095
  int angulo = map(x, 0, 4095, 0, 180);
  angulo = constrain(angulo, 0, 180);
  servo.write(angulo);
  delay(20);
}
```

`attach(pin, 500, 2400)` importa: el estándar dice 1000-2000µs, pero los SG90 clones suelen tener rango real de 500-2400µs. Si tu servo no llega a los extremos o hace ruido al tope, es esto.

**Alimentación**: el servo va a 5V externo con GND común. Si lo colgás del pin 5V del ESP32 alimentado por USB, la caída de tensión al arrancar el motor reinicia la placa. Vas a ver reinicios aleatorios y vas a culpar al código.

### 5.3 — Stepper y control IR (día 5-7)

El stepper 28BYJ-48 con driver ULN2003 es tu primer actuador de **posición precisa**: a diferencia del servo (rango 180°), da vueltas completas y mantiene la posición exacta.

```cpp
#include <Stepper.h>
#include <IRremote.hpp>

const int PASOS_POR_VUELTA = 2048;  // 28BYJ-48 con reductora 64:1
// OJO con el orden de los pines: IN1, IN3, IN2, IN4 (no es un error)
Stepper motor(PASOS_POR_VUELTA, 32, 25, 33, 26);

const int PIN_IR = 16;

void setup() {
  Serial.begin(115200);
  motor.setSpeed(10);  // RPM. Más de ~15 y pierde pasos.
  IrReceiver.begin(PIN_IR, ENABLE_LED_FEEDBACK);
}

void loop() {
  if (IrReceiver.decode()) {
    uint16_t cmd = IrReceiver.decodedIRData.command;
    Serial.printf("IR comando: 0x%02X\n", cmd);

    // Primero corré esto y anotá el código de cada tecla de TU control.
    // Los códigos varían entre controles remotos.
    switch (cmd) {
      case 0x18: motor.step( PASOS_POR_VUELTA / 4); break;  // reemplazá
      case 0x52: motor.step(-PASOS_POR_VUELTA / 4); break;  // por los tuyos
    }
    IrReceiver.resume();
  }
}
```

**Limitación importante**: `motor.step()` es bloqueante. Un cuarto de vuelta a 10 RPM tarda 1.5 segundos durante los cuales el ESP32 no hace absolutamente nada — ni MQTT, ni sensores, ni botones. Es un problema real y no tiene solución elegante dentro de este diseño. Anotalo: **la semana 8 lo resuelve con FreeRTOS**, moviendo el motor a otra tarea en el segundo núcleo. Que te duela ahora es lo que hace que la solución tenga sentido después.

### Criterio de terminado — Semana 5

- [ ] Sabés si tu relay es activo-alto o activo-bajo
- [ ] El control de tanque tiene histéresis + timeout + detección de sensor caído
- [ ] El servo llega a 0° y 180° sin ruido ni vibración
- [ ] Tenés mapeados los códigos IR de tu control
- [ ] Comprobaste que el stepper bloquea el `loop()` y entendés por qué es un problema

---

## Semana 6 — SPI y control de acceso

> **Caso real**: control de acceso con registro de fichaje. Es un producto que se vende hoy, en cualquier oficina o gimnasio.

**Componentes**: módulo RFID RC522, llavero y tarjeta, teclado 4x4, relay, LCD, RTC.

### 6.1 — SPI vs I2C (día 1)

Tercer protocolo, tercera filosofía:

| | I2C | SPI |
|---|---|---|
| Cables | 2 (SDA, SCL) | 4 (SCK, MISO, MOSI) + 1 CS por dispositivo |
| Velocidad | 100-400 kHz | 10+ MHz |
| Selección | por dirección en el bus | por línea CS física |
| Para | sensores lentos, muchos dispositivos | pantallas, SD, RFID, datos rápidos |

I2C ahorra pines, SPI da velocidad. El RC522 usa SPI porque mueve bloques de datos de la tarjeta.

### 6.2 — RFID (día 2-4)

```
RC522        ESP32
  VCC   →    3.3V     ⚠️ NUNCA 5V. Lo quemás y no hay vuelta atrás.
  RST   →    GPIO 17
  GND   →    GND
  MISO  →    GPIO 19
  MOSI  →    GPIO 23
  SCK   →    GPIO 18
  SDA   →    GPIO 5    (es el chip select, mal nombrado por el fabricante)
```

```cpp
#include <SPI.h>
#include <MFRC522.h>

MFRC522 rfid(5, 17);  // CS, RST

void setup() {
  Serial.begin(115200);
  SPI.begin(18, 19, 23);
  rfid.PCD_Init();
  Serial.println("Acercá una tarjeta...");
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial())   return;

  String uid;
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (rfid.uid.uidByte[i] < 0x10) uid += "0";
    uid += String(rfid.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();
  Serial.printf("UID: %s\n", uid.c_str());

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}
```

Anotá los UID de tu llavero y tu tarjeta: son tus dos credenciales de prueba.

### 6.3 — Sistema completo (día 5-7)

Junta RFID + teclado + relay + LCD + RTC + MQTT en un control de acceso funcional:

```cpp
#include <Preferences.h>

Preferences store;

bool autorizado(const String& uid) {
  store.begin("acceso", true);   // read-only
  bool ok = store.isKey(uid.c_str());
  store.end();
  return ok;
}

void registrarEvento(const String& uid, bool permitido) {
  DateTime t = rtc.now();
  char json[200];
  snprintf(json, sizeof(json),
    "{\"uid\":\"%s\",\"permitido\":%s,\"ts\":%lu}",
    uid.c_str(), permitido ? "true" : "false", (unsigned long)t.unixtime());

  Serial.println(json);
  if (mqtt.connected()) {
    mqtt.publish("acceso/eventos", json);
  } else {
    // Sin conexión: guardar en NVS y enviar después.
    // Un control de acceso NUNCA puede perder eventos.
    guardarEventoPendiente(json);
  }
}

void abrirPuerta() {
  digitalWrite(PIN_RELAY, RELAY_ACTIVO);
  delay(3000);                    // aceptable acá: es una acción atómica
  digitalWrite(PIN_RELAY, !RELAY_ACTIVO);
}
```

Requisitos del sistema (esto es una especificación, cumplila):

1. Tarjeta autorizada → abre 3 segundos, LCD muestra el nombre, log a MQTT
2. Tarjeta desconocida → buzzer de error, LED rojo, log igual (los intentos fallidos son el dato más interesante para seguridad)
3. Teclado con PIN maestro como respaldo si se pierde la tarjeta
4. **Sin conexión funciona igual**: la whitelist vive en NVS, los eventos se acumulan y se envían al reconectar
5. Alta de tarjetas nuevas por MQTT (topic `acceso/alta`) sin reprogramar nada

El punto 4 es el que separa esto de un tutorial. Un control de acceso que no abre la puerta porque se cayó internet es un producto inaceptable. **La lógica crítica vive en el dispositivo; la nube es para observabilidad y administración, nunca en el camino crítico.** Esta es probablemente la lección de arquitectura más importante de todo el roadmap, y es la que más le cuesta a la gente que viene de backend.

### Criterio de terminado — Semana 6

- [ ] Lee UID de llavero y tarjeta de forma confiable
- [ ] Whitelist persiste en NVS entre reinicios
- [ ] Funciona con el WiFi apagado
- [ ] Al volver la conexión, los eventos acumulados se envían
- [ ] Podés dar de alta una tarjeta publicando en MQTT

---

## Semana 7 — Expansión de I/O

> **Caso real**: panel indicador industrial. Y la respuesta a "me quedé sin pines".

**Componentes**: 74HC595, display 8x8, display 4 dígitos, display 1 dígito, LEDs.

### 7.1 — El 74HC595 (día 1-3)

Con todo lo de la semana 6 conectado ya casi no te quedan pines. El 74HC595 convierte **3 pines en 8 salidas**, y se pueden encadenar: dos chips = 16 salidas con los mismos 3 pines.

```
74HC595      ESP32
  DS  (14) → GPIO 23   datos
  SHCP(11) → GPIO 18   clock (desplaza un bit)
  STCP(12) → GPIO 5    latch (publica los 8 bits a la vez)
  OE  (13) → GND       output enable, activo-bajo
  MR  (10) → 3.3V      master reset, activo-bajo
  VCC (16) → 3.3V
  GND (8)  → GND
```

```cpp
const int DS = 23, SHCP = 18, STCP = 5;

void escribir595(uint8_t valor) {
  digitalWrite(STCP, LOW);                    // congelar salidas
  shiftOut(DS, SHCP, MSBFIRST, valor);        // desplazar 8 bits
  digitalWrite(STCP, HIGH);                   // publicar de golpe
}

void setup() {
  pinMode(DS, OUTPUT); pinMode(SHCP, OUTPUT); pinMode(STCP, OUTPUT);
}

void loop() {
  for (int i = 0; i < 8; i++) {
    escribir595(1 << i);   // un LED que "corre"
    delay(100);
  }
}
```

El latch (`STCP`) es el detalle elegante: mientras desplazás los bits las salidas quedan congeladas, así que nunca se ven estados intermedios. Es un doble buffer, el mismo concepto que en gráficos.

### 7.2 — Displays y multiplexado (día 4-7)

**Antes de codear, identificá qué te vino**, porque cambia todo:

| Display | Si tiene... | Entonces |
|---|---|---|
| 4 dígitos | 4 pines (VCC, GND, CLK, DIO) | Es TM1637 → librería `TM1637Display`, fácil |
| 4 dígitos | 12 pines | Es crudo → multiplexado a mano o con el 595 |
| Matriz 8x8 | 5 pines (VCC, GND, DIN, CS, CLK) | Tiene MAX7219 → librería `LedControl`, fácil |
| Matriz 8x8 | 16 pines | Es cruda → necesita dos 74HC595 |

Si te vino cruda, el multiplexado es el ejercicio:

```cpp
// Una matriz 8x8 cruda tiene 64 LEDs pero solo podés prender una fila
// a la vez. El truco es prender fila 1, luego 2, luego 3... tan rápido
// que el ojo las ve todas juntas. Persistencia de la visión.
// A >60Hz de refresco completo no se ve parpadeo.

uint8_t buffer[8] = {
  0b00111100,
  0b01000010,
  0b10100101,
  0b10000001,
  0b10100101,
  0b10011001,
  0b01000010,
  0b00111100
};  // una carita

void refrescar() {
  for (int fila = 0; fila < 8; fila++) {
    apagarFilas();                 // evita "ghosting" entre filas
    escribirColumnas(buffer[fila]);
    activarFila(fila);
    delayMicroseconds(1500);       // 8 filas × 1.5ms = 12ms ≈ 83Hz
  }
}
```

Ese `apagarFilas()` antes de cambiar es obligatorio: sin él, cada fila se ilumina un instante con los datos de la anterior y la imagen sale sucia. Se llama *ghosting* y es el bug clásico del multiplexado.

**Proyecto de la semana**: panel de estado que muestra en la matriz un ícono según el estado del sistema (OK / alerta / sin conexión), en el display de 4 dígitos la temperatura actual, y usa el 595 para una barra de LEDs de nivel del tanque. Todo alimentado por MQTT desde la semana 3.

### Criterio de terminado — Semana 7

- [ ] Controlás 8 LEDs con 3 pines
- [ ] Identificaste qué variante de displays te vino
- [ ] Si es multiplexado: no se ve parpadeo ni ghosting
- [ ] El panel refleja datos reales que llegan por MQTT

---

## Semana 8 — Firmware que no se cuelga

> **Caso real**: la diferencia entre un prototipo y un producto. Acá volvés sobre todo lo hecho y lo arreglás.

**Componentes**: ninguno nuevo. Todo el trabajo es software.

Esta es la semana más importante del roadmap y la que menos aparece en los tutoriales.

### 8.1 — FreeRTOS: las dos tareas (día 1-3)

El ESP32 tiene dos núcleos y un sistema operativo de tiempo real ya corriendo. Tu `loop()` es solo una tarea de baja prioridad en el núcleo 1.

Esto resuelve el stepper bloqueante de la semana 5:

```cpp
QueueHandle_t colaMotor;

struct ComandoMotor { int pasos; };

void tareaMotor(void* param) {
  ComandoMotor cmd;
  for (;;) {
    // Bloquea esta tarea hasta que llegue un comando.
    // Bloquear una tarea NO bloquea las demás: el scheduler
    // le da el CPU a otra. Esta es la idea central de un RTOS.
    if (xQueueReceive(colaMotor, &cmd, portMAX_DELAY) == pdTRUE) {
      motor.step(cmd.pasos);
    }
  }
}

void tareaTelemetria(void* param) {
  for (;;) {
    publicarTelemetria();
    vTaskDelay(pdMS_TO_TICKS(10000));  // NO delay(): cede el CPU
  }
}

void setup() {
  colaMotor = xQueueCreate(5, sizeof(ComandoMotor));

  xTaskCreatePinnedToCore(
    tareaMotor,      // función
    "motor",         // nombre (aparece en los dumps de crash)
    4096,            // stack en bytes — si te quedás corto: crash
    nullptr,         // parámetro
    1,               // prioridad (0 = mínima)
    nullptr,         // handle
    0                // núcleo 0 (el 1 lo usa Arduino)
  );

  xTaskCreatePinnedToCore(tareaTelemetria, "telem", 8192, nullptr, 1, nullptr, 1);
}

void loop() {
  // Ahora el loop queda libre para lo que tiene que responder rápido:
  // botones, RFID, teclado.
  atenderEntradas();
  vTaskDelay(pdMS_TO_TICKS(10));
}
```

Reglas que te van a morder si no las respetás:

- **`vTaskDelay()` en vez de `delay()`** dentro de tareas: `delay()` en algunas versiones ocupa el CPU sin cederlo.
- **Nunca compartas variables entre tareas sin protección.** Usá colas (`xQueue`) para pasar datos, o mutex si tenés que compartir estado. Una variable modificada desde dos núcleos sin sincronizar produce corrupción intermitente, el peor tipo de bug.
- **Dimensioná el stack**: 4096 bytes alcanza para tareas simples; si usás `String`, JSON o TLS, subí a 8192. Un stack chico se manifiesta como reinicio aleatorio.

### 8.2 — Watchdog (día 4)

Tu dispositivo va a estar en un techo o adentro de un tablero. Si se cuelga, nadie va a ir a apretar reset.

```cpp
#include <esp_task_wdt.h>

void setup() {
  esp_task_wdt_config_t cfg = {
    .timeout_ms = 10000,
    .idle_core_mask = 0,
    .trigger_panic = true   // si expira, reinicia
  };
  esp_task_wdt_init(&cfg);
  esp_task_wdt_add(NULL);   // vigilar esta tarea
}

void loop() {
  esp_task_wdt_reset();     // "sigo vivo"
  hacerTrabajo();
}
```

Si `hacerTrabajo()` se cuelga más de 10 segundos, el chip se reinicia solo. Un dispositivo que se reinicia y vuelve a funcionar es infinitamente mejor que uno colgado.

**Regla**: el reset del watchdog va en un solo lugar, en el flujo principal. Si lo esparcís por todos lados, siempre hay alguno que se ejecuta y el watchdog deja de servir.

### 8.3 — Reconexión y diagnóstico (día 5-7)

Reescribí la conexión de la semana 3 para que sobreviva a la realidad:

```cpp
unsigned long ultimoIntento = 0;
int backoff = 1000;
const int BACKOFF_MAX = 60000;

void mantenerConexion() {
  if (WiFi.status() == WL_CONNECTED && mqtt.connected()) {
    backoff = 1000;   // todo bien, resetear
    return;
  }
  if (millis() - ultimoIntento < (unsigned long)backoff) return;
  ultimoIntento = millis();

  if (WiFi.status() != WL_CONNECTED) {
    WiFi.disconnect();
    WiFi.begin(SSID, PASS);
  } else if (!mqtt.connect(clientId.c_str(), nullptr, nullptr,
                           TOPIC_ESTADO, 1, true, "offline")) {
    // falló, aumentar espera
  }

  // Backoff exponencial: no martillees el router cada 100ms.
  // Si el WiFi está caído, reintentar 10 veces por segundo solo
  // consume batería y satura el canal para todos.
  backoff = min(backoff * 2, BACKOFF_MAX);
}
```

Y agregá a la telemetría los datos que te van a permitir diagnosticar a distancia:

```cpp
snprintf(json, sizeof(json),
  "{\"heap\":%u,\"heap_min\":%u,\"uptime\":%lu,\"rssi\":%d,\"reset\":%d}",
  ESP.getFreeHeap(),          // memoria libre ahora
  ESP.getMinFreeHeap(),       // mínimo histórico ← detecta fugas
  millis() / 1000,
  WiFi.RSSI(),
  (int)esp_reset_reason());   // por qué se reinició la última vez
```

`esp_reset_reason()` te dice si el último reinicio fue por corte de energía, por watchdog, por panic o por OTA. Sin ese dato, diagnosticar un dispositivo remoto es adivinar.

### Criterio de terminado — Semana 8

- [ ] El stepper se mueve sin frenar el resto del sistema
- [ ] Cortás el WiFi 10 minutos, lo devolvés y reconecta solo con backoff
- [ ] Un `while(1)` de prueba dispara el watchdog y reinicia
- [ ] Publicás `heap_min` y `reset_reason`
- [ ] **72 horas continuas sin intervención** ← el test que importa

---

## Semana 9 — Energía y autonomía

> **Caso real**: sensor a batería en un lugar sin enchufe. Cambia por completo cómo se diseña.

**Componentes**: conector de batería 9V, multímetro.

### 9.1 — Medir el consumo (día 1-2)

Poné el multímetro en modo corriente **en serie** con la alimentación. Números de referencia para un ESP32:

| Estado | Consumo | Autonomía con 500mAh |
|---|---|---|
| WiFi transmitiendo | 160-260 mA | ~2 horas |
| WiFi conectado, idle | 80-100 mA | ~5 horas |
| WiFi apagado, CPU activa | 30-40 mA | ~14 horas |
| **Deep sleep** | **10-150 µA** | **meses** |

La conclusión es brutal y define la arquitectura: **un ESP32 con WiFi permanente no funciona a batería.** Punto. La única estrategia viable es dormir casi todo el tiempo.

### 9.2 — Deep sleep (día 3-5)

```cpp
#include <esp_sleep.h>

// Esta variable sobrevive al deep sleep: vive en la RTC RAM,
// que sigue alimentada mientras el resto del chip se apaga.
RTC_DATA_ATTR int ciclos = 0;

const uint64_t INTERVALO_US = 15ULL * 60 * 1000000;  // 15 minutos

void setup() {
  Serial.begin(115200);
  ciclos++;

  // Todo el "programa" va acá. Después del deep sleep el chip
  // arranca de cero y vuelve a ejecutar setup(). loop() nunca corre.
  float t = leerTemperatura();

  conectarWiFi();
  publicar(t);
  mqtt.disconnect();
  WiFi.disconnect(true);

  Serial.printf("Ciclo %d, durmiendo 15 min\n", ciclos);
  Serial.flush();

  esp_sleep_enable_timer_wakeup(INTERVALO_US);
  esp_deep_sleep_start();   // no retorna nunca
}

void loop() {}   // inalcanzable
```

El cambio mental: **con deep sleep no existe el `loop()`**. Tu programa es un `setup()` que se ejecuta, hace su trabajo y se suicida. Todo el estado que quieras conservar va en `RTC_DATA_ATTR` o en NVS.

Lo que domina el consumo es el tiempo de conexión WiFi (típicamente 2-5 segundos). Optimizarlo es lo que multiplica la autonomía:

```cpp
// Guardar el canal y el BSSID del router en RTC RAM ahorra el escaneo.
// Baja el tiempo de conexión de ~4s a ~1s: 4x más autonomía.
RTC_DATA_ATTR uint8_t canal = 0;
RTC_DATA_ATTR uint8_t bssid[6];
RTC_DATA_ATTR bool tieneCache = false;

void conectarWiFi() {
  if (tieneCache) WiFi.begin(SSID, PASS, canal, bssid);
  else            WiFi.begin(SSID, PASS);

  unsigned long t0 = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - t0 > 15000) {     // timeout: no te quedes sin batería
      esp_sleep_enable_timer_wakeup(INTERVALO_US);
      esp_deep_sleep_start();
    }
    delay(50);
  }

  canal = WiFi.channel();
  memcpy(bssid, WiFi.BSSID(), 6);
  tieneCache = true;
}
```

### 9.3 — Presupuesto energético (día 6-7)

Calculalo en una planilla. Es el entregable de la semana:

```
Despertar + leer sensor:   1.0 s × 40 mA   = 0.011 mAh
Conectar WiFi:             1.5 s × 180 mA  = 0.075 mAh
Publicar MQTT:             0.5 s × 180 mA  = 0.025 mAh
Deep sleep:              897.0 s × 0.05 mA = 0.012 mAh
                                       Total = 0.123 mAh por ciclo

Ciclos por día: 96 (cada 15 min)
Consumo diario: 11.8 mAh
Batería 18650 de 2500 mAh × 0.8 (derrateo real) = 2000 mAh útiles
Autonomía: 2000 / 11.8 ≈ 169 días ≈ 5.6 meses
```

**Advertencia sobre la pila de 9V**: tiene ~500mAh y un regulador lineal desperdicia como calor todo lo que va de 9V a 3.3V (más del 60% de la energía). Para un proyecto a batería en serio, usá 18650 de 3.7V con un regulador de bajo dropout, o dos pilas AA. La pila de 9V del kit sirve para pruebas, no para autonomía.

### Criterio de terminado — Semana 9

- [ ] Mediste el consumo real en cada estado con el multímetro
- [ ] Tu nodo despierta, publica y duerme
- [ ] Cachear el BSSID redujo medibemente el tiempo de conexión
- [ ] Tenés la planilla del presupuesto energético
- [ ] Hay timeout en la conexión (nunca despierto para siempre)

---

## Semana 10 — Producción: OTA y TLS

> **Caso real**: 20 dispositivos instalados y hay que actualizarlos sin ir a buscarlos.

### 10.1 — OTA (día 1-3)

```cpp
#include <ArduinoOTA.h>

void setup() {
  // ... WiFi ...

  ArduinoOTA.setHostname("sensor-sala");
  ArduinoOTA.setPassword("una-clave-de-verdad");

  ArduinoOTA
    .onStart([]() {
      // CRÍTICO: parar todo lo que escriba en flash o mueva motores
      detenerTareas();
      Serial.println("OTA iniciando");
    })
    .onProgress([](unsigned int hecho, unsigned int total) {
      Serial.printf("OTA %u%%\r", (hecho * 100) / total);
    })
    .onError([](ota_error_t err) {
      Serial.printf("OTA error %u\n", err);
    });

  ArduinoOTA.begin();
}

void loop() {
  ArduinoOTA.handle();
  // ...
}
```

**Las dos reglas que evitan que dejes un dispositivo muerto e inaccesible:**

1. **Nunca subas firmware sin OTA incluido.** Una actualización que quita el OTA es la última que vas a poder hacer sin ir físicamente. Poné el OTA en tu plantilla base y no lo saques nunca.
2. **Probá el firmware nuevo en un dispositivo de banco antes de tocar los instalados.** Siempre.

El ESP32 tiene particiones OTA duales (`ota_0` y `ota_1`): la nueva imagen se escribe en la partición inactiva y solo se cambia el arranque si la descarga se verificó completa. Un corte de luz a mitad de la actualización no te deja el dispositivo ladrillo. Verificá que tu esquema de particiones tenga espacio para las dos (`Tools → Partition Scheme → Minimal SPIFFS` si te quedás corto).

### 10.2 — TLS (día 4-5)

Hasta acá tu MQTT viaja en texto plano: cualquiera en la red ve tus datos y puede publicar comandos falsos.

```cpp
#include <WiFiClientSecure.h>

const char* CA_ROOT = R"EOF(
-----BEGIN CERTIFICATE-----
...el certificado de tu broker...
-----END CERTIFICATE-----
)EOF";

WiFiClientSecure tls;
PubSubClient mqtt(tls);

void setup() {
  // ... WiFi ...

  // La hora tiene que ser correcta ANTES del TLS: la validación
  // del certificado chequea fecha de expiración. Sin NTP,
  // el handshake falla con un error críptico.
  configTime(0, 0, "pool.ntp.org");
  while (time(nullptr) < 1600000000) delay(200);

  tls.setCACert(CA_ROOT);   // NO uses setInsecure() fuera de pruebas
  mqtt.setServer(MQTT_HOST, 8883);
}
```

TLS cuesta ~40KB de RAM durante el handshake y sube el stack necesario de la tarea a 8192+. Si te aparecen crashes al conectar, es eso.

### 10.3 — Provisioning y secretos (día 6-7)

Sacá las credenciales del código fuente. Un SSID y password hardcodeados significan recompilar por cada instalación, y que tu password de WiFi termine en GitHub.

```cpp
#include <WiFiManager.h>   // librería tzapu

void setup() {
  WiFiManager wm;
  // Si no puede conectarse, levanta un AP propio con un portal web
  // donde el usuario elige la red y pone la clave. Queda guardado en NVS.
  if (!wm.autoConnect("Sensor-Setup", "configurar")) {
    ESP.restart();
  }
}
```

Con esto, el mismo binario sirve para todos los dispositivos y la instalación la puede hacer alguien sin computadora.

**Checklist de seguridad mínima**, ninguno opcional:

- [ ] Credenciales en NVS, nunca en el código
- [ ] `.gitignore` con `secrets.h`
- [ ] TLS con validación de certificado (no `setInsecure()`)
- [ ] OTA con contraseña
- [ ] Cada dispositivo con credenciales MQTT propias (si uno se compromete, revocás solo ese)
- [ ] ACLs en el broker: un sensor solo publica en su topic, no en el de los demás

### Criterio de terminado — Semana 10

- [ ] Actualizaste el firmware sin cable USB
- [ ] MQTT sobre TLS validando certificado
- [ ] El WiFi se configura desde el celular, sin recompilar
- [ ] No hay ni un secreto en el repo

---

## Semana 11 — Multi-nodo

> **Caso real**: 5 sensores en una casa o un campo, donde no todos llegan al WiFi.

**Componentes**: un segundo ESP32 (~$10).

### 11.1 — ESP-NOW (día 1-4)

WiFi tiene un problema para nodos a batería: asociarse a un router tarda segundos y consume. ESP-NOW es un protocolo de Espressif que manda paquetes directo entre ESP32 **sin router, sin asociación, en milisegundos**.

| | WiFi + MQTT | ESP-NOW |
|---|---|---|
| Tiempo de envío | 2-5 s | ~5 ms |
| Consumo por mensaje | ~0.1 mAh | ~0.0002 mAh |
| Alcance | el del router | 100-200 m línea de vista |
| Payload | ilimitado | 250 bytes |
| Necesita infraestructura | sí | no |

La arquitectura que resuelve casi todos los casos reales:

```
Nodo sensor 1 (batería, deep sleep) ──┐
Nodo sensor 2 (batería, deep sleep) ──┼─ ESP-NOW ─→ Gateway (enchufado)
Nodo sensor 3 (batería, deep sleep) ──┘                    │
                                                      WiFi + MQTT
                                                           ↓
                                                        Nube
```

Los sensores despiertan 5ms, mandan y duermen: duran **años**. El gateway está enchufado y mantiene WiFi permanente. Esta topología es la respuesta correcta al 80% de los proyectos IoT reales, y no aparece en ningún roadmap de principiante.

```cpp
// --- NODO SENSOR ---
#include <esp_now.h>
#include <WiFi.h>

uint8_t MAC_GATEWAY[] = {0x24, 0x6F, 0x28, 0xAA, 0xBB, 0xCC};

typedef struct {
  uint8_t  idNodo;
  float    temperatura;
  float    humedad;
  uint16_t bateriaMv;
} Paquete;

void setup() {
  WiFi.mode(WIFI_STA);
  esp_now_init();

  esp_now_peer_info_t peer = {};
  memcpy(peer.peer_addr, MAC_GATEWAY, 6);
  peer.channel = 0;
  peer.encrypt = false;
  esp_now_add_peer(&peer);

  Paquete p = { 1, leerTemperatura(), leerHumedad(), leerBateria() };
  esp_now_send(MAC_GATEWAY, (uint8_t*)&p, sizeof(p));

  delay(50);   // dejar que salga antes de dormir
  esp_sleep_enable_timer_wakeup(15ULL * 60 * 1000000);
  esp_deep_sleep_start();
}

void loop() {}
```

```cpp
// --- GATEWAY ---
void onRecibido(const esp_now_recv_info_t* info, const uint8_t* data, int len) {
  if (len != sizeof(Paquete)) return;   // validá SIEMPRE el tamaño
  Paquete p;
  memcpy(&p, data, sizeof(p));

  char topic[64], json[160];
  snprintf(topic, sizeof(topic), "campo/nodo%d/telemetria", p.idNodo);
  snprintf(json, sizeof(json),
    "{\"temp\":%.2f,\"hum\":%.2f,\"bat_mv\":%u}",
    p.temperatura, p.humedad, p.bateriaMv);

  mqtt.publish(topic, json);
}

void setup() {
  conectarWiFi();          // el gateway sí usa WiFi normal
  esp_now_init();
  esp_now_register_recv_cb(onRecibido);
}
```

**Trampa**: ESP-NOW y WiFi comparten radio, así que el gateway tiene que estar **en el mismo canal** que su router. Fijá el canal en el router o leelo con `WiFi.channel()` y configurá los nodos igual. Si los canales no coinciden, los paquetes se pierden en silencio — sin error, sin nada. Es el bug más frustrante de ESP-NOW.

`peer.encrypt = false` está bien para probar. En producción, activá encriptación con LMK: sin eso, cualquiera con un ESP32 puede inyectar lecturas falsas en tu red.

### 11.2 — Reportar batería (día 5-7)

Un nodo a batería tiene que avisar cuánto le queda. Divisor de tensión con dos resistencias de 10K sobre ADC1, y agregalo al paquete. Configurá una alerta en el dashboard a los 3.4V (para una celda de litio).

### Criterio de terminado — Semana 11

- [ ] Dos nodos mandando por ESP-NOW al gateway
- [ ] El gateway los reenvía a MQTT y aparecen en el dashboard
- [ ] Los nodos duermen entre envíos y calculaste su autonomía
- [ ] Alerta de batería baja funcionando
- [ ] Entendés por qué los canales tienen que coincidir

---

## Semana 12 — Producto entregable

> Convertir el mejor de tus proyectos en algo que le mostrarías a un cliente.

### 12.1 — Elegí uno y hacelo bien (día 1-2)

Un proyecto terminado vale más que ocho prototipos en protoboard. Candidatos:

| Proyecto | Vende bien porque |
|---|---|
| Control de acceso RFID con fichaje | Es un producto que existe y se compra |
| Monitor de cadena de frío | Regulatorio en farmacia y gastronomía |
| Control de tanque + riego | Universal en LATAM, ahorra agua y bombas |
| Red de sensores ESP-NOW | Demuestra arquitectura, que es lo escaso |

### 12.2 — Sacarlo de la protoboard (día 3-5)

La protoboard tiene contactos que se aflojan y capacitancia parásita. Un dispositivo que se cuelga cada dos días muchas veces es un cable flojo, no un bug.

- Pasalo a **perfboard** con soldadura (si nunca soldaste: 2 horas de práctica con LEDs viejos y listo)
- Poné el ESP32 sobre **zócalos**, no soldado directo — vas a querer sacarlo
- **Un capacitor de 470µF** entre VCC y GND cerca del ESP32. Absorbe los picos de corriente al transmitir WiFi y elimina una clase entera de reinicios misteriosos
- **Borneras** para todo lo que salga del gabinete
- Gabinete plástico. Un proyecto en una caja se ve terminado; el mismo circuito colgando no

### 12.3 — Documentación (día 6-7)

Esto es lo que un empleador o cliente realmente mira. El README tiene que tener:

```markdown
# Nombre del proyecto

Una línea: qué problema resuelve y para quién.

## Demo
[GIF de 20 segundos del dispositivo funcionando]
[Captura del dashboard con datos reales]

## Arquitectura
[Diagrama: sensor → ESP32 → MQTT → InfluxDB → Grafana]

## Decisiones de diseño
- Por qué ESP-NOW y no WiFi en los nodos (autonomía: 6 meses vs 2 días)
- Por qué la whitelist vive en el dispositivo (funciona sin internet)
- Por qué histéresis de 1.5°C (evita ciclado del compresor)

## Hardware
| Componente | Modelo | Pin | Nota |

## Instalación
Pasos reproducibles, de cero a funcionando.

## Datos de operación
- Corriendo desde: [fecha]
- Uptime: X días
- Consumo medido: X mAh/día
```

La sección de **decisiones de diseño** es la más importante y la que casi nadie escribe. Cualquiera copia un tutorial; explicar *por qué* elegiste algo sobre la alternativa es lo que demuestra criterio de ingeniería. En una entrevista técnica, esa sección es la que te van a preguntar.

### Criterio de terminado — Semana 12

- [ ] Un proyecto fuera de la protoboard, en gabinete
- [ ] Funcionando de verdad más de una semana, con datos que lo prueben
- [ ] README con demo visual, diagrama y decisiones justificadas
- [ ] Podés explicar cualquier línea de tu código
- [ ] Repo público y prolijo

---

## Compras extra

Lo que el kit no trae y sí vas a necesitar:

| Ítem | Precio | Cuándo | Por qué |
|---|---|---|---|
| **Multímetro** | ~$5 | Semana 1 | Sin esto debuggeás a ciegas. El primero de la lista. |
| **Fuente 5V 2A** | ~$8 | Semana 5 | Servo y stepper no andan con USB |
| **Segundo ESP32** | ~$10 | Semana 11 | ESP-NOW necesita dos |
| Backpack I2C para LCD | ~$2 | Semana 4 | Solo si tu LCD tiene 16 pines |
| Capacitores 470µF | ~$1 | Semana 12 | Estabilidad de alimentación |
| Perfboard + estaño | ~$5 | Semana 12 | Sacarlo de la protoboard |

**Opcionales según a dónde quieras ir:**

| Ítem | Precio | Para |
|---|---|---|
| MPU6050 (IMU) | ~$5 | Detección de vibración/movimiento |
| DHT22 o SHT31 | ~$5 / $12 | Reemplazar al DHT11 con precisión real |
| DS18B20 sonda estanca | ~$3 | Medir líquidos y exteriores |
| Módulo RS485 (MAX485) | ~$3 | **Modbus RTU**: el protocolo del IoT industrial |
| Analizador lógico 8ch | ~$10 | Ver I2C y SPI de verdad cuando no andan |
| Portapilas 18650 + TP4056 | ~$5 | Proyectos a batería en serio |

Si tu objetivo es empleo en IoT industrial en LATAM, el **MAX485 + Modbus** es la compra de mayor retorno de toda la lista: es lo que hablan los medidores de energía, los variadores y los PLC, y casi nadie que viene de software lo sabe.

---

## Cuando algo no anda

### El 90% de los problemas

| Síntoma | Causa más probable |
|---|---|
| No sube el código | Mantené `BOOT` apretado al empezar la subida. Cable USB de solo carga (probá otro). Driver CP210x/CH340 faltante. |
| Serial muestra símbolos raros | Baudrate mal: tiene que ser 115200 |
| Reinicios al mover un motor | Alimentación insuficiente. Fuente externa + capacitor. |
| `analogRead()` devuelve basura | Estás en ADC2 con WiFi encendido. Mové a GPIO 32-39. |
| Botón errático | Falta `INPUT_PULLUP` o falta debounce |
| I2C no encuentra nada | SDA/SCL cruzados, sin alimentación, o el módulo no es I2C |
| RFID no lee | ¿Lo alimentaste con 5V? Ya está quemado. Verificá los 4 pines SPI. |
| Anda 2 horas y se cuelga | Fuga de memoria. Graficá `heap` en el tiempo. |
| Anda en el escritorio, falla instalado | RSSI bajo, alimentación pobre, o temperatura |
| Reinicio aleatorio sin patrón | Stack de tarea insuficiente, o `delay()` largo con watchdog activo |

### El método

1. **Serial primero.** `Serial.printf()` en cada paso. El 80% se resuelve viendo dónde deja de imprimir.
2. **Aislar.** Desconectá todo y probá el componente problemático solo, con el sketch de ejemplo de su librería.
3. **Multímetro.** ¿Hay 3.3V donde tiene que haberlos? ¿El GND está realmente unido?
4. **Continuidad.** Con el multímetro en modo continuidad, verificá cada cable. Los jumpers de kit fallan seguido.
5. **Buscar bien.** "ESP32 MFRC522 not reading" te da mejores resultados que la descripción del síntoma en tus palabras.
6. **Preguntar bien.** r/esp32 con: código mínimo que reproduce, foto del cableado, salida del serial, qué ya probaste.

### Regla de la hora

Si llevás una hora en el mismo problema, parás y hacés otra cosa. En hardware, el 100% de los problemas que sobreviven una hora son de cableado, y los encontrás en 5 minutos con la cabeza fresca. Insistir cansado es cómo la gente abandona.

---

## Expectativas honestas

Lo que este roadmap sí te da en 12 semanas:

- Fundamentos sólidos de electrónica digital y analógica
- Los tres protocolos que importan (GPIO/PWM, I2C, SPI) y ESP-NOW
- Un sistema IoT completo end-to-end con OTA y TLS
- Criterio de diseño: histéresis, timeouts, fallas seguras, operación offline
- Portfolio con proyectos propios y documentados

Lo que **no** te da, aunque otros roadmaps lo prometan:

- No sos "firmware engineer senior". Eso son años.
- No sabés diseñar PCB, ni EMC, ni certificaciones.
- No viste RTOS de verdad bajo restricciones duras, ni bare-metal sin Arduino.
- No sabés STM32, Zephyr ni sistemas críticos.

Con 12 semanas honestas quedás como **junior con portfolio propio**, que es una posición real y defendible. Es mucho mejor que llegar diciendo "hice un roadmap de 12 semanas y soy ingeniero de firmware", que es lo que promete el documento original y lo que te va a hacer quedar mal en la primera entrevista técnica.

Tu ventaja real sobre otros juniors no es el hardware: es que ya sabés arquitectura, versionado, testing y despliegue. Esa combinación sí es escasa. Apoyate ahí y sé honesto con lo otro.

---

## Anexo A — Catálogo del kit

Los 39 ítems del kit HEMMEL TEK-002, con cómo identificarlos cuando abrís la bolsa.

**Antes de empezar**: separá todo en bolsitas o en una caja con divisiones y etiquetalas. Vas a agradecerlo en la semana 6, cuando busques una resistencia de 10K entre 30 resistencias iguales a simple vista.

---

### A.1 — Base

| Ítem | Cómo lo reconocés | Notas |
|---|---|---|
| **NodeMCU ESP-32S, 38 pines** | Placa negra larga, módulo metálico cuadrado con antena serigrafiada, dos botones (`EN`/`RST` y `BOOT`) | Los pines están rotulados en la placa. **GPIO 6-11 no existen para vos** (están conectados a la flash) |
| **Cable USB-A → USB-C** | Obvio | Si no aparece el puerto serie, probá otro cable: muchos son de solo carga, sin líneas de datos |
| **Protoboard 830 puntos** | Placa blanca con agujeritos | Ver A.9 sobre cómo están conectados internamente |
| **65 jumpers** | Cables rígidos macho-macho de colores | Probá continuidad con el tester: es normal que 2-3 estén cortados por dentro |
| **10 Dupont macho-hembra** | Cables con pin de un lado y conector hembra del otro | Para conectar módulos que tienen **pines machos** a la protoboard. Los módulos (relay, RFID, RTC) los necesitan |

---

### A.2 — Pasivos

| Ítem | Cómo lo reconocés | Notas |
|---|---|---|
| **15 LEDs** | Rojo, verde, amarillo | **Pata larga = ánodo (+)**, pata corta = cátodo (−). Siempre con resistencia de 220Ω en serie |
| **30 resistencias** | Cilindros beige con bandas de color | Ver tabla de códigos abajo |
| **Potenciómetro 10K** | Perilla azul o negra, 3 patas | Extremos a 3.3V y GND, pata del medio al ADC |
| **3 fotorresistencias (LDR)** | Disco chato con un zigzag naranja en la cara | No tiene polaridad. Necesita divisor de tensión con 10K |

**Código de colores de tus resistencias:**

| Valor | Bandas | Para qué |
|---|---|---|
| **220Ω** | rojo · rojo · marrón · dorado | Limitar corriente de LEDs |
| **1KΩ** | marrón · negro · rojo · dorado | Divisores, protección de bases |
| **10KΩ** | marrón · negro · naranja · dorado | Pull-ups, divisores de LDR |

Si dudás, medilas con el tester en modo `Ω` — es más rápido y confiable que interpretar los colores bajo luz de lámpara.

---

### A.3 — Sonido

| Ítem | Cómo lo reconocés | Voltaje | Semana |
|---|---|---|---|
| **Buzzer activo** | Cilindro negro, tapa **sellada y lisa** (a veces con una etiqueta) | 3.3-5V | 1 |
| **Buzzer pasivo** | Cilindro negro, se ve **el PCB verde por abajo** | 3.3-5V | 1 |
| **Módulo sensor de sonido** | Placa con un **micrófono redondo metálico**, chip LM393 y un potenciómetro azul de ajuste | 3.3-5V | 5 |

**Cómo distinguir los buzzers con seguridad** (se parecen mucho):

1. **Por abajo**: el pasivo suele mostrar el circuito verde; el activo está sellado.
2. **Con el tester en `Ω`**: el pasivo mide ~8-16Ω (es una bobina). El activo da resistencia alta o infinita.
3. **Prueba definitiva**: dale 3.3V directo. El **activo suena** (tiene oscilador interno). El **pasivo hace un click** y nada más.

El sensor de sonido tiene salida digital (`DO`, se activa al pasar un umbral que regulás con el potenciómetro) y a veces analógica (`AO`). **No mide decibeles** — detecta "hubo un ruido fuerte". Sirve para detectar un golpe, una palmada o que arrancó una máquina, no para medir nivel sonoro.

---

### A.4 — Entrada

| Ítem | Cómo lo reconocés | Notas |
|---|---|---|
| **5 switches con tope** | Botoncito cuadrado de 4 patas + capuchón de color | Ver la trampa abajo |
| **Joystick PS2** | Palanca negra tipo PlayStation sobre PCB | 5 pines: `GND`, `+5V`, `VRx`, `VRy`, `SW`. Los dos ejes van a **ADC1** (GPIO 32/33) |
| **Teclado matriz 16 botones** | Membrana plana 4x4 con cable de 8 pines | 4 filas + 4 columnas. Librería `Keypad` |
| **Receptor infrarrojo** | Componente negro de 3 patas con **una cúpula redonda** al frente (VS1838B) | Se parece al sensor de llama. Ver A.5 |
| **Control remoto IR** | Controlcito negro chato, suele venir con la pila puesta | Sacale el plástico aislante de la pila |
| **Sensor de inclinación** | Módulo con un **cilindro metálico** (o el cilindro suelto, SW-520D) | Adentro tiene una bolita. Al inclinarlo, cierra o abre el contacto |

**La trampa del botón de 4 patas** — es el error más común y más desconcertante:

```
Un switch táctil tiene 4 patas, pero son solo 2 contactos:

   1 ●━━━━━━● 2      Las patas 1-2 están SIEMPRE unidas entre sí.
     ┊      ┊        Las patas 3-4 también.
   3 ●━━━━━━● 4      Apretar une los dos pares.

❌ Si cableás entre 1 y 2 → el botón queda "apretado" para siempre
✅ Cableá en DIAGONAL (1 y 4, o 2 y 3) → funciona siempre
```

Si tu botón parece estar siempre presionado, es esto. Confirmalo con el tester en continuidad: las patas que pitan sin apretar son un par, no las uses juntas.

**El sensor de inclinación** no dice el ángulo, es binario: inclinado o no. Se lee con `INPUT_PULLUP` igual que un botón, y **rebota igual que un botón** — necesita el mismo debounce. Casos reales: detectar que se abrió una tapa, que se volcó un equipo, o que alguien movió una caja.

---

### A.5 — Sensores

| Ítem | Cómo lo reconocés | Voltaje | Semana |
|---|---|---|---|
| **LM35DZ** | Cápsula negra semicircular de 3 patas (TO-92). **Dice "LM35DZ"** impreso | **5V** (mínimo 4V) | 2 |
| **DHT11** | Cajita **celeste** con rejilla, 3 o 4 pines | 3.3-5V | 4 |
| **Sensor de llama** | Módulo con un LED-like **oscuro/azulado inclinado**, chip LM393 y potenciómetro | 3.3-5V | 1 |
| **Sensor nivel de agua** | Placa alargada con **tiras de cobre paralelas** | 3.3-5V | 5 |

**El LM35 parece un transistor.** Es una cápsula negra de 3 patas idéntica a mil componentes. La única forma de estar seguro es leer lo que dice impreso: `LM35DZ`. Con la parte plana hacia vos y las patas hacia abajo:

```
   ┌─────────┐
   │  LM35DZ │      izquierda → +5V   (NO 3.3V: necesita 4V mínimo)
   │  (plana)│      centro    → salida analógica (GPIO 36)
   └─┬──┬──┬─┘      derecha   → GND
     1  2  3
```

**Llama vs receptor IR** — se confunden porque los dos son negros y detectan infrarrojo:

| | Sensor de llama | Receptor IR |
|---|---|---|
| Forma | Módulo (PCB) con elemento **inclinado ~60°** | Componente suelto con **cúpula redonda** |
| Pines | 3-4 (`VCC`,`GND`,`DO`,`AO`) | 3 patas peladas |
| Chip | Tiene LM393 y potenciómetro azul | Ninguno |
| Detecta | Luz IR de una llama (~760-1100nm) | Señales moduladas a 38kHz |

Si tiene potenciómetro azul de ajuste, es el de llama.

**El sensor de nivel de agua se corroe.** Funciona midiendo la resistencia entre las tiras de cobre, y el agua con corriente permanente electroliza el cobre: en semanas se degrada. En un producto real se lo alimenta desde un GPIO que solo se prende un instante para medir:

```cpp
const int PIN_ALIM_SENSOR = 26;

int leerNivel() {
  digitalWrite(PIN_ALIM_SENSOR, HIGH);  // energizar
  delay(10);                            // estabilizar
  int v = analogRead(34);
  digitalWrite(PIN_ALIM_SENSOR, LOW);   // apagar → no se corroe
  return v;
}
```

---

### A.6 — Displays

| Ítem | Cómo lo reconocés | Verificá |
|---|---|---|
| **Display 1 dígito** | 7 segmentos rojo, 10 patas | Cátodo o ánodo común |
| **Display 4 dígitos** | 4 dígitos juntos | **¿4 pines o 12?** |
| **Matriz 8x8** | Cuadrado de 64 LEDs | **¿5 pines o 16?** |
| **LCD 1602** | Pantalla verde/azul, 2 líneas de 16 caracteres | **¿4 pines o 16?** |

**Los tres chequeos que definen tu código** (hacelos antes de la semana 4):

| Display | Pines | Qué es | Librería |
|---|---|---|---|
| LCD 1602 | 4 (`GND`,`VCC`,`SDA`,`SCL`) | Tiene backpack I2C | `LiquidCrystal_I2C` ✅ |
| LCD 1602 | 16 | Paralelo crudo | `LiquidCrystal`, gasta 6 GPIO. Comprá backpack (~$2) |
| 4 dígitos | 4 (`CLK`,`DIO`,`VCC`,`GND`) | Chip TM1637 | `TM1637Display` ✅ |
| 4 dígitos | 12 | Crudo | Multiplexado a mano (semana 7) |
| Matriz | 5 (`DIN`,`CS`,`CLK`,`VCC`,`GND`) | Chip MAX7219 | `LedControl` ✅ |
| Matriz | 16 | Cruda | Necesita **dos** 74HC595 (tenés uno) |

**Cátodo común vs ánodo común** en el display de 1 dígito: poné el tester en modo diodo, una punta en un pin fijo y probá los otros. Si un pin enciende segmentos con la punta **negra**, es cátodo común. Con la **roja**, ánodo común. Cambia toda tu lógica: en cátodo común un segmento prende con `HIGH`, en ánodo común con `LOW`.

---

### A.7 — Actuadores

| Ítem | Cómo lo reconocés | Alimentación | Semana |
|---|---|---|---|
| **Servo SG90** | Cajita azul con brazos plásticos blancos | **5V externo** | 5 |
| **Motor paso a paso** | Cilindro **azul** con conector blanco de 5 pines (28BYJ-48) | **5V externo** | 5 |
| **Driver ULN2003** | PCB con 4 LEDs, conector blanco y chip DIP-16 | **5V externo** | 5 |
| **Módulo relay 1 canal** | Cubo **azul** grande + borneras a tornillo | VCC a **5V** | 5 |

**Servo SG90** — código de colores universal:

```
naranja (o amarillo) → señal (GPIO 13)
rojo                 → +5V externo
marrón (o negro)     → GND (unido al GND del ESP32)
```

**Stepper + ULN2003** — van siempre juntos, el motor no se conecta directo al ESP32:

```
ESP32 → IN1,IN2,IN3,IN4 del ULN2003 → conector blanco → motor
Fuente 5V → borneras del ULN2003 (no del ESP32)
```

El orden de pines en la librería `Stepper` es **IN1, IN3, IN2, IN4** — no es un error de tipeo, es por cómo están devanadas las bobinas. Si el motor vibra sin girar, probá permutar.

**Relay** — dos lados bien separados:

```
Lado de control (baja tensión):   VCC → 5V,  GND → GND,  IN → GPIO 27
Lado de potencia (borneras):      NO (normal abierto) · COM (común) · NC (normal cerrado)
```

⚠️ Las borneras conmutan **220V si vos lo conectás ahí**. Mientras estés aprendiendo, usá el relay solo con cargas de baja tensión (una tira de LEDs de 12V, un ventilador de PC). Antes de tocar 220V: desenchufar siempre, nunca trabajar con el circuito energizado, y aislar bien. Si no estás seguro, no lo hagas — el click del relay ya te confirma que tu lógica anda.

---

### A.8 — Módulos

| Ítem | Cómo lo reconocés | Voltaje | Semana |
|---|---|---|---|
| **74HC595N** | Chip negro DIP-16, **dice "74HC595"** | 3.3V | 7 |
| **Módulo RFID RC522** | PCB **azul** grande con antena espiralada plana, 8 pines | **3.3V ⚠️** | 6 |
| **Llavero + tarjeta RFID** | Llavero azul y tarjeta blanca tipo credencial | — | 6 |
| **Módulo RTC** | PCB con **portapilas circular** (CR2032) | 3.3-5V | 4 |
| **Módulo RGB 3 colores** | LED grande sobre PCB chico, 4 pines | 3.3V | 1 |

**RC522**: es el componente más caro y más frágil del kit. **VCC a 3.3V.** Con 5V se quema al instante y no hay reparación. Medí con el tester antes de conectar. El pin rotulado `SDA` **no es I2C**, es el chip-select de SPI — está mal etiquetado de fábrica y confunde a todo el mundo.

**Módulo RTC**: fijate qué chip dice.

| Chip | Precisión | Nota |
|---|---|---|
| **DS3231** | ±2 min/año | Tiene compensación de temperatura. El bueno. |
| **DS1307** | ±20 min/mes | Aceptable, pero hay que resincronizar seguido |

Los dos responden en `0x68` por I2C y usan la misma librería (`RTClib`). **Sacale el plástico aislante a la pila** o va a perder la hora en cada corte. Si tu módulo dice DS1307, resincronizá por NTP en cada arranque (ya lo hacés desde la semana 10).

**Módulo RGB**: 4 pines, uno común y tres de color. Averiguá cuál tenés:

```
Cátodo común (-):  el pin común va a GND.  Color prende con valor ALTO
Ánodo común (+):   el pin común va a 3.3V. Color prende con valor BAJO (invertido)
```

La mayoría de los módulos del kit **ya traen las resistencias incorporadas** (buscá tres cuadraditos negros en el PCB). Si no las tiene, poné 220Ω en cada color o quemás el LED.

---

### A.9 — La protoboard

No es un componente, pero medio kit falla por no entender cómo está conectada por dentro:

```
 ┌────────────────────────────────────────┐
 │ + ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●  │ ← toda la fila unida (alimentación)
 │ − ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●  │ ← toda la fila unida (GND)
 │                                        │
 │ a ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●   │ ┐
 │ b ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●   │ │ columnas de 5
 │ c ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●   │ │ unidas entre sí
 │ d ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●   │ │ (a-b-c-d-e)
 │ e ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●   │ ┘
 │═══════════ canal central ══════════════│ ← separa los dos lados
 │ f ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●   │ ┐ otro grupo
 │ g ●●●●●  ●●●●●  ●●●●●  ●●●●●  ●●●●●   │ ┘ (f-g-h-i-j)
 └────────────────────────────────────────┘
```

Tres cosas que arreglan casi todo:

1. **Verticalmente unido, horizontalmente no.** Los 5 agujeros de una columna son el mismo nodo eléctrico.
2. **El canal del medio separa.** Por eso los chips DIP como el 74HC595 se montan a caballo del canal: cada pata queda en su propio nodo.
3. **Las filas de alimentación a veces se cortan al medio.** Muchas protoboard de 830 puntos tienen las tiras `+`/`−` partidas en dos mitades (fijate si hay un corte en la línea roja/azul). Si tu circuito anda de un lado y no del otro, es esto: poné un jumper puenteando las mitades.

---

### A.10 — Alimentación

| Ítem | Cómo lo reconocés | Uso |
|---|---|---|
| **Conector de batería 9V** | Broche a presión con cables rojo y negro | Rojo → `VIN`, negro → `GND` |

Sirve para alimentar **el ESP32 solo**, sin motores. La pila de 9V tiene ~500mAh y el regulador de la placa disipa como calor todo lo que va de 9V a 3.3V (más del 60% de la energía). Con WiFi activo dura unas 2-3 horas.

Para los proyectos a batería de la semana 9, usá 18650 de 3.7V con módulo TP4056 (~$5). Y **nunca** conectes la pila de 9V al pin de 3.3V o al de 5V: esos son salidas del regulador, no entradas. Entra por `VIN` o por USB, nunca por otro lado.

---

### A.11 — Los cuatro huérfanos

Estos cuatro componentes no tenían proyecto asignado. Acá van, integrados a las semanas que ya existen:

**Módulo RGB → Semana 1.** Indicador de estado por color para tu panel de alarma, en lugar de tres LEDs sueltos. Verde = reposo, amarillo = alerta, rojo pulsante = disparada. Enseña mezcla aditiva de color con tres canales PWM simultáneos, y es la continuación natural del ejercicio de los buzzers.

```cpp
void setColor(uint8_t r, uint8_t g, uint8_t b) {
  // Si tu módulo es de ánodo común, invertí: 255-r, 255-g, 255-b
  analogWrite(PIN_R, r);
  analogWrite(PIN_G, g);
  analogWrite(PIN_B, b);
}
```

**Sensor de inclinación → Semana 5.** Detector de apertura de tapa o de vuelco, integrado al control de tanque como cuarta protección: si el gabinete se movió, bloqueo de seguridad y alerta por MQTT. Se lee como un botón (con `INPUT_PULLUP` y debounce), pero el caso de uso es de seguridad, no de interfaz.

**Sensor de sonido → Semana 5.** Detección de eventos por umbral: que arrancó la bomba, que hay un golpe, que una máquina cambió de régimen. Combinalo con el control de tanque: si el relay dice "bomba encendida" pero el sensor de sonido no detecta nada, **la bomba no está funcionando**. Eso es verificación de actuador — comprobar que lo que ordenaste efectivamente pasó — y es un patrón que casi nadie implementa y que distingue un sistema serio.

**Display de 1 dígito → Semana 7.** Es el paso previo a la matriz 8x8. Con 7 segmentos y un solo dígito aprendés el mapeo de bits a segmentos sin la complicación del multiplexado; después, con el 74HC595, lo hacés con 3 pines en lugar de 8. Cuando pases a la matriz, ya vas a tener la mitad del problema resuelto.

---

### A.12 — Resumen de voltajes

Pegá esto al lado de la protoboard. La mayoría de los componentes muertos se mueren acá:

| Componente | Voltaje | Si te equivocás |
|---|---|---|
| **RC522 (RFID)** | **3.3V ÚNICAMENTE** | **Se quema, irreversible** |
| LM35DZ | 5V (mínimo 4V) | Con 3.3V lee mal o no lee |
| Módulo relay | 5V (VCC) | Con 3.3V no dispara o falla intermitente |
| Servo SG90 | 5V externo | Con el pin del ESP32: reinicios aleatorios |
| Stepper + ULN2003 | 5V externo | Igual: reinicios, o no se mueve |
| ESP32 | USB o VIN 5-12V | Nunca alimentes por los pines 3.3V/5V |
| DHT11, RTC, LCD, 74HC595 | 3.3V o 5V, toleran ambos | — |
| Todo lo demás | 3.3V seguro | — |

**Regla de oro**: cualquier salida de un módulo que esté alimentado con 5V puede entregar 5V en su pin de datos, y los GPIO del ESP32 toleran **3.3V máximo**. Si alimentás un módulo con 5V y su salida digital va directo a un GPIO, medí primero con el tester: si entrega 5V, necesitás un divisor de tensión (10K + 20K) o un conversor de nivel. Los módulos de este kit con comparador LM393 (llama, sonido) suelen entregar el mismo voltaje con que los alimentás — alimentalos con 3.3V y te ahorrás el problema.

---

## Historial

| Versión | Fecha | Cambios |
|---|---|---|
| 2.0 | Sep 2026 | Reescrito para el kit HEMMEL TEK-002. Software adelantado a semana 3. Casos de uso reales por semana. Código corregido (INPUT_PULLUP, ESP32Servo, ADC1, DHT11, analogReadMilliVolts). Agregadas semanas 8-12 que faltaban en v1. Expectativas ajustadas. |
| 2.1 | Sep 2026 | Anexo A: catálogo de los 39 ítems con identificación física, voltajes y trampas. Integrados los 4 componentes huérfanos (RGB, inclinación, sonido, display 1 dígito). |
