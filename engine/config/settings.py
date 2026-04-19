

# settings.py

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")

    if not any([TG_BOT_TOKEN, TG_CHAT_ID]):
        raise ValueError(
            "Missing critical credentials! Ensure all config variables are set corrwctly.")
