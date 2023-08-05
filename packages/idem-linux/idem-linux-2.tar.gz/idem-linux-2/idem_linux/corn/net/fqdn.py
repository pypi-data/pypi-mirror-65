import logging
import socket
from typing import List

log = logging.getLogger(__name__)

# Possible value for h_errno defined in netdb.h
HOST_NOT_FOUND = 1
NO_DATA = 4


async def _get_fqdns(fqdn: str, protocol: int) -> List[str]:
    socket.setdefaulttimeout(1)
    try:
        result = socket.getaddrinfo(fqdn, None, protocol)
        return sorted({item[4][0] for item in result})
    except socket.gaierror as e:
        log.debug(e)
    return []


async def load_socket_info(hub):
    hub.corn.CORN.localhost = socket.gethostname()

    # try socket.getaddrinfo to get fqdn
    try:
        addrinfo = socket.getaddrinfo(
            hub.corn.CORN.localhost,
            0,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM,
            socket.SOL_TCP,
            socket.AI_CANONNAME,
        )
        for info in addrinfo:
            # info struct [family, socktype, proto, canonname, sockaddr]
            if len(info) >= 4:
                hub.corn.CORN.fqdn = info[3]
    except socket.gaierror:
        pass

    if "fqdn" not in hub.corn.CORN:
        hub.corn.CORN.fqdn = socket.getfqdn() or "localhost"

    log.debug("loading fqdns based grains")
    hub.corn.CORN.host, hub.corn.CORN.domain = hub.corn.CORN.fqdn.partition(".")[::2]
    hub.corn.CORN.fqdn_ip4 = await _get_fqdns(hub.corn.CORN.fqdn, socket.AF_INET)
    hub.corn.CORN.fqdn_ip6 = await _get_fqdns(hub.corn.CORN.fqdn, socket.AF_INET6)
    hub.corn.CORN.fqdns = hub.corn.CORN.fqdn_ip4 + hub.corn.CORN.fqdn_ip6
