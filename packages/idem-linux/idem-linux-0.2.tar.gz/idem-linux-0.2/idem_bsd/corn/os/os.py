import logging
import shutil

log = logging.getLogger(__name__)


async def _load_osrelease_freebsd(hub) -> str:
    version = shutil.which("freebsd-version")
    if version:
        return (await hub.exec.cmd.run([version, "-u"])).stdout


async def load_osbuild(hub):
    sysctl = shutil.which("sysctl")

    if sysctl:
        hub.corn.CORN.osbuild = (
            await hub.exec.cmd.run([sysctl, "-n", "kern.osrevision"])
        ).stdout.strip()
    else:
        hub.corn.CORN.osbuild = "unknown"


async def load_oscodename(hub):
    """
    BSD Doesn't have codenames so we'll use the BSD version of the user environment.
    """
    uname = shutil.which("uname")
    if uname:
        hub.corn.CORN.oscodename = (
            await hub.exec.cmd.run([uname, "-U"])
        ).stdout.strip()
    else:
        hub.corn.CORN.oscodename = "unknown"


async def load_linux_distribution(hub):
    hub.corn.CORN.os = hub.corn.CORN.kernel
    full_release = await _load_osrelease_freebsd(hub) or hub.corn.CORN.kernelrelease
    hub.corn.CORN.osmanufactuer = "unknown"
    hub.corn.CORN.osrelease = full_release.split("-", 1)[0]
    hub.corn.CORN.osfullname = f"{hub.corn.CORN.os}-{full_release}"
    hub.corn.CORN.osrelease_info = tuple(
        int(x) if x.isdigit() else x for x in hub.corn.CORN.osrelease.split(".")
    )
    hub.corn.CORN.osmajorrelease = hub.corn.CORN.osrelease_info[0]
    hub.corn.CORN.osfinger = f"{hub.corn.CORN.os}-{hub.corn.CORN.osmajorrelease}"
