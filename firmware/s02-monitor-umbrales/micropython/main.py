# Montaje 4 — Monitor de umbrales: temperatura + luz, con histéresis.
#
# Caso: heladera de farmacia. El LM35 mide la temperatura y la fotorresistencia
# vigila la puerta: adentro de una heladera cerrada está oscuro, así que luz
# significa puerta abierta.
#
# Probar sin guardarlo en el chip:
#   mpremote run main.py
# Dejarlo instalado (arranca solo al encender):
#   mpremote cp ../../../shared/config/pinout.py :
#   mpremote cp main.py : + repl

import time
from machine import ADC, Pin

import pinout

# ---------- Temperatura ----------
# LM35 con ATTN_0DB y promedio de 16 (ver docs/decisiones.md): ±0.09°C en reposo.
# Medido en el montaje 3: ambiente 25.5°C, entre los dedos llega a 31°C.
#   ALTO 28.0  2.5°C sobre el ambiente: lo dispara la mano, no el cuarto
#   BAJO 26.5  1.5°C de banda muerta, más de 15 veces el ruido medido
#
# HISTERESIS: dispara a 28.0 pero no libera hasta 26.5. Sin esa banda, con la
# temperatura rondando 28.0 la alarma entraría y saldría varias veces por
# segundo. En un relay que maneja un compresor, eso lo destruye en días.
TEMP_ALTO = 28.0
TEMP_BAJO = 26.5

# ---------- Puerta (luz) ----------
# Fotorresistencia + 10K, medido en el montaje 2:
#   tapada          ~157 mV  → puerta cerrada
#   luz del cuarto  ~500 mV  → puerta abierta
#   ALTO 350 / BAJO 250: la banda queda entre los dos, lejos de ambos
LUZ_ALTO = 350
LUZ_BAJO = 250

# Abrir la puerta un rato es normal: alguien saca un remedio. La alarma suena
# recién si queda abierta más de este tiempo. Las heladeras comerciales usan
# ~60 s; 6 s alcanza para verlo funcionar.
PUERTA_MAX_MS = 6_000

N = 16

lm35 = ADC(Pin(pinout.LM35))
lm35.atten(ADC.ATTN_0DB)
ldr = ADC(Pin(pinout.LDR))
ldr.atten(ADC.ATTN_11DB)

led = Pin(pinout.LED_ROJO, Pin.OUT, value=0)
buzzer = Pin(pinout.BUZZER_ACTIVO, Pin.OUT, value=0)


def promedio_mv(adc):
    suma = 0
    for _ in range(N):
        suma += adc.read_uv()
    return suma / N / 1000


def histeresis(activo, valor, alto, bajo):
    """Nuevo estado: se activa por encima de `alto`, se libera por debajo de `bajo`."""
    if not activo and valor > alto:
        return True
    if activo and valor < bajo:
        return False
    return activo


temp_alta = False
puerta_abierta = False
puerta_alarma = False
desde_apertura = 0
ultimo_reporte = time.ticks_ms()

print("\n=== MONITOR DE UMBRALES ===")

while True:
    ahora = time.ticks_ms()
    temp = promedio_mv(lm35) / 10          # 10 mV por °C
    luz = promedio_mv(ldr)

    nuevo = histeresis(temp_alta, temp, TEMP_ALTO, TEMP_BAJO)
    if nuevo != temp_alta:
        temp_alta = nuevo
        print("ALARMA: temperatura alta ({:.2f} °C)".format(temp) if temp_alta
              else "Temperatura normalizada ({:.2f} °C)".format(temp))

    nuevo = histeresis(puerta_abierta, luz, LUZ_ALTO, LUZ_BAJO)
    if nuevo != puerta_abierta:
        puerta_abierta = nuevo
        desde_apertura = ahora
        print("Puerta abierta" if puerta_abierta else "Puerta cerrada")

    # ticks_diff y no una resta: ticks_ms() desborda y vuelve a cero.
    abierta_ms = time.ticks_diff(ahora, desde_apertura) if puerta_abierta else 0
    nuevo = abierta_ms > PUERTA_MAX_MS
    if nuevo and not puerta_alarma:
        print("ALARMA: puerta abierta más de {} s".format(PUERTA_MAX_MS // 1000))
    puerta_alarma = nuevo

    alarma = temp_alta or puerta_alarma
    led.value(alarma)
    # El buzzer activo solo prende o apaga. El pitido intermitente (250 ms de
    # cada segundo) sale del reloj, sin sleep, para no frenar las lecturas.
    buzzer.value(alarma and (ahora // 250) % 4 == 0)

    if time.ticks_diff(ahora, ultimo_reporte) >= 1000:
        ultimo_reporte = ahora
        print("T={:5.2f} °C  luz={:4.0f} mV  puerta={}  {}".format(
            temp, luz,
            "abierta {:2d}s".format(abierta_ms // 1000) if puerta_abierta else "cerrada   ",
            "<< ALARMA" if alarma else ""))

    time.sleep_ms(20)
