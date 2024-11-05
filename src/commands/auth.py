from bot import Bot
from threadpool import RunInThread
import discord
import logging
from canvasapi import Canvas, current_user
import os

async def GetUserProfile(CanvasGateway: Canvas):
	CanvasUser: current_user.CurrentUser = CanvasGateway.get_current_user()
	CanvasProfile = CanvasUser.get_profile() # If the token is invalid this will error

	return CanvasProfile

@Bot.tree.command(name = "auth")
@discord.app_commands.describe(access_token = "Your Canvas API Access Token. Run the /help command for information on obtaining one.")
async def auth(Interaction: discord.Interaction, access_token: str):
	logging.getLogger("discord.client").info(f"User {Interaction.user.id} has initiated a link request")

	await Interaction.response.send_message("Starting linking process...", ephemeral = True)

	try:
		CanvasGateway = Canvas(os.environ.get("CANVAS_API_URL"), access_token)
		CanvasProfile = await GetUserProfile(CanvasGateway)

		UserName = CanvasProfile.get("name")
		if UserName is None:
			return await Interaction.edit_original_response(content = "This account does not have a valid name") # Should never happen

		await Interaction.edit_original_response(content = f"Linking as `{ CanvasProfile.get("name") }`")
	except Exception as Error:
		logging.getLogger("discord.client").error(f"Link request {Interaction.user.id} had something go very wrong!\n{Error}")

		await Interaction.edit_original_response(content = "Something went wrong :(")
