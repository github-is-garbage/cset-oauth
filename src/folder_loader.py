from pathlib import Path
import os

EXECUTING_DIRECTORY = Path(__file__).parent.resolve()

def LoadFromFolder(Name):
	for File in os.listdir(EXECUTING_DIRECTORY / Name):
		if not File.endswith(".py"): continue

		__import__(f"{Name}.{File[:-3]}", locals(), globals())
