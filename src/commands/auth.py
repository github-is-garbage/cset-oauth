from bot import Bot
import discord
import logging
from canvasapi import Canvas, current_user, paginated_list, course, enrollment, user
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

async def StartUserLink(Interaction: discord.Interaction, AccessToken: str) -> tuple[str, str, str, str]:
	CanvasGateway = Canvas(os.getenv("CANVAS_API_URL"), AccessToken)
	CanvasProfile = await GetUserProfile(CanvasGateway)

	UserName = CanvasProfile.get("name")
	if UserName is None:
		return await Interaction.edit_original_response(content = "This account does not have a valid name") # Should never happen

	Courses: paginated_list.PaginatedList = CanvasGateway.get_courses()
	HasCSET, CSETCourse = await HasCSETCourse(Courses)

	if not HasCSET:
		return await Interaction.edit_original_response(content = "You are not currently enrolled in any CSET course")

	logging.getLogger("discord.client").info(f"User { Interaction.user.id } has CSET course { CSETCourse.name }")

	TeacherEnrollment = await GetCourseTeacher(CSETCourse)
	CourseTeacher: user.User = GetAttributeSafe(TeacherEnrollment, "user")

	if not TeacherEnrollment or not CourseTeacher:
		return await Interaction.edit_original_response(content = "Unable to determine instructor")

	TeacherName = CourseTeacher.get("name")

	if not TeacherName:
		return await Interaction.edit_original_response(content = "Received unnamed instructor") # Should never happen

	StudentID = CanvasProfile.get("id")
	StudentName = CanvasProfile.get("name")
	TeacherID = CourseTeacher.get("id")

	logging.getLogger("discord.client").info(f"User { Interaction.user.id } is { StudentName } ({ StudentID }) linking with { TeacherName } ({ TeacherID })")

	if StudentID == TeacherID:
		await Interaction.edit_original_response(content = f"Linking as instructor `{ TeacherName }`")
	else:
		await Interaction.edit_original_response(content = f"Linking as student `{ StudentName }` for instructor `{ TeacherName }`")

	return StudentID, StudentName, TeacherID, TeacherName

# gross gross gross gross gross gross gross

CSET_TEACHERS = {
	os.getenv("TEACHER_A"): os.getenv("TEACHER_A_ROLE"),
	os.getenv("TEACHER_B"): os.getenv("TEACHER_B_ROLE"),
	os.getenv("TEACHER_C"): os.getenv("TEACHER_C_ROLE"),
	os.getenv("TEACHER_D"): os.getenv("TEACHER_D_ROLE")
}

@Bot.tree.command(name = "auth")
@discord.app_commands.describe(access_token = "Your Canvas API Access Token. Run the /help command for information on obtaining one.")
async def auth(Interaction: discord.Interaction, access_token: str):
	logging.getLogger("discord.client").info(f"User {Interaction.user.id} has initiated a link request")

	await Interaction.response.send_message("Starting linking process...", ephemeral = True)

	try:
		StudentID, StudentName, TeacherID, TeacherName = await StartUserLink(Interaction, access_token)
		TeacherRole: str = CSET_TEACHERS.get(TeacherName)

		if not TeacherName or not TeacherRole:
			return

		logging.getLogger("discord.client").info(f"User { Interaction.user.id } should have role { TeacherRole }")

		print(StudentID, StudentName, TeacherID, TeacherName)
	except Exception as Error:
		logging.getLogger("discord.client").error(f"Link request { Interaction.user.id } had something go very wrong!\n{Error}")

		await Interaction.edit_original_response(content = "Something went wrong :(")
