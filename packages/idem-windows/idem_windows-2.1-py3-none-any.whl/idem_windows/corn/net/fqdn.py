import logging
import socket
from typing import List

log = logging.getLogger(__name__)


async def load_localhost(hub):
    hub.corn.CORN.localhost = socket.gethostname()


async def _get_fqdns(fqdn: str, protocol: int) -> List[str]:
    socket.setdefaulttimeout(1)
    try:
        result = socket.getaddrinfo(fqdn, None, protocol)
        return sorted({item[4][0] for item in result})
    except socket.gaierror as e:
        log.debug(e)
    return []


async def load_fqdn(hub):
    # try socket.getaddrinfo to get fqdn
    try:
        addrinfo = socket.getaddrinfo(
            socket.gethostname(),
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

    if not hub.corn.CORN.get("fqdn"):
        hub.corn.CORN.fqdn = socket.getfqdn() or "localhost"

    log.debug("loading host and domain")
    hub.corn.CORN.host, hub.corn.CORN.domain = hub.corn.CORN.fqdn.partition(".")[::2]
    log.debug("loading fqdns")
    hub.corn.CORN.fqdn_ip4 = await _get_fqdns(hub.corn.CORN.fqdn, socket.AF_INET)
    hub.corn.CORN.fqdn_ip6 = await _get_fqdns(hub.corn.CORN.fqdn, socket.AF_INET6)
    hub.corn.CORN.fqdns = hub.corn.CORN.fqdn_ip4 + hub.corn.CORN.fqdn_ip6
