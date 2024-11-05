from bot import Bot
from threadpool import RunInThread
import discord
import logging
import os

@Bot.tree.command(name = "auth")
@discord.app_commands.describe(access_token = "Your Canvas API Access Token. Run the /help command for information on obtaining one.")
async def auth(Interaction: discord.Interaction, access_token: str):
	logging.getLogger("discord.client").info(f"User {Interaction.user.id} has initiated a link request")

	await Interaction.response.send_message("Starting linking process...", ephemeral = True)

	try:
		await Interaction.edit_original_response(content = "d")
	except Exception as Error:
		logging.getLogger("discord.client").error(f"Link request {Interaction.user.id} had something go very wrong!\n{Error}")

		try:
			# This may not be the exact reason, but we need something to tell them
			#await Bail(Interaction, "Your request has expired.\nPlease try again.")
			pass
		except:
			logging.getLogger("discord.client").error(f"Failed to notify {Interaction.user.id} of error")
