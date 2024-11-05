from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import os
from bot import Bot

from folder_loader import LoadFromFolder

LoadFromFolder("commands")
LoadFromFolder("events")
LoadFromFolder("models")

from db import Engine
from models.base import ModelBase

ModelBase.metadata.create_all(Engine, checkfirst = True)

Bot.run(os.getenv("BOT_TOKEN"))
