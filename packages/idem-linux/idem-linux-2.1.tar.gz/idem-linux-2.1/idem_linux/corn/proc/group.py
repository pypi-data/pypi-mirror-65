import os
import grp


async def load_group(hub):
    hub.corn.CORN.gid = os.getegid()
    hub.corn.CORN.groupname = grp.getgrgid(hub.corn.CORN.gid).gr_name
