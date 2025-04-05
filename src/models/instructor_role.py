from models.base import ModelBase

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ctypes import c_uint64

class InstructorRole(ModelBase):
	__tablename__ = "instructor_roles"

	RoleID: Mapped[c_uint64] = mapped_column(
		BIGINT(unsigned = True),

		name = "role_id",
		primary_key = True
	)

	UserID: Mapped[c_uint64] = mapped_column(
		BIGINT(unsigned=True),
		ForeignKey("linked_users.user_id"),

		name = "user_id"
	)

	Instructor: Mapped["LinkedUser"] = relationship("LinkedUser", foreign_keys = [UserID])
