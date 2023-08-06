import os
import pwd


async def load_console_user(hub):
    name = os.getlogin() if hasattr(os, "getlogin") else None
    hub.corn.CORN.console_username = (name or os.environ.get("LOGNAME") or "root")
    hub.corn.CORN.console_user = pwd.getpwnam(hub.corn.CORN.console_username).pw_uid
