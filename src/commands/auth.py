import discord
from discord import app_commands
from discord.ext import commands

from bot import Bot

class AuthCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.command(name = "auth", description = "Link your Canvas account using an API token.")
	@app_commands.describe(access_token = "Your Canvas Access Token (see /help for instructions)")
	async def auth(self, interaction: discord.Interaction, access_token: str):
		await interaction.response.send_message(
			content = f"Received access token: `{access_token[:5]}...` (token truncated)",
			ephemeral = True
		)

async def setup(bot: commands.Bot):
	await bot.add_cog(AuthCommand(bot))
