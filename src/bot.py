import discord
from discord.ext import commands

Intents = discord.Intents.default()
Intents.members = True

Bot = commands.Bot(
	command_prefix = ";",
	intents = Intents,
	case_insensitive = True
)
