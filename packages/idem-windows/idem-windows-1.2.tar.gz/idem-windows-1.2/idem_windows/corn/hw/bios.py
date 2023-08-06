import datetime


async def load_bios_info(hub):
    biosinfo = await hub.exec.wmi.get("Win32_BIOS", 0)

    # bios name had a bunch of whitespace appended to it in my testing
    # 'PhoenixBIOS 4.0 Release 6.0     '
    hub.corn.CORN.biosversion = await hub.corn.init.clean_value(
        "biosversion", biosinfo.Name.strip()
    )

    date = datetime.datetime.strptime(
        biosinfo.ReleaseDate.split(".")[0], "%Y%m%d%H%M%S"
    )
    hub.corn.CORN.biosreleasedate = f"{date.month}/{date.day}/{date.year}"
    hub.corn.CORN.serialnumber = await hub.corn.init.clean_value(
        "serialnumber", biosinfo.SerialNumber
    )
