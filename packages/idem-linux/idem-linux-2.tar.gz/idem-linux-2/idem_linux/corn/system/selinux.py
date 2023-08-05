import shutil


async def load_selinux(hub):
    if shutil.which("selinuxenabled"):
        hub.corn.CORN.selinux.enabled = (await hub.exec.cmd.run("selinuxenabled"))[
            "retcode"
        ] == 0

        if shutil.which("getenforce"):
            hub.corn.CORN.selinux.enforced = (await hub.exec.cmd.run("getenforce"))[
                "stdout"
            ].strip()
