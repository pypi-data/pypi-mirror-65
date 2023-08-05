import ipaddress


async def load_gateway(hub):
    """
    Populates corn which describe whether a server has a default gateway
    configured or not.

    List of corn:

        ip4_gw: True # ip/True/False if default ipv4 gateway
        ip6_gw: True # ip/True/False if default ipv6 gateway
        ip_gw: True # True if either of the above is True, else False
    """
    ip4_gw = []
    ip6_gw = []

    for interface in hub.exec.wmi.WMI.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        for gateway in interface.DefaultIPGateway:
            addr = ipaddress.ip_address(gateway)
            if isinstance(addr, ipaddress.IPv4Address):
                ip4_gw.append(str(addr))
            elif isinstance(addr, ipaddress.IPv6Address):
                ip6_gw.append(str(addr))

    hub.corn.CORN.ip4_gw = ip4_gw or False
    hub.corn.CORN.ip6_gw = ip6_gw or False
    hub.corn.CORN.ip_gw = bool(ip4_gw or ip6_gw) or False
