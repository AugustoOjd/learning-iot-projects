#pragma once

// Pinout maestro del kit HEMMEL TEK-002 sobre NodeMCU ESP-32S.
// Única fuente de verdad: si cambiás un pin, cambialo acá y en roadmap_v2_kit.md.
//
// Reglas que esta asignación respeta (ver "Antes de enchufar nada" en el roadmap):
//   - Todo lo analógico vive en ADC1 (GPIO 32-39). ADC2 muere al encender el WiFi.
//   - GPIO 34/35/36/39 son solo entrada y no tienen pull-up interno.
//   - GPIO 6-11 están conectados a la flash: no existen.
//   - GPIO 12 no se usa para nada (strapping: en HIGH al bootear el chip no arranca).

// ---------- Buses (fijos, no moverlos) ----------
#define PIN_I2C_SDA      21   // LCD1602-I2C, RTC
#define PIN_I2C_SCL      22
#define PIN_SPI_SCK      18   // RC522
#define PIN_SPI_MISO     19
#define PIN_SPI_MOSI     23
#define PIN_SPI_CS        5   // rotulado "SDA" en el RC522: NO es I2C
#define PIN_SPI_RST      17

// ---------- Analógicos (ADC1, solo entrada) ----------
#define PIN_LM35         36   // s02 — temperatura, alimentar a 5V
#define PIN_LDR          39   // s02 — divisor con 10K a GND
#define PIN_POTENCIOMETRO 34  // s02
#define PIN_NIVEL_AGUA   34   // s05 — reemplaza al potenciómetro
#define PIN_SONIDO_AO    35   // s05
#define PIN_JOYSTICK_X   32   // s05
#define PIN_JOYSTICK_Y   33

// ---------- Digitales ----------
#define PIN_LED_ONBOARD   2
#define PIN_LED_ROJO     13
#define PIN_LED_AMARILLO 14
#define PIN_LED_VERDE    27
#define PIN_BOTON_1      16   // INPUT_PULLUP, otra pata a GND
#define PIN_BOTON_2       4
#define PIN_BUZZER_ACT   25   // activo: digitalWrite
#define PIN_BUZZER_PAS   26   // pasivo: tone() / PWM
#define PIN_DHT11        15   // pull-up 10K a 3.3V
#define PIN_LLAMA_DO     35   // digital, alternativo al analógico
#define PIN_INCLINACION  33   // INPUT_PULLUP, rebota como un botón
#define PIN_IR_RX        16
#define PIN_RELAY        27   // VCC del relay a 5V
#define PIN_SERVO        13   // alimentación 5V externa

// Stepper 28BYJ-48 vía ULN2003 — alimentación 5V externa.
// OJO: la librería Stepper espera el orden IN1, IN3, IN2, IN4.
#define PIN_STEPPER_IN1  32
#define PIN_STEPPER_IN2  33
#define PIN_STEPPER_IN3  25
#define PIN_STEPPER_IN4  26

// 74HC595 — comparte pines con SPI (no uses ambos a la vez)
#define PIN_595_DS       23
#define PIN_595_SHCP     18
#define PIN_595_STCP      5

// Módulo RGB (s01) — verificá si es cátodo o ánodo común
#define PIN_RGB_R        13
#define PIN_RGB_G        14
#define PIN_RGB_B        27

// Alimentación conmutada del sensor de nivel: se energiza solo para medir,
// si no las tiras de cobre se electrolizan en semanas.
#define PIN_ALIM_NIVEL   26

// Teclado matricial 4x4 (s06)
#define FILAS_TECLADO    {13, 14, 27, 26}
#define COLUMNAS_TECLADO {25, 33, 32,  4}

// Algunos pines se repiten entre proyectos: es a propósito, nunca vas a tener
// todo conectado a la vez. Si dos periféricos de UN MISMO proyecto chocan acá,
// es un bug de asignación, no una coincidencia.
