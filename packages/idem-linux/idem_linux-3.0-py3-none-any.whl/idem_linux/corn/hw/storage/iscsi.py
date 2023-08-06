import aiofiles
import errno
import logging
import os

log = logging.getLogger(__name__)


async def load_iqn(hub):
    """
    Return iSCSI IQN from a Linux host.
    """
    initiator = "/etc/iscsi/initiatorname.iscsi"

    if os.path.exists(initiator):
        iscsi_iqn = []
        try:
            async with aiofiles.open(initiator, "r") as _iscsi:
                async for line in _iscsi:
                    line = line.strip()
                    if line.startswith("InitiatorName="):
                        iscsi_iqn.append(line.split("=", 1)[1])
        except IOError as ex:
            if ex.errno != errno.ENOENT:
                log.debug(f"Error while accessing '{initiator}': {ex}")

        if iscsi_iqn:
            hub.corn.CORN.iscsi_iqn = iscsi_iqn
