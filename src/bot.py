import discord
from discord.ext import commands

Intentions = discord.Intents.default()
Intentions.members = True

Bot = commands.Bot(
	command_prefix = ";",
	intents = Intentions,

	case_insensitive = True
)
