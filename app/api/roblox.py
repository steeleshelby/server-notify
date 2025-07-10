import requests
from app.config.config import (
    ROBLOSECURITY,
    PLACE_ID,
    VIP_SERVER_ID
)
from app.logs.change_logger import logger

def server_info():
    response = requests.get(f"https://games.roblox.com/v1/games/{PLACE_ID}/private-servers", headers={
    "User-Agent": "Roblox/WinInet",
    "Cookie": f".ROBLOSECURITY={ROBLOSECURITY}"
})
    try:
        response.raise_for_status()
    except requests.HTTPError:
        logger.error(f"Roblox (server_info) | Error\nStatus code: {response.status_code}\nResponse text: {response.text}")
        return

    data = response.json()
    for server in data.get("data", []):
        if server.get('vipServerId') != VIP_SERVER_ID:
            continue
        logger.debug("Roblox (server_info) | The info was received")
        try:
            return {
                "is_success": True,
                "is_server_alive": True,
                "playing": str(server["playing"]) + "/" + str(server["maxPlayers"]),
                "players": (
                    f"{player['name']} ({player['displayName']})"
                    for player in server["players"]
                )
            }
        except KeyError:
            return {
                "is_success": True,
                "is_server_alive": False
            }
    logger.error("Roblox (server_info) | We couldn't find your vip server")
    return {
        "is_success": False
    }

def shutdown_server():
    csrf_token_response = requests.post(
        "https://apis.roblox.com/matchmaking-api/v1/game-instances/shutdown",
        headers={"Content-Type": "application/json"},
        cookies={".ROBLOSECURITY": ROBLOSECURITY}
    )

    csrf_token = csrf_token_response.headers.get("x-csrf-token")
    if not csrf_token:
        logger.error("Roblox (shutdown[csrf_token_response]) | Failed to get X-CSRF-TOKEN")
        return {
            "is_success": False
        }

    shutdown_response = requests.post(
        "https://apis.roblox.com/matchmaking-api/v1/game-instances/shutdown",
        headers={
            "Content-Type": "application/json",
            "x-csrf-token": csrf_token
        },
        cookies={".ROBLOSECURITY": ROBLOSECURITY},
        json={
            "placeId": PLACE_ID,
            "privateServerId": VIP_SERVER_ID
        }
    )

    try:
        shutdown_response.raise_for_status()
    except requests.HTTPError:
        logger.error(f"Roblox | Error (shutdown[shutdown_response])\nStatus code: {shutdown_response.status_code}\nResponse text: {shutdown_response.text}")
        return {
            "is_success": False
        }

    return {
        "is_success": True
    }
