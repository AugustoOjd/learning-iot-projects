# Setup del entorno (WSL2)

Instalación una sola vez, más el comando que hay que repetir en cada reinicio.

---

## 1. PlatformIO — una sola vez

```bash
sudo apt update && sudo apt install -y python3-pip python3-venv
python3 -m venv ~/.pio-venv
~/.pio-venv/bin/pip install -U platformio
echo 'export PATH="$HOME/.pio-venv/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
pio --version
```

### Extensión de VS Code (opcional pero recomendada)

```bash
code --install-extension platformio.platformio-ide
code --install-extension ms-vscode.cpptools
```

⚠️ Tiene que quedar instalada **en el remoto WSL**, no en Windows. Corriendo el comando desde
una terminal de WSL ya queda en el lugar correcto. Desde el marketplace, el botón es
*"Install in WSL: Ubuntu"*.

Da botones de compilar/subir/monitor, selector de entorno (`blink-test` ↔ `s01-panel-alarma`)
y genera `c_cpp_properties.json`, que es lo que hace que IntelliSense resuelva
`#include "config/pinout.h"`.

La extensión trae su propio PIO Core en `~/.platformio`, pero comparte el directorio de
paquetes con el del venv: no se descarga el toolchain dos veces.

### Abrí el workspace, no la carpeta

```bash
code ~/robotic_projects/laboratorio-iot.code-workspace
```

**Esto importa.** La extensión de PlatformIO espera un proyecto por carpeta: si abrís la raíz
del repo directamente, no encuentra ningún `platformio.ini` arriba y te quedás sin botones,
sin IntelliSense y sin selector de entorno.

El archivo `.code-workspace` monta la raíz (para docs e índices) más cada proyecto como
carpetas hermanas. PlatformIO detecta todos y te da un **selector de proyecto en la barra de
estado**, al lado del de entorno.

## 2. USB hacia WSL con `usbipd-win` — una sola vez

**WSL2 no ve los dispositivos USB por defecto.** Sin esto, PlatformIO nunca va a encontrar
el ESP32 aunque lo tengas enchufado.

En **PowerShell de Windows como administrador**:

```powershell
winget install --exact dorssel.usbipd-win
```

Cerrá y reabrí PowerShell como administrador, enchufá el ESP32 y:

```powershell
usbipd list
```

Buscá `CP2102 USB to UART Bridge Controller` (o `CH340`) — en esta máquina es
`VID:PID 10c4:ea60`. **El BUSID depende del puerto físico**, así que cambia si movés la placa.

```powershell
usbipd bind --busid <BUSID>      # una vez por puerto, queda persistente
```

> 💡 **No hace falta ir a PowerShell para consultar.** WSL puede ejecutar binarios de
> Windows, así que desde tu misma terminal Linux:
> ```bash
> usbipd.exe list
> ```
> Si no lo encuentra en el PATH, la ruta completa es
> `"/mnt/c/Program Files/usbipd-win/usbipd.exe"`.
> El `bind` sí necesita PowerShell como administrador; `list` y `attach` no.

En WSL, permiso para el puerto serie:

```bash
sudo usermod -aG dialout $USER
```

Requiere `wsl --shutdown` desde PowerShell y volver a abrir.

---

## 🔁 En cada reinicio o cada vez que reenchufes

Esto es lo único que se repite. En PowerShell como administrador:

```powershell
usbipd attach --wsl --busid 1-2 --auto-attach
```

Con `--auto-attach` el comando queda corriendo y **reconecta solo** cada vez que el ESP32
reaparece: desenchufás y enchufás la placa y el puerto vuelve sin intervención. Dejalo en una
ventana de PowerShell mientras trabajás. Sin ese flag, hay que repetir el `attach` a mano.

Verificar en WSL:

```bash
ls -l /dev/ttyUSB0
```

> **BUSID actual:** `1-2` — CP2102 (`10c4:ea60`). _(Antes estaba en `1-7`; cambió al mover
> la placa de puerto.)_
>
> **El BUSID es del puerto, no del dispositivo.** Si cambiás el ESP32 de puerto USB hay que
> volver a `bind` ese puerto nuevo. Para no repetirlo: **usá siempre el mismo puerto** y
> marcalo. Para ver cuál es ahora, desde WSL: `usbipd.exe list`

---

## 3. Verificar que todo funciona — sin cablear nada

```bash
cd ~/robotic_projects/firmware/s01-panel-alarma/arduino
pio run -e blink-test -t upload
pio device monitor
```

La primera compilación descarga el toolchain de ESP32 (~200 MB) y tarda unos minutos.

Si el LED azul de la placa parpadea y el monitor imprime `LED on` / `LED off`, quedan
confirmados: PlatformIO, el driver USB, el cable (que tenga líneas de datos y no sea de solo
carga), el arranque de la placa y la subida de código.

**A partir de ahí, cualquier problema es de cableado.** Sin este paso, el primer circuito que
falle te deja con cinco sospechosos en vez de uno.

### Si falla

| Síntoma | Causa |
|---|---|
| `Could not open /dev/ttyUSB0` | Falta el `usbipd attach`, o falta el grupo `dialout` (¿hiciste `wsl --shutdown`?) |
| No aparece ningún puerto | El cable USB es de solo carga. Probá otro |
| `Failed to connect to ESP32` | Mantené apretado `BOOT` cuando empieza la subida |
| Símbolos raros en el monitor | Baudrate: tiene que ser 115200 |

---

## 4. MicroPython — cuando llegues a s01 montaje 1

```bash
~/.pio-venv/bin/pip install esptool mpremote

# Una sola vez por chip: flashear el intérprete.
# esptool v5+ usa guiones y ya no lleva el sufijo .py
esptool --chip esp32 --port /dev/ttyUSB0 erase-flash
esptool --chip esp32 --port /dev/ttyUSB0 --baud 460800 \
    write-flash -z 0x1000 ESP32_GENERIC-*.bin

# Por proyecto
cd ~/robotic_projects/firmware/s01-panel-alarma/micropython
mpremote cp ../../../shared/config/pinout.py :
mpremote cp main.py : + repl
```

⚠️ Flashear MicroPython **borra el firmware de Arduino** y viceversa. El chip tiene uno u
otro, no los dos. Para volver a Arduino, simplemente subí un sketch con `pio run -t upload`.

---

## Plan B: PlatformIO en Windows

Si `usbipd` te da pelea, instalá VS Code + PlatformIO **en Windows** y abrí la carpeta por
`\\wsl.localhost\Ubuntu\home\naod_\robotic_projects`. Funciona, pero compila más lento y te
deja el entorno partido en dos.

---

[⬅ README del repo](../README.md) · [Índice de proyectos](../firmware/index.md)
