import requests
from app.config.config import (
    ROBLOSECURITY,
    PLACE_ID,
    SERVER_NAME
)

url = f"https://games.roblox.com/v1/games/{PLACE_ID}/private-servers"

headers = {
    "User-Agent": "Roblox/WinInet",
    "Cookie": f".ROBLOSECURITY={ROBLOSECURITY}"
}

def server_info():
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for server in data.get("data", []):
            if server.get('name') != SERVER_NAME:
                continue
            return {
                "is_success": True,
                "playing": server["playing"],
                "players": [
                    f"{player['name']} ({player['displayName']})"
                    for player in server["players"]
                ]
            }
    else:
        return {
            "is_success": False
        }
