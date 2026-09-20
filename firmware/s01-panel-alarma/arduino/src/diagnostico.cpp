// Diagnóstico del montaje 1. Separa el LED del botón para saber cuál falla.
//
//   pio run -e diagnostico -t upload && pio device monitor
//
// Qué mirar:
//   - El LED parpadea 1 vez por segundo  → el circuito del LED está bien
//   - El valor impreso cambia al apretar  → el circuito del botón está bien
// Cada mitad se prueba por separado: el parpadeo NO depende del botón.

#include <Arduino.h>
#include "config/pinout.h"

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n\n=== DIAGNOSTICO s01 ===");
  Serial.printf("LED  en GPIO %d\n", PIN_LED_ROJO);
  Serial.printf("BOTON en GPIO %d (INPUT_PULLUP)\n", PIN_BOTON_1);
  Serial.println("Esperado en reposo: boton=1");
  Serial.println("Esperado apretado:  boton=0\n");

  pinMode(PIN_LED_ROJO, OUTPUT);
  pinMode(PIN_BOTON_1, INPUT_PULLUP);
}

void loop() {
  // El LED parpadea solo, sin depender del botón.
  bool encendido = (millis() / 500) % 2;
  digitalWrite(PIN_LED_ROJO, encendido);

  static unsigned long ultimo = 0;
  if (millis() - ultimo >= 500) {
    ultimo = millis();
    Serial.printf("boton=%d   led=%s\n",
                  digitalRead(PIN_BOTON_1),
                  encendido ? "ON " : "OFF");
  }
}
