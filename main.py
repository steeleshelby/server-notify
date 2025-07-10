import threading
from datetime import datetime
from time import sleep
from app.api.roblox import server_info, shutdown_server
from app.api.discord import edit_server_info, shutdown_notify

def wait_until_15():
    triggered = False
    while True:
        now = datetime.now()

        if now.hour == 14 and now.minute == 0 and not triggered:
            shutdown_info = shutdown_server()
            shutdown_notify(shutdown_info["is_success"])
            triggered = True

        elif now.minute != 0:
            triggered = False

        sleep(1)

time_thread = threading.Thread(target=wait_until_15)
time_thread.daemon = True
time_thread.start()

while True:
    info = server_info()
    if info["is_success"] is False:
        sleep(60)
        continue
    edit_server_info(players_count=info["playing"], players=info["players"], is_server_alive=info["is_server_alive"])
    sleep(60)
