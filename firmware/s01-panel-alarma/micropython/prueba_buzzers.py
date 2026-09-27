# Montaje 2 — buzzer activo vs pasivo.
#
#   mpremote run prueba_buzzers.py
#
# Requiere pinout.py ya copiado al chip:
#   mpremote cp ../../../shared/config/pinout.py :

import time
from machine import Pin, PWM

import pinout

activo = Pin(pinout.BUZZER_ACTIVO, Pin.OUT)


def fase(titulo):
    print("\n---", titulo)


fase("1. Buzzer ACTIVO con digitalWrite")
print("Tiene un oscilador adentro: con darle tensión ya suena.")
for _ in range(3):
    activo.value(1)
    time.sleep_ms(500)
    activo.value(0)
    time.sleep_ms(300)

fase("2. Buzzer PASIVO con digitalWrite")
print("No deberías escuchar NADA, o apenas un click.")
print("Es solo una membrana: sin oscilador propio no puede sonar.")
pasivo_digital = Pin(pinout.BUZZER_PASIVO, Pin.OUT)
for _ in range(3):
    pasivo_digital.value(1)
    time.sleep_ms(300)
    pasivo_digital.value(0)
    time.sleep_ms(300)

fase("3. Buzzer PASIVO con PWM")
print("Ahora vos le generás la onda, y suena la frecuencia que le pidas.")
# duty 512 de 1023 = 50% del ciclo en alto: la onda cuadrada más simple.
pasivo = PWM(Pin(pinout.BUZZER_PASIVO), freq=440, duty=512)
for nota, freq in [("La  440 Hz", 440), ("La  880 Hz", 880), ("Do 1047 Hz", 1047)]:
    print("  ", nota)
    pasivo.freq(freq)
    time.sleep_ms(600)

fase("4. Sirena bitonal")
print("Alternando dos frecuencias: esto va a ser tu alarma del montaje 3.")
for _ in range(6):
    pasivo.freq(880)
    time.sleep_ms(250)
    pasivo.freq(660)
    time.sleep_ms(250)

pasivo.deinit()   # libera el canal de PWM; sin esto el pin sigue oscilando
activo.value(0)
print("\nFin.")
