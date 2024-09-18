import asyncio
from concurrent.futures import ThreadPoolExecutor

ThreadPool = ThreadPoolExecutor()

async def RunInThread(Function, *Args, **KwArgs):
	Loop = asyncio.get_event_loop()

	return await Loop.run_in_executor(ThreadPool, Function, *Args, **KwArgs)
