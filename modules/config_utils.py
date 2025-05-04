import os
import json
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".." / ".env"
CONFIG_PATH = BASE_DIR / ".." / ".config"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)

TWITCH_CLIENT_ID = os.getenv("CLIENT_ID", "")
TWITCH_CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
TWITCH_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
TWITCH_REFRESH_TOKEN = os.getenv("REFRESH_TOKEN", "")
TWITCH_AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE", "")
TWITCH_REDIRECT_URI = os.getenv("REDIRECT_URI", "")


def load_config():
    default_config = {"channels": [], "vod_check_interval_minutes": 15}
    if not CONFIG_PATH.exists():
        return default_config
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_config = json.load(f)
            merged = {**default_config, **user_config}
            return merged
    except Exception as e:
        print(f"Failed to parse .config: {e}")
        return default_config
