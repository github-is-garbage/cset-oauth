from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.user import User
from canvasapi.enrollment import Enrollment
from canvasapi.paginated_list import PaginatedList
from datetime import datetime, timezone
import os

def create_canvas_client(token: str) -> Canvas:
	return Canvas(os.getenv("CANVAS_API_URL"), token)

def get_profile(canvas: Canvas) -> dict:
	user = canvas.get_current_user()
	return user.get_profile()

def get_active_cset_course(courses: PaginatedList) -> Course | None:
	for course in courses:
		if not hasattr(course, "name") or "CSET" not in course.name:
			continue

		if hasattr(course, "end_at_date") and course.end_at_date:
			if course.end_at_date < datetime.now(timezone.utc):
				continue

		return course

	return None

def get_instructor_name(course: Course) -> str | None:
	enrollments = course.get_enrollments(type=["TeacherEnrollment"])

	for enrollment in enrollments:
		user = getattr(enrollment, "user", None)

		if user:
			name = user.get("name")

			if name:
				return name

	return None
