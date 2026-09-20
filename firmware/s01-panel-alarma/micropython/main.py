# Ver README.md del proyecto. Pines en shared/config/pinout.py
#
# Flashear MicroPython en el chip (una sola vez):
#   esptool.py --chip esp32 erase_flash
#   esptool.py --chip esp32 write_flash -z 0x1000 ESP32_GENERIC-*.bin
#
# Subir y correr:
#   mpremote cp ../../../shared/config/pinout.py :
#   mpremote cp main.py : + repl
