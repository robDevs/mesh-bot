import time
import json
import os
from config import STATE_FILE, ADMIN_NODES

class BotState:
    def __init__(self, interface, channel_index):
        self.interface = interface
        self.channel_index = channel_index
        self.start_time = time.time()
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "notes": [],
        }
    
    def save_state(self):
        with open(STATE_FILE, "W") as f:
            json.dump(self.state, f, indent=2)

def send_reply(bot, text):
    bot.interface.sendText(text, channelIndex=bot.channel_index)
    print(f"→ Replied on channel {bot.channel_index}")

def is_admin(sender_id):
    return sender_id in ADMIN_NODES