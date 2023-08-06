import aiofiles
import logging
import os
import shutil

log = logging.getLogger(__name__)


async def load_systemd(hub):
    cmd = shutil.which("systemctl")
    if cmd and shutil.which("localectl"):
        log.debug("Adding systemd corn")
        systemd_info = (
            (await hub.exec.cmd.run([cmd, "--version"])).stdout.strip().splitlines()
        )
        hub.corn.CORN.systemd.version = systemd_info[0].split()[1]
        hub.corn.CORN.systemd.features = systemd_info[1]


async def load_init(hub):
    # Add init grain
    hub.corn.CORN.init = "unknown"
    log.debug("Adding init grain")

    system = "/run/systemd/system"
    cmdline = "/proc/1/cmdline"

    if os.path.exists(system) and os.stat(system):
        hub.corn.CORN.init = "systemd"
    elif os.path.exists(cmdline):
        async with aiofiles.open("/proc/1/cmdline") as fhr:
            init_cmdline = (await fhr.read()).replace("\x00", " ").split()
            if len(init_cmdline) >= 1:
                init_bin = shutil.which(init_cmdline[0])
                if init_bin.endswith("bin/init"):
                    supported_inits = (b"upstart", b"sysvinit", b"systemd")
                    edge_len = max(len(x) for x in supported_inits) - 1
                    buf_size = hub.OPT.get("file_buffer_size", 262144)
                    try:
                        async with aiofiles.open(init_bin, "rb") as fp_:
                            edge = b""
                            buf = (await fp_.read(buf_size)).lower()
                            while buf:
                                if isinstance(buf, str):
                                    # This makes testing easier
                                    buf = buf.encode()
                                buf = edge + buf
                                for item in supported_inits:
                                    if item in buf:
                                        item = item.decode("utf-8")
                                        hub.corn.CORN.init = item
                                        buf = b""
                                        break
                                edge = buf[-edge_len:]
                                buf = (await fp_.read(buf_size)).lower()
                    except (IOError, OSError) as exc:
                        log.error(
                            "Unable to read from init_bin (%s): %s", init_bin, exc
                        )
                elif shutil.which("supervisord") in init_cmdline:
                    hub.corn.CORN.init = "supervisord"
                elif shutil.which("dumb-init") in init_cmdline:
                    # https://github.com/Yelp/dumb-init
                    hub.corn.CORN.init = "dumb-init"
                elif shutil.which("tini") in init_cmdline:
                    # https://github.com/krallin/tini
                    hub.corn.CORN.init = "tini"
                elif "runit" in init_cmdline:
                    hub.corn.CORN.init = "runit"
                elif "/sbin/my_init" in init_cmdline:
                    # Phusion Base docker container use runit for srv mgmt, but
                    # my_init as pid1
                    hub.corn.CORN.init = "runit"
                else:
                    log.debug(
                        "Could not determine init system from command line: (%s)",
                        " ".join(init_cmdline),
                    )
            else:
                # Emtpy init_cmdline
                log.warning("Unable to fetch data from /proc/1/cmdline")
