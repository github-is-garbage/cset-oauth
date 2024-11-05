from sqlalchemy import create_engine, URL
import os

ConnectionURL = URL.create(
	"mysql+mysqlconnector",

	os.getenv("MYSQL_USERNAME"),
	os.getenv("MYSQL_PASSWORD"),

	os.getenv("MYSQL_URL"),
	os.getenv("MYSQL_PORT"),

	os.getenv("MYSQL_DATABASE")
)

Engine = create_engine(ConnectionURL, echo = True)
