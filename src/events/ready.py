from bot import Bot
import logging

@Bot.event
async def on_ready():
	logging.getLogger("discord.client").log(logging.INFO, "Connected to Discord")

	logging.getLogger("discord.client").log(logging.INFO, f"Ready as {Bot.user}")
