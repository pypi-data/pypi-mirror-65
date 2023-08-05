import aiofiles
import glob
import logging
import os

log = logging.getLogger(__name__)


async def load_disks(hub):
    """
    Return list of disk devices and work out if they are SSD or HDD.
    """
    SSDs = []
    disks = []
    for entry in glob.glob("/sys/block/*/queue/rotational"):
        if os.path.exists(entry):
            async with aiofiles.open(entry, "r") as entry_fp:
                device = entry.split("/")[3]
                flag = await entry_fp.read(1)
                if flag == "0":
                    SSDs.append(device)
                    log.debug(f"Device {device} reports itself as an SSD")
                elif flag == "1":
                    disks.append(device)
                    log.debug(f"Device {device} reports itself as an HDD")
                else:
                    log.debug(
                        f"Unable to identify device {device} as an SSD or HDD. It does not report 0 or 1"
                    )
    if SSDs:
        hub.corn.CORN.SSDs = sorted(SSDs)
    if disks:
        hub.corn.CORN.disks = sorted(disks)
