"""Pinout maestro del kit HEMMEL TEK-002 sobre NodeMCU ESP-32S.

Espejo de pinout.h. Si cambiás un pin, cambialo en los dos archivos.

Reglas que esta asignación respeta (ver "Antes de enchufar nada" en el roadmap):
  - Todo lo analógico vive en ADC1 (GPIO 32-39). ADC2 muere al encender el WiFi.
  - GPIO 34/35/36/39 son solo entrada y no tienen pull-up interno.
  - GPIO 6-11 están conectados a la flash: no existen.
  - GPIO 12 no se usa para nada (strapping: en HIGH al bootear el chip no arranca).

Subir al dispositivo con:
    mpremote cp shared/config/pinout.py :
"""

# ---------- Buses (fijos, no moverlos) ----------
I2C_SDA = 21          # LCD1602-I2C, RTC
I2C_SCL = 22
SPI_SCK = 18          # RC522
SPI_MISO = 19
SPI_MOSI = 23
SPI_CS = 5            # rotulado "SDA" en el RC522: NO es I2C
SPI_RST = 17

# ---------- Analógicos (ADC1, solo entrada) ----------
LM35 = 36             # s02 — alimentar a 5V
LDR = 39              # s02 — divisor con 10K a GND
POTENCIOMETRO = 34    # s02
NIVEL_AGUA = 34       # s05 — reemplaza al potenciómetro
SONIDO_AO = 35        # s05
JOYSTICK_X = 32       # s05
JOYSTICK_Y = 33

# ---------- Digitales ----------
LED_ONBOARD = 2
LED_ROJO = 13
LED_AMARILLO = 14
LED_VERDE = 27
BOTON_1 = 16          # Pin.PULL_UP, otra pata a GND
BOTON_2 = 4
BUZZER_ACTIVO = 25    # nivel alto y suena
BUZZER_PASIVO = 26    # PWM: necesita frecuencia
DHT11 = 15            # pull-up 10K a 3.3V
LLAMA_DO = 35
INCLINACION = 33      # Pin.PULL_UP, rebota como un botón
IR_RX = 16
RELAY = 27            # VCC del relay a 5V
SERVO = 13            # alimentación 5V externa

# Stepper 28BYJ-48 vía ULN2003 — alimentación 5V externa
STEPPER = (32, 33, 25, 26)   # IN1..IN4

# 74HC595 — comparte pines con SPI (no uses ambos a la vez)
SR_DS = 23
SR_SHCP = 18
SR_STCP = 5

# Módulo RGB (s01) — verificá si es cátodo o ánodo común
RGB_R = 13
RGB_G = 14
RGB_B = 27

# Alimentación conmutada del sensor de nivel: se energiza solo para medir,
# si no las tiras de cobre se electrolizan en semanas.
ALIM_NIVEL = 26

# Teclado matricial 4x4 (s06)
TECLADO_FILAS = (13, 14, 27, 26)
TECLADO_COLUMNAS = (25, 33, 32, 4)

# Algunos pines se repiten entre proyectos: es a propósito, nunca vas a tener
# todo conectado a la vez. Si dos periféricos de UN MISMO proyecto chocan acá,
# es un bug de asignación, no una coincidencia.
