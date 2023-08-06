from typing import List

import aiofiles
import distro
import logging
import os
import re

log = logging.getLogger(__name__)

_REPLACE_LINUX_RE = re.compile(r"\W(?:gnu/)?linux", re.IGNORECASE)

_OS_NAME_MAP = {
    "redhatente": "RedHat",
    "gentoobase": "Gentoo",
    "archarm": "Arch ARM",
    "arch": "Arch",
    "debian": "Debian",
    "raspbian": "Raspbian",
    "fedoraremi": "Fedora",
    "chapeau": "Chapeau",
    "korora": "Korora",
    "amazonami": "Amazon",
    "alt": "ALT",
    "enterprise": "OEL",
    "oracleserv": "OEL",
    "cloudserve": "CloudLinux",
    "cloudlinux": "CloudLinux",
    "pidora": "Fedora",
    "scientific": "ScientificLinux",
    "synology": "Synology",
    "nilrt": "NILinuxRT",
    "poky": "Poky",
    "manjaro": "Manjaro",
    "manjarolin": "Manjaro",
    "univention": "Univention",
    "antergos": "Antergos",
    "sles": "SUSE",
    "void": "Void",
    "slesexpand": "RES",
    "linuxmint": "Mint",
    "neon": "KDE neon",
}

_OS_FAMILY_MAP = {
    "Ubuntu": "Debian",
    "Fedora": "RedHat",
    "Chapeau": "RedHat",
    "Korora": "RedHat",
    "FedBerry": "RedHat",
    "CentOS": "RedHat",
    "GoOSe": "RedHat",
    "Scientific": "RedHat",
    "Amazon": "RedHat",
    "CloudLinux": "RedHat",
    "OVS": "RedHat",
    "OEL": "RedHat",
    "XCP": "RedHat",
    "XCP-ng": "RedHat",
    "XenServer": "RedHat",
    "RES": "RedHat",
    "Sangoma": "RedHat",
    "Mandrake": "Mandriva",
    "ESXi": "VMware",
    "Mint": "Debian",
    "VMwareESX": "VMware",
    "Bluewhite64": "Bluewhite",
    "Slamd64": "Slackware",
    "SLES": "Suse",
    "SUSE Enterprise Server": "Suse",
    "SUSE  Enterprise Server": "Suse",
    "SLED": "Suse",
    "openSUSE": "Suse",
    "SUSE": "Suse",
    "openSUSE Leap": "Suse",
    "openSUSE Tumbleweed": "Suse",
    "SLES_SAP": "Suse",
    "Solaris": "Solaris",
    "SmartOS": "Solaris",
    "OmniOS": "Solaris",
    "OpenIndiana Development": "Solaris",
    "OpenIndiana": "Solaris",
    "OpenSolaris Development": "Solaris",
    "OpenSolaris": "Solaris",
    "Oracle Solaris": "Solaris",
    "Arch ARM": "Arch",
    "Manjaro": "Arch",
    "Antergos": "Arch",
    "ALT": "RedHat",
    "Trisquel": "Debian",
    "GCEL": "Debian",
    "Linaro": "Debian",
    "elementary OS": "Debian",
    "elementary": "Debian",
    "Univention": "Debian",
    "ScientificLinux": "RedHat",
    "Raspbian": "Debian",
    "Devuan": "Debian",
    "antiX": "Debian",
    "Kali": "Debian",
    "neon": "Debian",
    "Cumulus": "Debian",
    "Deepin": "Debian",
    "NILinuxRT": "NILinuxRT",
    "KDE neon": "Debian",
    "Void": "Void",
    "IDMS": "Debian",
    "Funtoo": "Gentoo",
    "AIX": "AIX",
    "TurnKey": "Debian",
}


async def _get_synology_osrelease(osrelease: str) -> str:
    # Get os from synology
    version = "/etc.defaults/VERSION"
    if os.path.isfile(version) and os.path.isfile("/etc.defaults/synoinfo.conf"):
        log.debug("Parsing Synology distrib info from /etc/.defaults/VERSION")
        async with aiofiles.open(version, "r") as fp_:
            synoinfo = {}
            async for line in fp_:
                try:
                    key, val = line.rstrip("\n").split("=")
                except ValueError:
                    continue
                if key in ("majorversion", "minorversion", "buildnumber"):
                    synoinfo[key] = val.strip('"')
            if len(synoinfo) != 3:
                log.warning(
                    "Unable to determine Synology version info. "
                    "Please report this, as it is likely a bug."
                )
            else:
                return f'{synoinfo["majorversion"]}.{synoinfo["minorversion"]}-{synoinfo["buildnumber"]}'


async def _get_osrelease_info(osrelease: str) -> List[str]:
    osrelease_info = osrelease.split(".")
    for idx, value in enumerate(osrelease_info):
        if not value.isdigit():
            continue
        osrelease_info[idx] = int(value)
    return osrelease_info


async def _get_os(osfullname: str) -> str:
    distroname = _REPLACE_LINUX_RE.sub("", osfullname).strip()

    # return the first ten characters with no spaces, lowercased
    shortname = distroname.replace(" ", "").lower()[:10]

    # this maps the long names from the /etc/DISTRO-release files to the
    # traditional short names that Salt has used.
    return _OS_NAME_MAP.get(shortname, distroname)


async def load_manufacturer(hub):
    # TODO There has got to be a way to programmatically determine this
    # For example, ubuntu is manufactuerd by Canonical, etc...
    hub.corn.CORN.osmanufactuer = "unknown"


async def load_linux_distribution(hub):
    info = distro.LinuxDistribution()
    hub.corn.CORN.osbuild = info.build_number()
    hub.corn.CORN.oscodename = info.codename().strip("\"'")

    hub.corn.CORN.osfullname = info.name().strip("\"'")
    hub.corn.CORN.osrelease = info.version().strip("\"'")

    if not (hub.corn.CORN.get("osfullname") or hub.corn.CORN.get("osrelease")):
        hub.corn.CORN.osrelease = await _get_synology_osrelease(hub.corn.CORN.osrelease)
        if hub.corn.CORN.get("osrelease"):
            hub.corn.CORN.osfullname = "Synology"
        else:
            hub.corn.CORN.osrelease = ""
            hub.corn.CORN.osfullname = ""

    hub.corn.CORN.os = await _get_os(hub.corn.CORN.osfullname)

    hub.corn.CORN.os_family = _OS_FAMILY_MAP.get(hub.corn.CORN.os, hub.corn.CORN.os)
    if hub.corn.CORN.os_family == "NILinuxRT":
        # This will likely have been defined elsewhere, dereference and redefine
        del hub.corn.CORN.ps
        hub.corn.CORN.ps = "ps -o user,pid,ppid,tty,time,comm"
    hub.corn.CORN.osrelease_info = await _get_osrelease_info(hub.corn.CORN.osrelease)

    major_version = distro.LinuxDistribution().major_version().strip("\"'")
    hub.corn.CORN.osmajorrelease = (
        int(major_version) if major_version else hub.corn.CORN.osrelease_info[0]
    )

    # load osfinger
    os_name = hub.corn.CORN[
        "os"
        if hub.corn.CORN.os
        in ("Debian", "FreeBSD", "OpenBSD", "NetBSD", "Mac", "Raspbian")
        else "osfullname"
    ]
    finger = (
        hub.corn.CORN.osrelease
        if os_name in ("Ubuntu",)
        else hub.corn.CORN.osrelease_info[0]
    )
    if os_name and finger:
        hub.corn.CORN.osfinger = f"{os_name}-{finger}"
