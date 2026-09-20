// Verificación de cadena de herramientas. NO necesita ningún cable conectado.
// Usa el LED que ya viene soldado en la placa (GPIO 2).
//
//   pio run -e blink-test -t upload && pio device monitor
//
// Si el LED parpadea y el monitor imprime, entonces funcionan: PlatformIO, el driver
// USB, el cable (tiene líneas de datos), el arranque de la placa y la subida de código.
// A partir de ahí, cualquier problema es de cableado — no de toolchain.

#include <Arduino.h>
#include "config/pinout.h"

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED_ONBOARD, OUTPUT);
  Serial.println("\n=== toolchain OK ===");
}

void loop() {
  digitalWrite(PIN_LED_ONBOARD, HIGH);
  Serial.println("LED on");
  delay(500);
  digitalWrite(PIN_LED_ONBOARD, LOW);
  Serial.println("LED off");
  delay(500);
}
