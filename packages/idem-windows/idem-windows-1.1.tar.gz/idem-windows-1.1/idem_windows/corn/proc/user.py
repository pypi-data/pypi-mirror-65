async def load_user(hub):
    hub.corn.CORN.username = hub.exec.user.current()
    # The relative ID is always the last number in the SID it is a unique identifier for a user or group.
    hub.corn.CORN.uid = int(
        hub.exec.user.sid_from_name(hub.corn.CORN.username).split("-")[-1]
    )

    groups = hub.exec.user.groups(hub.corn.CORN.username)
    admin = "Administrators"
    hub.corn.CORN.groupname = admin if admin in groups else groups.pop()
    hub.corn.CORN.gid = int(
        hub.exec.user.sid_from_name(hub.corn.CORN.groupname).split("-")[-1]
    )


async def load_console_user(hub):
    systeminfo = await hub.exec.wmi.get("Win32_ComputerSystem", 0)
    hub.corn.CORN.console_username = systeminfo.UserName
    hub.corn.CORN.console_user = int(
        hub.exec.user.sid_from_name(hub.corn.CORN.console_username).split("-")[-1]
    )
