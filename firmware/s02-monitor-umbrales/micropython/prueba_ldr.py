# Montaje 2 — fotorresistencia (LDR) en GPIO 39 (ADC1), divisor con 10K a GND
#
#   3.3V ── LDR ──┬── GPIO 39
#                 │
#                10K
#                 │
#                GND
#
# Más luz → menos resistencia en la LDR → el punto medio sube hacia 3.3V.
# Además del voltaje, despeja la resistencia de la LDR con la fórmula del divisor.
#
#   mpremote run prueba_ldr.py

from machine import ADC, Pin
import time
import pinout

R_FIJA = 10_000      # la resistencia de 10K a GND
VCC_MV = 3300

adc = ADC(Pin(pinout.LDR))
adc.atten(ADC.ATTN_11DB)

while True:
    mv = adc.read_uv() // 1000
    # Divisor: V = VCC × R_FIJA / (R_LDR + R_FIJA)  →  R_LDR = R_FIJA × (VCC − V) / V
    if mv > 0:
        r_ldr = R_FIJA * (VCC_MV - mv) // mv
        print("mV={:4d}  R_LDR≈{:7d} Ω".format(mv, r_ldr))
    else:
        print("mV={:4d}  R_LDR: fuera de rango (muy oscuro)".format(mv))
    time.sleep_ms(300)
