from bot import Bot
import discord
import os

@Bot.tree.command(name = "help")
async def help(Interaction: discord.Interaction):
	await Interaction.response.send_message(
		(f"""
		Please generate a Canvas API Access Token to use with this command.
		1. Go to your [profile settings]({ os.environ.get("CANVAS_PROFILE_URL") })
		2. Click on the button labeled "**New Access Token**"
		3. Fill out the "Purpose" textbox with "CSET OAuth" (Case-insensitive)
		4. Click on the button labeled "**Generate Token**"
		5. Copy the entire Token string (About 70 characters)
		6. Run the `/auth` command and set the "access_token" argument to the copied value
		""").replace("\t", ""),

		ephemeral = True,
	)
