import time
import meshtastic
import meshtastic.serial_interface
from meshtastic.protobuf.portnums_pb2 import PortNum

# === CONFIG ===
SERIAL_PORT = "/dev/tty.usbserial-0001"
PRIVATE_CHANNEL_INDEX = 1   # <-- your private channel
NODE_NAME = "pi-bot"

# === CONNECT ===
interface = meshtastic.serial_interface.SerialInterface(SERIAL_PORT)

print(f"Connected to Meshtastic node on {SERIAL_PORT}")
print(f"Listening ONLY on private channel {PRIVATE_CHANNEL_INDEX}")

# === MESSAGE HANDLER ===
def on_receive(packet, interface):
    decoded = packet.get("decoded")
    if not decoded:
        return

    # Only process text messages
    if decoded.get("portnum") != PortNum.TEXT_MESSAGE_APP:
        return

    # Ignore messages not on our private channel
    channel = decoded.get("channel")
    if channel != PRIVATE_CHANNEL_INDEX:
        return

    text = decoded.get("text", "").strip()
    sender = packet.get("fromId")

    print(f"[CH {channel}] {sender}: {text}")
    return

    # === COMMAND HANDLING ===
    response = None

    cmd = text.upper()

    if cmd == "PING":
        response = "PONG 🛰️"

    elif cmd == "HELLO":
        response = f"Hello from {NODE_NAME}"

    # Add more commands here
    # elif cmd.startswith("DO_SOMETHING"):

    if response:
        interface.sendText(
            response,
            channelIndex=PRIVATE_CHANNEL_INDEX
        )
        print(f"→ Responded on channel {PRIVATE_CHANNEL_INDEX}")

# Register callback
interface.onReceive += on_receive

# === MAIN LOOP ===
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")
    interface.close()
