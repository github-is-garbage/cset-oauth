from sqlalchemy import create_engine, URL
from models.base import ModelBase
import os

ConnectionURL = URL.create(
	"mysql+mysqlconnector",

	username = os.getenv("MYSQL_USERNAME"),
	password = os.getenv("MYSQL_PASSWORD"),
	host = os.getenv("MYSQL_URL"),
	port = int(os.getenv("MYSQL_PORT")),
	database = os.getenv("MYSQL_DATABASE")
)

Engine = create_engine(ConnectionURL, echo = True)

def create_all_tables():
	from models.linked_user import LinkedUser
	from models.instructor_role import InstructorRole
	from models.section_role import SectionRole

	ModelBase.metadata.create_all(Engine, checkfirst = True)
