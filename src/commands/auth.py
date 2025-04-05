import discord
from discord import app_commands
from discord.ext import commands

from sqlalchemy.orm import Session
from core.db import Engine
from models.linked_user import LinkedUser
from models.section_role import SectionRole

from canvas import service as canvas_service

class AuthCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.command(name = "auth", description = "Link your Canvas account using an API token.")
	@app_commands.describe(access_token = "Your Canvas Access Token (see /help for instructions)")
	async def auth(self, interaction: discord.Interaction, access_token: str):
		await interaction.response.send_message("Checking your Canvas info...", ephemeral = True)

		try:
			canvas = canvas_service.create_canvas_client(access_token)
			profile = canvas_service.get_profile(canvas)
			courses = canvas.get_courses()

			student_id = profile.get("id")
			student_name = profile.get("name")

			cset_course = canvas_service.get_active_cset_course(courses)
			if not cset_course:
				await interaction.edit_original_response(content = "You are not currently in an active CSET course.")
				return

			instructor_name = canvas_service.get_instructor_name(cset_course)
			if not instructor_name:
				await interaction.edit_original_response(content = "Could not find the instructor's name.")
				return

			with Session(Engine) as db:
				section_info = db.get(SectionRole, instructor_name)

				if not section_info:
					await interaction.edit_original_response(
						content = f"Instructor `{instructor_name}` is not registered. Ask an admin to run `/register`."
					)
					return

				role_id = section_info.RoleID
				section_name = section_info.Section

				existing = db.get(LinkedUser, student_id)
				if existing:
					await interaction.edit_original_response(
						content = f"You are already linked as `{existing.Name}` in section `{section_name}`."
					)
					return

				db.add(LinkedUser(
					UserID = student_id,
					DiscordID = interaction.user.id,
					Name = student_name,
					DiscordRoleID = role_id
				))
				db.commit()

			# roler
			role = interaction.guild.get_role(role_id)
			if role:
				member = interaction.guild.get_member(interaction.user.id)
				if member:
					await member.add_roles(role, reason = "Canvas auth role assignment")

			await interaction.edit_original_response(
				content = f"Linked as `{student_name}`. You have been assigned to `{section_name}`."
			)

		except Exception as e:
			await interaction.edit_original_response(
				content = f"Something went wrong while linking: `{str(e)}`"
			)

async def setup(bot: commands.Bot):
	await bot.add_cog(AuthCommand(bot))
