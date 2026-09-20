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

---

_(Tus decisiones van acá. Una por técnica no obvia.)_
