import os
import pwd


async def load_console_user(hub):
    hub.corn.CORN.console_username = (
        os.getlogin() or os.environ.get("LOGNAME") or "root"
    )
    hub.corn.CORN.console_user = pwd.getpwnam(hub.corn.CORN.console_username).pw_uid
