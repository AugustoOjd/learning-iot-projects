# s02 — Monitor de umbrales

> **Semana 2** · 🐍 · Estado: 🟡 en curso

Monitor de sala de servidores o de heladera de farmacia, con alerta por umbral.

**Técnica central:** ADC, divisor de tensión e histéresis

---

## Por dónde empezar

1. **[README.md](README.md)** — el caso real, la técnica y el criterio de terminado
2. **[INSTRUCCIONES_FISICAS.md](INSTRUCCIONES_FISICAS.md)** — armar el circuito paso a paso, en cuatro montajes
3. **El código** — [🐍 MicroPython](micropython/)
4. **[media/](media/)** — foto y video **antes de desarmar**
5. **Cerrar** — las tres tareas de abajo

## Archivos de esta carpeta

| Archivo | Para qué | Estado |
|---|---|---|
| [`README.md`](README.md) | Caso real, dónde más se aplica, criterio de terminado. La cara de portfolio | |
| [`INSTRUCCIONES_FISICAS.md`](INSTRUCCIONES_FISICAS.md) | Componentes, cómo se ven, cómo se conectan | ✅ |
| [`micropython/`](micropython/) | El código. `mpremote cp main.py : + repl` | |
| [`documentation-days/`](documentation-days/) | Bitácora diaria: qué hice, qué falló y cómo lo encontré | 🟡 |
| [`media/`](media/) | Foto del cableado y video de 20s | ⬜ |

## Bitácora

| Día | Qué pasó |
|---|---|
| [2026-10-11](documentation-days/2026-10-11.md) | Roadmap reordenado (s05↔s07). Placa mapeada a columnas. Montaje 1: zonas ciegas del ADC, la fórmula lineal se equivoca ~180 mV, ruido ±2.5 mV. Falla: riel `−` flotante, diagnosticado usando el ADC como voltímetro |
| [2026-10-25](documentation-days/2026-10-25.md) | Montaje 2: fotorresistencia + 10K. El cuarto da 56K, no 10K: oscuro→ambiente usa solo el 11% del ADC. Regla de diseño: R fija ≈ √(R_oscuro × R_claro). Montaje 3: LM35 a 5V; `ATTN_0DB` + x16 da ±0.09°C; constante de tiempo ~20-25 s; exactitud pendiente sin termómetro. Montaje 4: monitor de heladera con histéresis en temperatura y puerta |

## Antes de desarmar

Los componentes se reutilizan la semana que viene: este circuito deja de existir y la
documentación es lo único que queda.

- [ ] Foto del cableado en [`media/`](media/)
- [ ] Video de 20 segundos funcionando
- [x] Tabla de componentes del [README](README.md) completa

## Al cerrar el proyecto

- [x] Sección "Dónde más se usa este patrón" del [README](README.md)
- [x] Fila nueva en [`docs/patrones.md`](../../docs/patrones.md)
- [x] Lo que descubriste de tu kit en [`docs/inventario.md`](../../docs/inventario.md)
- [x] Si tomaste alguna decisión no obvia: [`docs/decisiones.md`](../../docs/decisiones.md)
- [ ] Estado actualizado acá, en [`firmware/index.md`](../index.md) y en el [README raíz](../../README.md)

## Navegación

[⬅ Índice de proyectos](../index.md) ·
[Pinout](../../shared/config/pinout.h) ·
[Roadmap, semana 2](../../roadmap_v2_kit.md) ·
[Mapa de transferencia](../../docs/patrones.md)
