#include <Arduino.h>
#include "config/pinout.h"

// Montaje 1 — LED y botón.
// Instrucciones físicas y cableado: ../../INSTRUCCIONES_FISICAS.md

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED_ROJO, OUTPUT);
  pinMode(PIN_BOTON_1, INPUT_PULLUP);
}

void loop() {
  // Con INPUT_PULLUP el pin reposa en HIGH y cae a LOW al apretar,
  // porque el botón lo conecta a GND. La lógica queda invertida.
  bool apretado = (digitalRead(PIN_BOTON_1) == LOW);
  digitalWrite(PIN_LED_ROJO, apretado);
  delay(50);
}
