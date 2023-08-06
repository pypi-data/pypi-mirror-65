import getpass
import pwd


async def load_console_user(hub):
    hub.corn.CORN.console_username = getpass.getuser()
    hub.corn.CORN.console_user = pwd.getpwnam(hub.corn.CORN.console_username).pw_uid
