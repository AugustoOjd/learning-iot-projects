# Identifica qué LED físico responde a cada GPIO.
#
#   mpremote run prueba_leds.py
#
# Prende uno a la vez, 2 segundos cada uno, y dice cuál debería estar
# encendido. Si en algún turno no se enciende nada, ese es el que falla.
# Si se enciende el equivocado, tenés dos jumpers cruzados.

import time
from machine import Pin

import pinout

LEDS = (
    ("ROJO     (GPIO 13, columna 5  → j5)", pinout.LED_ROJO),
    ("AMARILLO (GPIO 14, columna 8  → j8)", pinout.LED_AMARILLO),
    ("VERDE    (GPIO 27, columna 9  → j9)", pinout.LED_VERDE),
)

pines = [(nombre, Pin(gpio, Pin.OUT)) for nombre, gpio in LEDS]

print("\n=== IDENTIFICACION DE LEDS ===")
print("Ctrl+C para salir\n")

while True:
    for nombre, pin in pines:
        for _, otro in pines:
            otro.value(0)
        pin.value(1)
        print("Encendido ->", nombre)
        time.sleep(2)
