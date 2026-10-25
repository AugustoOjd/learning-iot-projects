# Decisiones de diseño

Por qué elegí cada cosa sobre la alternativa. Esta es la sección que casi nadie escribe y la
que te van a preguntar en una entrevista técnica: cualquiera copia un tutorial, explicar el
criterio es lo que demuestra ingeniería.

Escribí cada entrada **cuando tomás la decisión**, no al final. En la semana 12 no vas a
acordarte por qué elegiste 1.5°C de histéresis en la semana 2.

## Formato

```
### [sNN] Decisión en una línea

**Alternativa descartada:** qué otra cosa podría haber hecho.
**Por qué:** el criterio. Idealmente con un número o una consecuencia concreta.
**Costo:** qué perdí al elegir esto (siempre hay uno).
```

---

### [s00] PlatformIO en vez del IDE de Arduino

**Alternativa descartada:** Arduino IDE 2.x, que es lo que asumen todos los tutoriales.
**Por qué:** las dependencias quedan fijadas en `platformio.ini`, que se versiona. El IDE de
Arduino guarda las librerías en una carpeta global compartida entre proyectos: en la semana 8,
reproducir con qué versión de `PubSubClient` compilaba la semana 3 sería imposible.
**Costo:** ~1 hora de curva inicial y tener que traducir mentalmente los tutoriales.

### [s00] Monorepo en vez de un repo por proyecto

**Alternativa descartada:** 12 repos, uno por semana.
**Por qué:** los proyectos comparten esqueleto (`shared/`). Con repos separados, el hardening
de la semana 8 habría que aplicarlo seis veces a mano.
**Costo:** el portfolio queda mezclado con ejercicios. Se resuelve extrayendo el proyecto final
a su propio repo público si hace falta.

### [s00] Expansión de I/O en la semana 5 y Actuadores en la 7

**Alternativa descartada:** el orden original del roadmap: actuadores (5), SPI (6), expansión
de I/O (7).
**Por qué:** ordenar la parte de electrónica según el riesgo de dañar componentes. El 74HC595
manejado a mano (datos, reloj, latch) es SPI hecho por software, así que ponerlo justo antes
de la semana 6 hace que SPI deje de ser una caja negra. Y los actuadores (relay, servo,
stepper, fuente externa, masa común) son la semana donde un error quema cosas: llegar con dos
semanas más de práctica y con el multímetro ya comprado baja ese riesgo.
**Costo:** el control de acceso (s06) usa el relay antes de haberlo estudiado: la cerradura es
un LED hasta la semana 7. Además, las carpetas cambiaron de nombre (`s05-panel-indicador`,
`s07-control-tanque`) y el roadmap deja de coincidir con la versión original.

### [s02] LM35 leído con `ATTN_0DB` y promedio de 16 lecturas

**Alternativa descartada:** `ATTN_11DB` (rango completo de 0 a 3.3V), que es lo que usan casi
todos los tutoriales, y una sola lectura por medición.
**Por qué:** la señal del LM35 a temperatura ambiente es de ~250 mV. Con 11dB, el 90% del
rango del ADC queda sin usar y cada cuenta vale ~0.08°C. Con 0dB vale ~0.02°C. Medido en
reposo: lectura suelta ±0.8°C, x16 con 11dB ±0.28°C, **x16 con 0dB ±0.09°C**. Con 1.5°C de
histéresis, ±0.8°C haría saltar la alarma por ruido.
**Costo:** 0dB satura cerca de 950 mV, o sea ~95°C, y para una sala o una heladera sobra. Lo que
no resuelve es la parte baja: tiene un piso de ~100 mV, así que debajo de ~10°C no mide con
ninguna atenuación. Y 16 lecturas tardan ~3 ms por medición.

---

_(Tus decisiones van acá. Una por técnica no obvia.)_
