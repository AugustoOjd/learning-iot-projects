# s01 — Panel de alarma

> **Semana 1** · 🔵🐍 · Estado: 🟡 en curso

Detector de incendio con sirena y luces. Es literalmente lo que hace un panel de alarma comercial.

**Técnica central:** Máquina de estados sin bloqueo

---

## Por dónde empezar

1. **[README.md](README.md)** — el caso real, la técnica y el criterio de terminado
2. **[INSTRUCCIONES_FISICAS.md](INSTRUCCIONES_FISICAS.md)** — armar el circuito paso a paso
3. **El código** — [🔵 Arduino](arduino/src/main.cpp) · [🐍 MicroPython](micropython/main.py)
4. **[media/](media/)** — foto y video **antes de desarmar**
5. **Cerrar** — las tres tareas de abajo

## Archivos de esta carpeta

| Archivo | Para qué | Estado |
|---|---|---|
| [`README.md`](README.md) | Caso real, dónde más se aplica, criterio de terminado. La cara de portfolio | |
| [`INSTRUCCIONES_FISICAS.md`](INSTRUCCIONES_FISICAS.md) | Componentes, cómo se ven, cómo se conectan | ✅ |
| [`arduino/`](arduino/) | Versión C++. `pio run -t upload` | |
| [`micropython/`](micropython/) | Versión Python. `mpremote cp main.py : + repl` | |
| [`documentation-days/`](documentation-days/) | Bitácora diaria: qué hice, qué falló y cómo lo encontré | 🟡 |
| [`media/`](media/) | Foto del cableado y video de 20s | ⬜ |

## Bitácora

| Día | Qué pasó |
|---|---|
| [2026-09-20](documentation-days/2026-09-20.md) | Entorno desde cero + montaje 1 funcionando. Tres fallas de cableado: ESP32 mal asentado, emparejado de los botones 12×12, rieles `−` independientes |

## Antes de desarmar

Los componentes se reutilizan la semana que viene: este circuito deja de existir y la
documentación es lo único que queda.

- [ ] Foto del cableado en [`media/`](media/)
- [ ] Video de 20 segundos funcionando
- [ ] Tabla de componentes del [README](README.md) completa

## Al cerrar el proyecto

- [ ] Sección "Dónde más se usa este patrón" del [README](README.md)
- [ ] Fila nueva en [`docs/patrones.md`](../../docs/patrones.md)
- [ ] Lo que descubriste de tu kit en [`docs/inventario.md`](../../docs/inventario.md)
- [ ] Si tomaste alguna decisión no obvia: [`docs/decisiones.md`](../../docs/decisiones.md)
- [ ] Estado actualizado acá, en [`firmware/index.md`](../index.md) y en el [README raíz](../../README.md)

## Navegación

[⬅ Índice de proyectos](../index.md) ·
[Pinout](../../shared/config/pinout.h) ·
[Roadmap, semana 1](../../roadmap_v2_kit.md) ·
[Mapa de transferencia](../../docs/patrones.md)
