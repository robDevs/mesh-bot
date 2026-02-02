import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from commands import COMMANDS
from bot import BotState, send_reply
from config import SERIAL_PORT, PRIVATE_CHANNEL_NAME

interface = meshtastic.serial_interface.SerialInterface(SERIAL_PORT)
interface.localNode.waitForConfig()

private_channel_index = 1
for ch in interface.localNode.channels or []:
    if ch.settings and ch.settings.name == PRIVATE_CHANNEL_NAME:
        private_channel_index = ch.index
        print(f"Found private channel: {private_channel_index}")
        break

bot = BotState(interface, private_channel_index)

def on_receive(packet, interface):
    print("hit command handler")
    decoded = packet.get("decoded")
    if not decoded:
        return
    
    if str(decoded.get("portnum")) != "TEXT_MESSAGE_APP":
        return
    
    text = decoded.get("text", "").strip()
    if not text.startswith("!"):
        return
    
    sender_id = packet.get("fromId", "unknown")
    sender_node = interface.nodes.get(sender_id)
    sender_name = (
        sender_node["user"].get("longName", sender_id)
        if sender_node else sender_id
    )

    print(f"[MSG] {sender_id}|{sender_name}: {text}")

    parts = text[1:].split()
    command = parts[0].upper()
    args = parts[1:]

    handler = COMMANDS.get(command)
    if not handler:
        send_reply(bot, "Unkown command. Try !help")
        return
    
    try:
        response = handler(bot, sender_name, sender_id, args)
        if response:
            send_reply(bot, response)
    except Exception as e:
        print(f"Command error: {e}")
        send_reply(bot, "⚠️ Command failed")

pub.subscribe(on_receive, "meshtastic.receive.text")
