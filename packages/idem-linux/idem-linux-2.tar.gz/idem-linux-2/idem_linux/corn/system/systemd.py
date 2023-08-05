import aiofiles
import logging
import os
import shutil

log = logging.getLogger(__name__)


async def load_systemd(hub):
    if shutil.which("systemctl") and shutil.which("localectl"):
        log.debug("Adding systemd corn")
        systemd_info = (await hub.exec.cmd.run("systemctl --version"))[
            "stdout"
        ].splitlines()
        hub.corn.CORN.systemd.version = systemd_info[0].split()[1]

        features = {}
        for feature in systemd_info[1].split(" "):
            if feature.startswith("+"):
                features[feature[1:].lower()] = True
            elif feature.startswith("-"):
                features[feature[1:].lower()] = False
            elif "=" in feature:
                k, v = feature.split("=", maxsplit=1)
                features[k.lower()] = v
        hub.corn.CORN.systemd.features = {
            k: features[k] for k in sorted(features.keys())
        }


async def load_init(hub):
    # Add init grain
    hub.corn.CORN.init = "unknown"
    log.debug("Adding init grain")
    try:
        os.stat("/run/systemd/system")
        hub.corn.CORN.init = "systemd"
    except (OSError, IOError):
        try:
            async with aiofiles.open("/proc/1/cmdline") as fhr:
                init_cmdline = (await fhr.read()).replace("\x00", " ").split()
        except (IOError, OSError):
            pass
        else:
            try:
                init_bin = shutil.which(init_cmdline[0])
            except IndexError:
                # Emtpy init_cmdline
                init_bin = None
                log.warning("Unable to fetch data from /proc/1/cmdline")
            if init_bin is not None and init_bin.endswith("bin/init"):
                supported_inits = (b"upstart", b"sysvinit", b"systemd")
                edge_len = max(len(x) for x in supported_inits) - 1
                buf_size = hub.opts.get("file_buffer_size", 262144)
                try:
                    async with aiofiles.open(init_bin, "rb") as fp_:
                        edge = b""
                        buf = (await fp_.read(buf_size)).lower()
                        while buf:
                            buf = edge + buf
                            for item in supported_inits:
                                if item in buf:
                                    item = item.decode("utf-8")
                                    hub.corn.CORN.init = item
                                    buf = b""
                                    break
                            edge = buf[-edge_len:]
                            buf = fp_.read(buf_size).lower()
                except (IOError, OSError) as exc:
                    log.error("Unable to read from init_bin (%s): %s", init_bin, exc)
            elif shutil.which("supervisord") in init_cmdline:
                hub.corn.CORN.init = "supervisord"
            elif shutil.which("dumb-init") in init_cmdline:
                # https://github.com/Yelp/dumb-init
                hub.corn.CORN.init = "dumb-init"
            elif shutil.which("tini") in init_cmdline:
                # https://github.com/krallin/tini
                hub.corn.CORN.init = "tini"
            elif init_cmdline == ["runit"]:
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
