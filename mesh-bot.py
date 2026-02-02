import time
import meshtastic
import meshtastic.serial_interface
from meshtastic.protobuf.portnums_pb2 import PortNum
from pubsub import pub

SERIAL_PORT = "/dev/ttyUSB0"
PRIVATE_CHANNEL_NAME = "Home"
NODE_NAME = "pi-bot"

# Keep track of bot start time
start_time = time.time()

# Connect to the radio
interface = meshtastic.serial_interface.SerialInterface(SERIAL_PORT)

# Wait for node config to sync
interface.localNode.waitForConfig()

# Detect private channel index
private_channel_index = None
for ch in interface.localNode.channels or []:
    if ch.settings and ch.settings.name == PRIVATE_CHANNEL_NAME:
        private_channel_index = ch.index
        print(f"found private channel: {private_channel_index}")
        break

if private_channel_index is None:
    print(f"Private channel '{PRIVATE_CHANNEL_NAME}' not found. Defaulting to index 1.")
    private_channel_index = 1

print(f"Using private channel '{PRIVATE_CHANNEL_NAME}' with index {private_channel_index}")

# === MESSAGE HANDLER ===
def on_receive(packet, interface):
    decoded = packet.get("decoded")
    if not decoded:
        return

    # Only handle text messages
    if str(decoded.get("portnum")) != "TEXT_MESSAGE_APP":
        return

    text = decoded.get("text", "").strip()
    sender = packet.get("fromId", "unknown")

    sender_id = packet.get("fromId")  # packet 'fromId'
    sender_node = interface.nodes.get(sender_id)

    if sender_node:
        sender_name = sender_node['user'].get('longName', str(sender_id))
    else:
        sender_name = str(sender_id)

    print(f"[MSG] {sender}|{sender_name}: {text}")

    # Command handling
    if not text.startswith("!"):
        return

    # Remove the "!" to get the command
    cmd = text[1:].upper()
    response = None
    if cmd == "PING":
        response = "PONG 🛰️"
    elif cmd == "HELLO":
        response = f"Hello from {NODE_NAME}"
    
     # === STATUS COMMAND ===
    elif cmd == "STATUS":
        uptime = int(time.time() - start_time)
        hours, remainder = divmod(uptime, 3600)
        minutes, seconds = divmod(remainder, 60)

        num_nodes = len(interface.nodes)  # how many nodes the bot knows
        response = (
            f"Uptime: {hours}h {minutes}m {seconds}s\n"
            f"Known nodes in mesh: {num_nodes}"
        )

    if response:
        # Always send on the private channel
        interface.sendText(response, channelIndex=private_channel_index)
        print(f"→ Replied on private channel {private_channel_index}")

# Subscribe to Meshtastic receive topic
pub.subscribe(on_receive, "meshtastic.receive.text")

# === MAIN LOOP ===
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")
    interface.close()
