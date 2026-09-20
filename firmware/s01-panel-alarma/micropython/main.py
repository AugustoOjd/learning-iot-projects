# Montaje 1 — LED y botón.
# Instrucciones físicas y cableado: ../INSTRUCCIONES_FISICAS.md
#
# Subir y correr:
#   mpremote cp ../../../shared/config/pinout.py :
#   mpremote cp main.py : + repl

import time
from machine import Pin

import pinout

led = Pin(pinout.LED_ROJO, Pin.OUT)
# PULL_UP: el pin reposa en 1 y cae a 0 al apretar, porque el botón lo lleva a GND.
boton = Pin(pinout.BOTON_1, Pin.IN, Pin.PULL_UP)

while True:
    apretado = boton.value() == 0
    led.value(apretado)
    time.sleep_ms(50)
