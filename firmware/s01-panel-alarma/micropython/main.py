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
boton = Pin(pinout.BOTON_1, Pin.IN, Pin.PULL_UP)

anterior = None
while True:
    apretado = boton.value() == 0
    led.value(apretado)
    if apretado != anterior:          # imprime solo al cambiar
        print("apretado" if apretado else "suelto")
        anterior = apretado
    time.sleep_ms(50)

