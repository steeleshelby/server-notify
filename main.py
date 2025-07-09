from time import sleep
from app.api.roblox import server_info
from app.api.discord import edit_message

while True:
    info = server_info()
    if info["is_success"] is False:
        sleep(60)
        continue
    edit_message(
        players_count=info["playing"],
        players=info["players"]
    )
    sleep(60)
