# Montaje 3 — Panel de alarma. Máquina de estados de cuatro estados.
#
#   mpremote run panel_alarma.py
#
# Requiere pinout.py en el chip:
#   mpremote cp ../../../shared/config/pinout.py :

import time
from machine import ADC, Pin, PWM

import pinout

REPOSO, ALERTA, DISPARADA, SILENCIADA = range(4)
NOMBRES = ("REPOSO", "ALERTA", "DISPARADA", "SILENCIADA")

# El sensor tiene que seguir detectando este tiempo seguido antes de disparar.
# Un sensor barato tiene falsos positivos; exigir persistencia los filtra.
# 4s hace el estado ALERTA claramente observable. En un producto real es un
# compromiso: más tiempo filtra mejor, pero son segundos de incendio sin avisar.
CONFIRMACION_MS = 4000
DEBOUNCE_MS = 50

# Umbrales medidos con prueba_llama.py, resistencia de 10K:
#   luz ambiente   1662 - 1900
#   con llama      3377 - 3776
#   separación     ~1500 cuentas
#
# Esa separación es amplia, así que un umbral fijo funciona. Los márgenes:
#   ALTO 2600  queda 700 por debajo de la llama sostenida
#   BAJO 2200  queda 300 por encima del máximo ambiente
#
# HISTERESIS: dispara a 2600 pero no libera hasta 2200. Sin esa banda muerta,
# un valor oscilando alrededor del umbral entraría y saldría del estado varias
# veces por segundo.
#
# ⚠️ BAJO tiene que quedar SIEMPRE por encima del máximo ambiente. Si lo
# pusieras en 1800, después de disparar el valor en reposo nunca bajaría de
# ahí de forma confiable y la alarma quedaría trabada.
#
# Recalibrar si cambia la luz del lugar: un intento anterior con el ambiente
# en 3700 dejaba solo 395 cuentas de separación y no era usable. Apantallar el
# sensor para reducir su campo de visión fue lo que recuperó el rango.
UMBRAL_FUEGO_ALTO = 2600
UMBRAL_FUEGO_BAJO = 2200

llama_adc = ADC(Pin(pinout.LLAMA_DO))
llama_adc.atten(ADC.ATTN_11DB)
llama_adc.width(ADC.WIDTH_12BIT)

_hay_fuego = False


def leer_llama():
    """Devuelve (hay_fuego, valor_crudo). Aplica promediado e histéresis."""
    global _hay_fuego

    suma = 0
    for _ in range(8):
        suma += llama_adc.read()
    valor = suma // 8

    if not _hay_fuego and valor > UMBRAL_FUEGO_ALTO:
        _hay_fuego = True
    elif _hay_fuego and valor < UMBRAL_FUEGO_BAJO:
        _hay_fuego = False

    return _hay_fuego, valor
boton = Pin(pinout.BOTON_1, Pin.IN, Pin.PULL_UP)
led_verde = Pin(pinout.LED_VERDE, Pin.OUT)
led_amarillo = Pin(pinout.LED_AMARILLO, Pin.OUT)
led_rojo = Pin(pinout.LED_ROJO, Pin.OUT)
sirena = PWM(Pin(pinout.BUZZER_PASIVO), freq=880, duty=0)

# El buzzer activo queda cableado del montaje 2 pero este panel no lo usa.
# Se inicializa en bajo igual: un pin de salida conectado y sin configurar
# queda flotando, y el estado indefinido es lo que produce fallas raras.
Pin(pinout.BUZZER_ACTIVO, Pin.OUT).value(0)

estado = REPOSO
entrada_estado = time.ticks_ms()

_ultimo_cambio = time.ticks_ms()
_ultima_lectura = 1
_estable = 1


def boton_apretado():
    """True una sola vez por pulsación, en el flanco de bajada. No bloquea."""
    global _ultimo_cambio, _ultima_lectura, _estable

    lectura = boton.value()
    if lectura != _ultima_lectura:
        _ultimo_cambio = time.ticks_ms()
        _ultima_lectura = lectura

    # ticks_diff y no una resta: ticks_ms() desborda y vuelve a cero.
    # Con resta directa, el programa falla una vez cada ~12 días.
    if time.ticks_diff(time.ticks_ms(), _ultimo_cambio) > DEBOUNCE_MS:
        if _estable != lectura:
            _estable = lectura
            if _estable == 0:
                return True
    return False


def cambiar_a(nuevo, nivel=None):
    global estado, entrada_estado
    estado = nuevo
    entrada_estado = time.ticks_ms()
    if nivel is None:
        print("->", NOMBRES[nuevo])
    else:
        print("-> {:<11} (sensor={})".format(NOMBRES[nuevo], nivel))


print("\n=== PANEL DE ALARMA ===")
cambiar_a(REPOSO)

while True:
    ahora = time.ticks_ms()
    hay_fuego, nivel = leer_llama()
    apretado = boton_apretado()
    en_estado = time.ticks_diff(ahora, entrada_estado)

    led_verde.value(0)
    led_amarillo.value(0)
    led_rojo.value(0)

    if estado == REPOSO:
        led_verde.value(1)
        sirena.duty(0)
        if hay_fuego:
            cambiar_a(ALERTA, nivel)

    elif estado == ALERTA:
        led_amarillo.value(1)
        if not hay_fuego:
            cambiar_a(REPOSO, nivel)
        elif en_estado > CONFIRMACION_MS:
            cambiar_a(DISPARADA, nivel)

    elif estado == DISPARADA:
        led_rojo.value((ahora // 250) % 2)              # parpadeo sin sleep
        sirena.duty(512)
        sirena.freq(880 if (ahora // 400) % 2 else 660)  # sirena bitonal
        if apretado:
            cambiar_a(SILENCIADA)

    elif estado == SILENCIADA:
        led_rojo.value(1)          # fijo: recordá que hubo un evento
        sirena.duty(0)
        # Solo vuelve a reposo si el fuego se fue Y alguien rearma
        if not hay_fuego and apretado:
            cambiar_a(REPOSO)

    time.sleep_ms(10)
