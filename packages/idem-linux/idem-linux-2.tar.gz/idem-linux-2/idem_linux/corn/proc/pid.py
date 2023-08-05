import os


async def load_pid(hub):
    hub.corn.CORN.pid = os.getpid()
