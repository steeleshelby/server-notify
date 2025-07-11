from yaml import safe_load
from app.exceptions.region import RegionException

file_path = "app/config/config.yml"

with open(file_path, "r", encoding="utf-8") as file:
    config_data = safe_load(file)

WEBHOOK_URL = config_data["webhook_url"] + "/messages/" + str(config_data["message_id"])
ROBLOSECURITY = config_data["roblosecurity"]
PLACE_ID = config_data["place_id"]
VIP_SERVER_ID = config_data["vip_server_id"]
SERVER_REGION = config_data["server_region"]
WEBHOOK_USERNAME = config_data["webhook_username"]
AVATAR_URL = config_data["avatar_url"]
THUMBNAIL_URL = config_data["thumbnail_url"]
WEBHOOK_URL_SHUTDOWN = config_data["webhook_url_shutdown"]
DISCORD_ID = config_data["discord_id"]

if SERVER_REGION.upper() not in ("EU", "US", "AS", "SA", "AF", "OC", "RU", "CN", "JP", "KR", "ME", "IN"):
    raise RegionException(invalid_region=SERVER_REGION.upper())
