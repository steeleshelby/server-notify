from yaml import safe_load

file_path = "app/config/config.yml"

with open(file_path, "r", encoding="utf-8") as file:
    config_data = safe_load(file)

WEBHOOK_URL = config_data["webhook_url"] + "/messages/" + str(config_data["message_id"])
ROBLOSECURITY = config_data["roblosecurity"]
PLACE_ID = config_data["place_id"]
SERVER_NAME = config_data["server_name"]