from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import os
from bot import Bot

from folder_loader import LoadFromFolder

LoadFromFolder("commands")
LoadFromFolder("events")

from sqlalchemy import text
from db import Engine

with Engine.connect() as Connection:
	Connection.execute(text("insert into linked_users values (123, 123, \"test man dude\")"))
	Connection.commit()


Bot.run(os.getenv("BOT_TOKEN"))
