import wmi
from typing import Any, Dict, List


async def _get_interfaces(
    wmi_network_adapter_config: List[wmi._wmi_property],
) -> Dict[str, Any]:
    interfaces = {}
    for interface in wmi_network_adapter_config:
        interfaces[interface.Description] = {}
        if interface.MACAddress:
            interfaces[interface.Description]["hwaddr"] = interface.MACAddress
        if interface.IPEnabled:
            interfaces[interface.Description]["up"] = True
            for ip in interface.IPAddress:
                if "." in ip:
                    if "inet" not in interfaces[interface.Description]:
                        interfaces[interface.Description]["inet"] = []
                    item = {"address": ip, "label": interface.Description}
                    if interface.DefaultIPGateway:
                        broadcast = next(
                            (i for i in interface.DefaultIPGateway if "." in i), ""
                        )
                        if broadcast:
                            item["broadcast"] = broadcast
                    if interface.IPSubnet:
                        netmask = next((i for i in interface.IPSubnet if "." in i), "")
                        if netmask:
                            item["netmask"] = netmask
                    interfaces[interface.Description]["inet"].append(item)
                if ":" in ip:
                    if "inet6" not in interfaces[interface.Description]:
                        interfaces[interface.Description]["inet6"] = []
                    item = {"address": ip}
                    if interface.DefaultIPGateway:
                        broadcast = next(
                            (i for i in interface.DefaultIPGateway if ":" in i), ""
                        )
                        if broadcast:
                            item["broadcast"] = broadcast
                    if interface.IPSubnet:
                        netmask = next((i for i in interface.IPSubnet if ":" in i), "")
                        if netmask:
                            item["netmask"] = netmask
                    interfaces[interface.Description]["inet6"].append(item)
        else:
            interfaces[interface.Description]["up"] = False
    return interfaces


async def load_interfaces(hub):
    """
    Obtain interface information for Windows systems
    Provides:
      ip_interfaces
    """
    # TODO this doesn't show loopback devices

    ipv4 = []
    ipv6 = []
    interfaces = await _get_interfaces(
        await hub.exec.wmi.get("Win32_NetworkAdapterConfiguration", IPEnabled=1)
    )

    for interface, device in interfaces.items():
        hw_addr = device.get("hwaddr")
        if hw_addr:
            hub.corn.CORN.hwaddr_interfaces[interface] = hw_addr
        inet4: List[str] = [ip.get("address") for ip in device.get("inet", [])]
        ipv4.extend(inet4)
        if inet4:
            hub.corn.CORN.ip4_interfaces[interface] = inet4
        inet6: List[str] = [ip.get("address") for ip in device.get("inet6", [])]
        ipv6.extend(inet6)
        if inet6:
            hub.corn.CORN.ip6_interfaces[interface] = inet6
        hub.corn.CORN.ip_interfaces[interface] = inet4 + inet6

    hub.corn.CORN.ipv4 = ipv4
    hub.corn.CORN.ipv6 = ipv6
