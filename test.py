import meshtastic.serial_interface

SERIAL_PORT = "/dev/tty.usbserial-0001"

iface = meshtastic.serial_interface.SerialInterface(SERIAL_PORT)
print("Connected!")
iface.close()
