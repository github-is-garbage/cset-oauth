from bot import Bot
import discord

@Bot.tree.command(name = "auth")
async def auth(interaction: discord.Interaction):
	await interaction.response.send_message("Response", ephemeral = True)
