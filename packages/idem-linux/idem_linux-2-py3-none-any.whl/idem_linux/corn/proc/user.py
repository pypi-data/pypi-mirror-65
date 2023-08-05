import os
import pwd


async def load_user(hub):
    hub.corn.CORN.uid = os.geteuid()
    hub.corn.CORN.username = pwd.getpwuid(hub.corn.CORN.uid).pw_name
