import discord
from discord import app_commands
from discord.ext import commands

from sqlalchemy.orm import Session
from core.db import Engine
from models.section_role import SectionRole
from enums.sections import SectionType

class RegisterCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.command(name = "register", description = "Link an instructor's email with a section and role.")
	@app_commands.describe(
		name = "Instructor name as it appears in Canvas",
		section = "Course section this instructor teaches",
		role = "Discord role to assign to students"
	)
	async def register(
		self,
		interaction: discord.Interaction,
		name: str,
		section: SectionType,
		role: discord.Role
	):
		with Session(Engine) as db:
			existing = db.get(SectionRole, name.lower())

			if existing:
				existing.RoleID = role.id
				existing.Section = section.value

				msg = "Updated existing mapping."
			else:
				db.add(SectionRole(
					InstructorName = name.lower(),
					Section = section.value,
					RoleID = role.id
				))

				msg = "Registered new instructor-section-role mapping." # words words words

			db.commit()

		await interaction.response.send_message(msg, ephemeral = True)

async def setup(bot: commands.Bot):
	await bot.add_cog(RegisterCommand(bot))
