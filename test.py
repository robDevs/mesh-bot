import meshtastic.serial_interface

SERIAL_PORT = "/dev/ttyUSB0"

iface = meshtastic.serial_interface.SerialInterface(SERIAL_PORT)
print("Connected!")
iface.close()
