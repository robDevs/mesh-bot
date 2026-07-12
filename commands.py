import time
import socket
import psutil
from config import NODE_NAME
from bot import send_node_reply

def cmd_ping(bot, sender, sender_id, args):
    """Respond with PONG"""
    return "PONG 🛰️"

def cmd_hello(bot, sender, sender_id, args):
    """Say hello"""
    return f"Hello from {NODE_NAME}"

def cmd_test(bot, sender, sender_id, args):
    hop_start = args.get("hopStart")
    hop_limit = args.get("hopLimit")
    print(f"hop start: {hop_start}")
    hops = hop_limit - hop_start
    relay_id = args.get("relayNode")
    relay = bot.interface.nodes.get(relay_id)
    print(f"relay: {relay}")
    relay_name = (
        relay["user"].get("longName", relay_id)
        if relay else relay_id
    )
    message = (
        f"Recieved test:\n"
        f"Hops: {hops}\n"
        f"Relay: {relay_name}"
    )
    send_node_reply(bot, message, sender_id, sender)

def cmd_status(bot, sender, sender_id, args):
    """Show uptime, mesh info, and internet connectivity"""
    uptime = int(time.time() - bot.start_time)
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)

    num_nodes = len(bot.interface.nodes)

    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        internet_status = "Online 🌐"
    except OSError:
        internet_status = "Offline ❌"

    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    mem_percent = mem.percent

    # Build message
    msg = (
        f"Uptime: {hours}h {minutes}m {seconds}s\n"
        f"Mesh nodes: {num_nodes}\n"
        f"Internet: {internet_status}\n"
        f"CPU: {cpu:.0f}% | Mem: {mem_percent:.0f}%"
    )

    return msg[:200]

COMMANDS = {
    "PING": cmd_ping,
    "HELLO": cmd_hello,
    "TEST": cmd_test,
    "STATUS": cmd_status,
}
