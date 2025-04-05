from models.base import ModelBase

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, ENUM
from sqlalchemy.orm import mapped_column, Mapped
from ctypes import c_uint64

class SectionRole(ModelBase):
	__tablename__ = "section_roles"

	Email: Mapped[str] = mapped_column(
		VARCHAR(255),

		name = "email",
		primary_key = True
	)

	RoleID: Mapped[c_uint64] = mapped_column(
		BIGINT(unsigned = True),

		name = "role_id"
	)

	Section: Mapped[str] = mapped_column(
		ENUM("AM_FRESHMAN", "PM_FRESHMAN", "AM_SOPHOMORE", "PM_SOPHOMORE"),

		name = "section"
	)
