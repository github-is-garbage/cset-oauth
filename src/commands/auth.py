from bot import Bot
from threadpool import RunInThread
import discord
import logging
from canvasapi import Canvas, current_user, paginated_list, course, enrollment
from datetime import datetime, timezone
import os

def GetAttributeSafe(Object: any, Attribute: str):
	return getattr(Object, Attribute) if hasattr(Object, Attribute) else None

async def GetUserProfile(CanvasGateway: Canvas):
	CanvasUser: current_user.CurrentUser = CanvasGateway.get_current_user()
	CanvasProfile = CanvasUser.get_profile() # If the token is invalid this will error

	return CanvasProfile

async def HasCSETCourse(Courses: paginated_list.PaginatedList) -> tuple[bool, course.Course]:
	for Course in Courses:
		CourseName: str = GetAttributeSafe(Course, "name")
		if not CourseName: continue # Should never happen

		Index: int = CourseName.find("CSET")
		if Index < 0: continue # Not CSET

		EndDate: datetime = GetAttributeSafe(Course, "end_at_date")
		if not EndDate: continue
		if EndDate < datetime.now(timezone.utc): continue # Closed

		return True, Course

	return False, None

async def GetCourseTeacher(Course: course.Course) -> enrollment.Enrollment:
	for Enrollment in Course.get_enrollments(type = [ "TeacherEnrollment" ]):
		return Enrollment

	return None

async def StartUserLink(Interaction: discord.Interaction, AccessToken: str) -> str:
	CanvasGateway = Canvas(os.environ.get("CANVAS_API_URL"), AccessToken)
	CanvasProfile = await GetUserProfile(CanvasGateway)

	UserName = CanvasProfile.get("name")
	if UserName is None:
		return await Interaction.edit_original_response(content = "This account does not have a valid name") # Should never happen

	Courses: paginated_list.PaginatedList = CanvasGateway.get_courses()
	HasCSET, CSETCourse = await HasCSETCourse(Courses)

	if not HasCSET:
		return await Interaction.edit_original_response(content = "You are not currently enrolled in any CSET course")

	TeacherEnrollment = await GetCourseTeacher(CSETCourse)
	CourseTeacher = GetAttributeSafe(TeacherEnrollment, "user")

	if not TeacherEnrollment or not CourseTeacher:
		return await Interaction.edit_original_response(content = "Unable to determine instructor")

	TeacherName = CourseTeacher.get("name")

	if not TeacherName:
		return await Interaction.edit_original_response(content = "Received unnamed instructor") # Should never happen

	await Interaction.edit_original_response(content = f"Linking as `{ CanvasProfile.get("name") }` for `{ TeacherName }`")

	return TeacherName

@Bot.tree.command(name = "auth")
@discord.app_commands.describe(access_token = "Your Canvas API Access Token. Run the /help command for information on obtaining one.")
async def auth(Interaction: discord.Interaction, access_token: str):
	logging.getLogger("discord.client").info(f"User {Interaction.user.id} has initiated a link request")

	await Interaction.response.send_message("Starting linking process...", ephemeral = True)

	try:
		TeacherName: str = await StartUserLink(Interaction, access_token)

		print(TeacherName)
	except Exception as Error:
		logging.getLogger("discord.client").error(f"Link request {Interaction.user.id} had something go very wrong!\n{Error}")

		await Interaction.edit_original_response(content = "Something went wrong :(")
