from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import os
from bot import Bot

Bot.run(os.getenv("BOT_TOKEN"))
