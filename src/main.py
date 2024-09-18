from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import os
from bot import Bot

from folder_loader import LoadFromFolder

LoadFromFolder("commands")
LoadFromFolder("events")

Bot.run(os.getenv("BOT_TOKEN"))
