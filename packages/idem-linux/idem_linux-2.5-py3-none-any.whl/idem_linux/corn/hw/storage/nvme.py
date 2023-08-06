# -*- coding: utf-8 -*-
"""
Grains for NVMe Qualified Names (NQN).
"""
import aiofiles
import errno
import logging

log = logging.getLogger(__name__)


async def load_nvme_nqn(hub):
    """
    Return NVMe NQN from a Linux host.
    """
    nvme_nqn = []

    initiator = "/etc/nvme/hostnqn"
    try:
        async with aiofiles.open(initiator, "r") as _nvme:
            async for line in _nvme:
                line = line.strip()
                if line.startswith("nqn."):
                    nvme_nqn.append(line)
    except IOError as ex:
        if ex.errno != errno.ENOENT:
            log.debug(f"Error while accessing '{initiator}': {ex}")

    if nvme_nqn:
        hub.corn.CORN.nvme_nqn = nvme_nqn
