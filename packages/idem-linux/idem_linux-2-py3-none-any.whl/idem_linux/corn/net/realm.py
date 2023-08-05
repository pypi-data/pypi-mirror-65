import aiofiles
import os
import shutil


async def load_windows_domain(hub):
    hub.corn.CORN.windowsdomain = None
    hub.corn.CORN.windowsdomaintype = "Unknown"

    if shutil.which("realm") and not hub.corn.CORN.windowsdomain:
        realms = (await hub.exec.cmd.run(["realm", "list", "--name-only"]))[
            "stdout"
        ].splitlines()
        hub.corn.CORN.windowsdomain = realms[0] if realms else "unknown"
        hub.corn.CORN.windowsdomaintype = "ldap"

    if os.path.exists("/etc/krb5.conf") and not hub.corn.CORN.windowsdomain:
        async with aiofiles.open("/etc/krb5.conf") as fp:
            async for line in fp:
                if "default_realm" in line:
                    hub.corn.CORN.windowsdomain = line.split("=")[1].strip()
                    hub.corn.CORN.windowsdomaintype = "kerberos"
                    break
    if (
        shutil.which("smbd")
        and shutil.which("testparm")
        and not hub.corn.CORN.windowsdomain
    ):
        ret = await hub.exec.cmd.run("testparm")
        if not ret["retcode"]:
            smb_config = ret["stdout"].splitlines()
            for line in smb_config:
                if "realm" in line:
                    hub.corn.CORN.windowsdomain = line.split("=")[1].strip()
                    hub.corn.CORN.windowsdomaintype = "samba"
                    break
