import requests
from time import time
from app.config.config import WEBHOOK_URL
from app.logs.change_logger import logger
from app.config.config import (
    SERVER_REGION,
    WEBHOOK_USERNAME,
    AVATAR_URL,
    THUMBNAIL_URL,
    WEBHOOK_URL_SHUTDOWN,
    DISCORD_ID
)

server_info = {
    "username": WEBHOOK_USERNAME if WEBHOOK_USERNAME is not None else "Buzz",
    "avatar_url": AVATAR_URL if AVATAR_URL is not None else "https://tr.rbxcdn.com/180DAY-5424fdb5e9690277d7e9aea106a8da21/150/150/Image/Webp/noFilter",
    "embeds": [
        {
            "title": f"🌲 Pine Tree ({SERVER_REGION}) 🌲",
            "thumbnail": {
                "url": THUMBNAIL_URL if THUMBNAIL_URL is not None else "https://tr.rbxcdn.com/180DAY-986f7d1ef380e9385e5c8129268fb4c3/150/150/Image/Webp/noFilter"
            },
            "footer": {
                "text": "Github link: https://github.com/steeleshelby/server-notify",
                "icon_url": "https://github.githubassets.com/favicons/favicon-dark.png"
            }
        }
    ]
}


shutdown_info = {
    "username": WEBHOOK_USERNAME if WEBHOOK_USERNAME is not None else "Buzz",
    "avatar_url": AVATAR_URL if AVATAR_URL is not None else "https://tr.rbxcdn.com/180DAY-5424fdb5e9690277d7e9aea106a8da21/150/150/Image/Webp/noFilter",
    "embeds": [
        {
            "title": "🔄 Server restart 🔄",
            "thumbnail": {
                "url": THUMBNAIL_URL if THUMBNAIL_URL is not None else "https://tr.rbxcdn.com/180DAY-986f7d1ef380e9385e5c8129268fb4c3/150/150/Image/Webp/noFilter"
            },
            "footer": {
                "text": "Github link: https://github.com/steeleshelby/server-notify",
                "icon_url": "https://github.githubassets.com/favicons/favicon-dark.png"
            }
        }
    ]
}

def edit_server_info(
        players_count: int,
        players: list[str],
        is_server_alive: bool
):
    timestamp = int(time())
    if is_server_alive is True:
        players = "\n".join(f"• {player}" for player in players)

        server_info["embeds"][0]["description"] = f"**🎮 Players Online: `{players_count}`**\n\n**👥 Players:\n** {players}\n\n> **🕒 Updated: <t:{timestamp}:R>**"
        server_info["embeds"][0]["color"] = 0x00ff00 if players_count != 6 else 0xff0000
    else:
        server_info["embeds"][0]["description"] = f"**🎮 Server Status: Offline**\n\n> **🕒 Updated: <t:{timestamp}:R>**"
        server_info["embeds"][0]["color"] = 0x666666

    response = requests.patch(WEBHOOK_URL, json=server_info)

    try:
        response.raise_for_status()
    except requests.HTTPError:
        logger.error(f"Discord (edit_server_info) | Error\nStatus code: {response.status_code}\nResponse text: {response.text}")
        return

    logger.debug("Discord (edit_server_info) | The message was successfully sent")


def shutdown_notify(is_success: bool):
    timestamp = int(time())

    shutdown_info["content"] = f"<@{DISCORD_ID}>" if is_success is False else ""
    shutdown_info["embeds"][0]["description"] = "> ⚒️ **The server has been rebooted**" if is_success is True else "> ⚒️ **The server has not been rebooted**"
    shutdown_info["embeds"][0]["description"] += f"\n> 🕒 **Time: <t:{timestamp}:D>**"
    shutdown_info["embeds"][0]["color"] = 0x00ff00 if is_success is True else 0xff0000

    response = requests.post(WEBHOOK_URL_SHUTDOWN, json=shutdown_info)

    try:
        response.raise_for_status()
    except requests.HTTPError:
        logger.error(f"Discord (shutdown_notify) | Error\nStatus code: {response.status_code}\nResponse text: {response.text}")
        return

    logger.debug("Discord (shutdown_notify) | The message was successfully sent")
