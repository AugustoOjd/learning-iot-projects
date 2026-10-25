# Montaje 1 — potenciómetro en GPIO 34 (ADC1)
#
# Compara la lectura cruda del ADC con la calibrada de fábrica.
# Girá de tope a tope y mirá cómo se separan cerca de 0V y de 3.3V.
#
#   mpremote cp ../../../shared/config/pinout.py :
#   mpremote run prueba_pot.py

from machine import ADC, Pin
import time
import pinout

adc = ADC(Pin(pinout.POTENCIOMETRO))
adc.atten(ADC.ATTN_11DB)   # rango completo ~0-3.3V

while True:
    crudo = adc.read()             # 0..4095, sin calibrar
    mv = adc.read_uv() // 1000     # con la calibración de fábrica del chip
    print("crudo={:4d}  mV={:4d}".format(crudo, mv))
    time.sleep_ms(200)
