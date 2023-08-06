import logging
import re

log = logging.getLogger(__name__)


async def load_motherboard(hub):
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa394072(v=vs.85).aspx
    try:
        motherboardinfo = await hub.exec.wmi.get("Win32_BaseBoard", 0)
        hub.corn.CORN.motherboard.productname = motherboardinfo.Product
        hub.corn.CORN.motherboard.serialnumber = motherboardinfo.SerialNumber
    except IndexError:
        log.debug("Motherboard info not available on this system")


async def load_system_info(hub):
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa394102%28v=vs.85%29.aspx
    systeminfo = await hub.exec.wmi.get("Win32_ComputerSystem", 0)
    hub.corn.CORN.manufacturer = await hub.corn.init.clean_value(
        "manufacturer", systeminfo.Manufacturer
    )
    hub.corn.CORN.productname = await hub.corn.init.clean_value(
        "productname", systeminfo.Model
    )

    hub.corn.CORN.computer_name = await hub.corn.init.clean_value(
        "computer_name", systeminfo.Name
    )
