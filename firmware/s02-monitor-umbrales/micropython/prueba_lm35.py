# Montaje 3 — LM35 en GPIO 36 (ADC1), alimentado a 5V
#
#   LM35 (cara plana hacia vos, patas abajo):
#     izquierda → 5V     centro → GPIO 36     derecha → GND
#
# 10 mV por °C. Compara dos atenuaciones del ADC sobre la misma señal,
# y una lectura suelta contra el promedio de 16.
#
#   mpremote run prueba_lm35.py

from machine import ADC, Pin
import time
import pinout

N = 16
adc = ADC(Pin(pinout.LM35))


def leer_mv(atten, n=N):
    adc.atten(atten)
    adc.read_uv()              # descartar la primera lectura después de cambiar la atenuación
    suma = 0
    for _ in range(n):
        suma += adc.read_uv()
        time.sleep_us(200)
    return suma / n / 1000


while True:
    suelta = leer_mv(ADC.ATTN_11DB, 1)
    mv11 = leer_mv(ADC.ATTN_11DB)
    mv0 = leer_mv(ADC.ATTN_0DB)
    print("11dB suelta: {:5.1f} °C  |  11dB x16: {:5.2f} °C  |  0dB x16: {:5.2f} °C".format(
        suelta / 10, mv11 / 10, mv0 / 10))
    time.sleep(1)
