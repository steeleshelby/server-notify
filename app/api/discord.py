import time
import requests
from app.config.config import WEBHOOK_URL

def edit_message(
        players_count: int,
        players: list[str]
):
    timestamp = int(time.time())
    players = "\n".join(f"• {player}" for player in players)

    data = {
        "username": "Buzz",
        "avatar_url": "https://tr.rbxcdn.com/180DAY-5424fdb5e9690277d7e9aea106a8da21/150/150/Image/Webp/noFilter",
        "embeds": [
            {
                "title": "🌲 Pine Tree (EU) 🌲",
                "description": f"**🎮 Players Online: `{players_count}/6`**\n\n**👥 Players:\n** {players}\n\n> **🕒 Updated: <t:{timestamp}:R>**",
                "color": 0x00ff00 if players_count != 6 else 0xff0000,
                "thumbnail": {
                    "url": "https://tr.rbxcdn.com/180DAY-986f7d1ef380e9385e5c8129268fb4c3/150/150/Image/Webp/noFilter"
                }
            }
        ]
    }

    response = requests.patch(WEBHOOK_URL, json=data)

    if int(str(response.status_code)[0]) == 2:
        print("✅ Сообщение успешно отправлено!")
    else:
        print("❌ Ошибка:", response.status_code)
        print(response.text)
