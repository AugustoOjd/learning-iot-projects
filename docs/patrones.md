# Mapa de transferencia

El índice inverso del laboratorio. En vez de "qué hice en la semana 4", responde
**"esto que aprendí, ¿dónde más sirve?"**.

Llenalo al cerrar cada proyecto, cuando la técnica todavía está fresca. La columna
que importa es la tercera: es la que convierte un ejercicio en criterio reutilizable.

| Técnica | Dónde la aprendí | Dónde más se aplica | ¿Ya la usé de nuevo? |
|---|---|---|---|
| **Máquina de estados** | s01 | Alarmas, semáforos, cargadores de batería, máquinas expendedoras, cualquier secuencia con confirmación entre pasos | |
| **Debounce** | s01 | Todo contacto mecánico: botones, sensores de inclinación, finales de carrera, caudalímetros de pulsos | |
| **Loop no bloqueante (`millis()`)** | s01 | Cualquier dispositivo que atienda más de una cosa. Es la precondición de todo lo demás | |
| **Divisor de tensión** | s02 | Todo sensor resistivo: LDR, termistores, humedad de suelo, nivel de agua. También para medir batería y adaptar señales de 5V a 3.3V | |
| **Filtro de media móvil** | s02 | Cualquier ADC ruidoso: corriente, peso, presión, sonido | |
| **Histéresis / banda muerta** | s02 | Termostatos, control de compresor, nivel de tanque, cualquier on/off con umbral. Sin esto se destruyen los actuadores | |
| **Telemetría con LWT** | s03 | Toda flota de dispositivos: distinguir "sin novedades" de "se murió" | |
| **Publicar `heap` y `uptime`** | s03 | Diagnóstico remoto de cualquier sistema embebido. Detecta fugas de memoria en un gráfico | |
| **I2C (bus compartido)** | s04 | Sensores, pantallas, expansores de I/O, EEPROM. Es el bus por defecto de la electrónica moderna | |
| **Persistencia en NVS** | s04 | Configuración, contadores, calibraciones, whitelists: todo lo que debe sobrevivir a un corte | |
| **Buffer circular en flash** | s04 | Logging en cualquier dispositivo con memoria contada. Reparte el desgaste de la flash | |
| **Store-and-forward** | s04 | Fichaje, medidores de energía, logística, telemetría rural. Todo lo que no puede perder eventos por una caída de red | |
| **Timeout de seguridad** | s05 | Bombas (marcha en seco), calefactores, cerraduras, motores. La pregunta es siempre "¿qué pasa si esto no termina?" | |
| **Detección de sensor caído** | s05 | Cualquier control automático. Una lectura imposible no se usa, se desconfía | |
| **Verificación de actuador** | s05 | Confirmar que lo ordenado efectivamente pasó: bomba + sensor de sonido, cerradura + sensor de puerta. Casi nadie lo implementa | |
| **PWM** | s05 | Servos, velocidad de motores, dimmers, brillo de pantallas, generación de tonos | |
| **SPI** | s06 | Pantallas rápidas, tarjetas SD, RFID, ADC externos, radios LoRa | |
| **Lógica crítica local** | s06 | Control de acceso, riego, seguridad, industrial. La nube es para observar y administrar, **nunca** en el camino crítico | |
| **Multiplexado** | s07 | Displays, teclados matriciales, lectura de muchos sensores con pocos pines | |
| **Expansión de I/O** | s07 | Cuando te quedás sin pines: paneles, controladores industriales, domótica con muchos relays | |
| **FreeRTOS: tareas y colas** | s08 | Cualquier dispositivo que haga dos cosas a distinta velocidad. Es el modelo de concurrencia del embebido | |
| **Watchdog** | s08 | Todo lo instalado donde nadie puede apretar reset. Obligatorio en producción | |
| **Backoff exponencial** | s08 | Toda reconexión: red, broker, API. También aplica a backend — ya lo conocés de otro lado | |
| **Deep sleep** | s09 | Todo lo que va a batería. Define la arquitectura entera del dispositivo | |
| **Presupuesto energético** | s09 | La conversación previa a cualquier proyecto a batería. Decide si el producto es viable | |
| **OTA** | s10 | Toda flota instalada. Sin esto, cada actualización es una visita técnica | |
| **TLS + gestión de secretos** | s10 | Cualquier dispositivo en red que no sea un juguete | |
| **Provisioning** | s10 | Instalación sin recompilar: un binario, muchos dispositivos, configurados por quien instala | |
| **Gateway + nodos dormidos** | s11 | Agro, edificios, minería, cualquier despliegue disperso a batería. Es la respuesta correcta al 80% del IoT real | |

## Cómo usarlo

Al terminar cada proyecto, agregá una fila por técnica nueva y completá la tercera columna
con 3-5 casos concretos. Cuando una técnica vieja reaparezca en un proyecto nuevo, marcala
en la cuarta columna: eso es la señal de que se te volvió criterio y no receta.
