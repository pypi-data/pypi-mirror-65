import aiofiles
import logging
import os
import yaml

log = logging.getLogger(__name__)


async def load_config(hub):
    """
    Return the corn set in the corn file
    """
    # TODO this comes from salt.salt.corn.extra.py, how do we want to locate static corn configs in hub.OPT?
    if "conf_file" not in hub.OPT:
        return

    if os.path.isdir(hub.OPT.conf_file):
        gfn = os.path.join(hub.OPT.conf_file, "corn")
    else:
        gfn = os.path.join(os.path.dirname(hub.OPT.conf_file), "corn")

    if os.path.isfile(gfn):
        log.debug("Loading static corn from %s", gfn)
        async with aiofiles.open(gfn, "rb") as fp_:
            try:
                # TODO? Load the yaml file with hub.rend
                hub.corn.CORN.update(yaml.safe_load(fp_))
            except Exception:  # pylint: disable=broad-except
                log.warning("Bad syntax in corn file! Skipping.")
