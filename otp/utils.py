import asyncio


async def run_async(func, *args):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, func, *args)
