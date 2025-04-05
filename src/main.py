from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import os
import asyncio
from bot import Bot
from core.db import create_all_tables

create_all_tables()

async def load_extensions(): # Stupid
	await Bot.load_extension("commands.auth")
	await Bot.load_extension("commands.register")

asyncio.run(load_extensions())

import events.ready

Bot.run(os.getenv("BOT_TOKEN"))
