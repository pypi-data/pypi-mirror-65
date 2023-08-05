# Add lsb corn on any distro with lsb-release. Note that this import
# can fail on systems with lsb-release installed if the system package
# does not install the python package for the python interpreter used by
# Salt (i.e. python2 or python3)
import aiofiles
import distro
import logging
import re
import os
from typing import Any, Dict

log = logging.getLogger(__name__)

# Matches any possible format:
#     DISTRIB_ID="Ubuntu"
#     DISTRIB_ID='Mageia'
#     DISTRIB_ID=Fedora
#     DISTRIB_RELEASE='10.10'
#     DISTRIB_CODENAME='squeeze'
#     DISTRIB_DESCRIPTION='Ubuntu 10.10'
_LSB_REGEX = re.compile(
    (
        "^(DISTRIB_(?:ID|RELEASE|CODENAME|DESCRIPTION))=(?:'|\")?"
        "([\\w\\s\\.\\-_]+)(?:'|\")?"
    )
)


async def _parse_lsb_release(hub) -> Dict[str, Any]:
    name = "/etc/lsb-release"
    grains = {}
    if os.path.exists(name):
        try:
            log.debug("Attempting to parse /etc/lsb-release")
            async with aiofiles.open(name) as ifile:
                async for line in ifile:
                    try:
                        key, value = _LSB_REGEX.match(line.rstrip("\n")).groups()[:2]
                    except AttributeError:
                        pass
                    else:
                        # Adds lsb_distrib_{id,release,codename,description}
                        grains[f"lsb_{key.lower()}"] = value.rstrip()
        except (IOError, OSError) as exc:
            log.debug("Failed to parse /etc/lsb-release: %s", exc)
    return grains


async def _import_lsb_release(hub) -> Dict[str, Any]:
    grains = {}
    try:
        log.debug("Getting lsb_release distro information")
        import lsb_release  # pylint: disable=import-error

        release = lsb_release.get_distro_information()
        for key, value in release.items():
            key = key.lower()
            distrib = "" if key.startswith("distrib_") else "distrib_"
            grains[f"lsb_{distrib}{key}"] = value
    # Catch a NameError to workaround possible breakage in lsb_release
    # See https://github.com/saltstack/salt/issues/37867
    except (ImportError, NameError):
        pass
    return grains


async def _parse_os_release(hub) -> Dict[str, Any]:
    """
    Parse os-release and return a parameter dictionary

    See http://www.freedesktop.org/software/systemd/man/os-release.html
    for specification of the file format.
    """
    grains = {}
    os_release_file = distro.LinuxDistribution().os_release_file
    if "lsb_distrib_id" not in hub.corn.CORN and os.path.exists(os_release_file):
        async with aiofiles.open(os_release_file) as ifile:
            regex = re.compile("^([\\w]+)=(?:['\"])?(.*?)(?:['\"])?$")
            async for line in ifile:
                match = regex.match(line.strip())
                if match:
                    # Shell special characters ("$", quotes, backslash,
                    # backtick) are escaped with backslashes
                    grains[match.group(1).lower()] = re.sub(
                        r'\\([$"\'\\`])', r"\1", match.group(2)
                    )
    return grains


async def load_lsb_release(hub):
    # The one that comes last is most authoritative
    hub.corn.CORN.update(await _parse_os_release(hub))
    hub.corn.CORN.update(await _parse_lsb_release(hub))
    hub.corn.CORN.update(await _import_lsb_release(hub))
