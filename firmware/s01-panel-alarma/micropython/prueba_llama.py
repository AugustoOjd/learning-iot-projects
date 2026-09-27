# Calibración del sensor de llama (fotodiodo IR, versión sin módulo).
#
#   mpremote run prueba_llama.py
#
# Imprime la lectura del ADC junto con el mínimo y el máximo vistos.
# Objetivo: encontrar el umbral que separa "luz ambiente" de "hay fuego".
#
# Cómo usarlo:
#   1. Dejalo corriendo un momento quieto  → anotá el rango en reposo
#   2. Acercá un encendejor a ~20 cm       → anotá el rango con llama
#   3. El umbral va en el medio de los dos
#
# Si el valor NO cambia al acercar la llama, invertí las dos patas del
# sensor: es un fotodiodo y la polaridad importa.

import time
from machine import ADC, Pin

import pinout

adc = ADC(Pin(pinout.LLAMA_DO))       # GPIO 35, ADC1
adc.atten(ADC.ATTN_11DB)               # rango completo, ~0 a 3.3V
adc.width(ADC.WIDTH_12BIT)             # 0 a 4095

minimo = 4095
maximo = 0

print("\n=== CALIBRACION SENSOR DE LLAMA ===")
print("Ctrl+C para salir\n")

while True:
    # Promedio de 16 lecturas: el ADC del ESP32 es ruidoso y este es
    # el filtro más barato que existe para ganar estabilidad.
    suma = 0
    for _ in range(16):
        suma += adc.read()
        time.sleep_us(200)
    valor = suma // 16

    if valor < minimo:
        minimo = valor
    if valor > maximo:
        maximo = valor

    # read_uv() usa la curva de calibración que Espressif graba en cada
    # chip de fábrica. Mucho más fiel que convertir el valor crudo a mano.
    mv = adc.read_uv() // 1000

    barra = "#" * (valor * 40 // 4095)
    print("{:4d}  {:4d} mV  min={:4d} max={:4d}  {}".format(
        valor, mv, minimo, maximo, barra))

    time.sleep_ms(200)
