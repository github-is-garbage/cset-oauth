from models.base import ModelBase

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ctypes import c_uint64

class LinkedUser(ModelBase):
	__tablename__ = "linked_users"

	UserID: Mapped[c_uint64] = mapped_column(
		BIGINT(unsigned = True),

		name = "user_id",
		primary_key = True
	)

	DiscordID: Mapped[c_uint64] = mapped_column(
		BIGINT(unsigned = True),

		name = "discord_id"
	)

	Name: Mapped[str] = mapped_column(
		VARCHAR(255),

		name = "name"
	)

	InstructorID: Mapped[c_uint64 | None] = mapped_column(
		BIGINT(unsigned = True),
		ForeignKey("linked_users.user_id"),

		name = "instructor_id",
		nullable = True
	)

	DiscordRoleID: Mapped[c_uint64 | None] = mapped_column(
		BIGINT(unsigned = True),
		ForeignKey("instructor_roles.role_id"),

		name = "instructor_role_id",
		nullable = True
	)

	Instructor: Mapped["LinkedUser"] = relationship("LinkedUser", remote_side = [UserID])
