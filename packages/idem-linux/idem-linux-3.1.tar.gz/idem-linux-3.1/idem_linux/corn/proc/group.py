import os
import grp


async def load_group(hub):
    hub.corn.CORN.gid = os.getegid()
    try:
        hub.corn.CORN.groupname = grp.getgrgid(hub.corn.CORN.gid).gr_name
    except KeyError:
        hub.corn.CORN.groupname = None
