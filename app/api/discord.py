import requests
from time import time
from app.config.config import WEBHOOK_URL
from app.logs.change_logger import logger
from app.config.config import SERVER_REGION, DISCORD_USERNAME, AVATAR_URL, THUMBNAIL_URL

data = {
    "username": DISCORD_USERNAME if DISCORD_USERNAME is not None else "Buzz",
    "avatar_url": AVATAR_URL if AVATAR_URL is not None else "https://tr.rbxcdn.com/180DAY-5424fdb5e9690277d7e9aea106a8da21/150/150/Image/Webp/noFilter",
    "embeds": [
        {
            "title": f"🌲 Pine Tree ({SERVER_REGION}) 🌲",
            "thumbnail": {
                "url": THUMBNAIL_URL if THUMBNAIL_URL is not None else "https://tr.rbxcdn.com/180DAY-986f7d1ef380e9385e5c8129268fb4c3/150/150/Image/Webp/noFilter"
            }
        }
    ]
}

def edit_message(
        players_count: int,
        players: list[str]
):
    timestamp = int(time())
    players = "\n".join(f"• {player}" for player in players)

    data["embeds"][0]["description"] = f"**🎮 Players Online: `{players_count}/6`**\n\n**👥 Players:\n** {players}\n\n> **🕒 Updated: <t:{timestamp}:R>**"
    data["embeds"][0]["color"] = 0x00ff00 if players_count != 6 else 0xff0000

    response = requests.patch(WEBHOOK_URL, json=data)

    try:
        response.raise_for_status()
    except requests.HTTPError:
        logger.error(f"Discord | Error\nStatus code: {response.status_code}\nResponse text: {response.text}")
        return

    logger.debug("Discord | The message was successfully sent")
