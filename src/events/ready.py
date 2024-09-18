from bot import Bot
import discord
import logging
import os

@Bot.event
async def on_ready():
	logging.getLogger("discord.client").log(logging.INFO, "Connected to Discord")

	# TODO: Make this global
	logging.getLogger("discord.client").log(logging.INFO, "Syncing commands to test guild")
	TestServer = discord.Object(int(os.getenv("GUILD_ID"))) # TODO: This sucks

	Bot.tree.copy_global_to(guild = TestServer)
	await Bot.tree.sync(guild = TestServer)

	logging.getLogger("discord.client").log(logging.INFO, f"Ready as {Bot.user}")
