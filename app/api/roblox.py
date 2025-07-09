import requests

from app.config.config import (
    ROBLOSECURITY,
    PLACE_ID,
    SERVER_NAME
)
from app.logs.change_logger import logger

url = f"https://games.roblox.com/v1/games/{PLACE_ID}/private-servers"

headers = {
    "User-Agent": "Roblox/WinInet",
    "Cookie": f".ROBLOSECURITY={ROBLOSECURITY}"
}

def server_info():
    response = requests.get(url, headers=headers)

    try:
        response.raise_for_status()
    except requests.HTTPError:
        logger.error(f"Roblox | Error\nStatus code: {response.status_code}\nResponse text: {response.text}")
        return

    data = response.json()
    for server in data.get("data", []):
        if server.get('name') != SERVER_NAME:
            continue
        logger.debug("Roblox | The info was received")
        return {
            "is_success": True,
            "playing": server["playing"],
            "players": (
                f"{player['name']} ({player['displayName']})"
                for player in server["players"]
            )
        }
    logger.error("Roblox | We couldn't find your vip server")
    return {
        "is_success": False
    }
