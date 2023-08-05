# Provides:
#    osversion
#    osmanufacturer
#    osfullname
import logging
import platform

log = logging.getLogger(__name__)


async def load_osinfo(hub):
    # https://msdn.microsoft.com/en-us/library/aa394239(v=vs.85).aspx
    osinfo = await hub.exec.wmi.get("Win32_OperatingSystem", 0)

    hub.corn.CORN.osmanufacturer = await hub.corn.init.clean_value(
        "osmanufacturer", osinfo.Manufacturer
    )
    hub.corn.CORN.osfullname = await hub.corn.init.clean_value(
        "osfullname", osinfo.Caption
    )
    hub.corn.CORN.kernelrelease = await hub.corn.init.clean_value(
        "kernelrelease", osinfo.Version
    )

    hub.corn.CORN.osrelease = await hub.corn.init.clean_value(
        "osversion", osinfo.Version
    )

    hub.corn.CORN.osrelease_info = hub.corn.CORN.osrelease.split(".")

    hub.corn.CORN.osservicepack = await hub.corn.init.clean_value(
        "osservicepack", osinfo.CSDVersion
    ) or platform.win32_ver()[2].replace("SP", "Service Pack ")

    hub.corn.CORN.osarch = await hub.corn.init.clean_value(
        "osarch", osinfo.OSArchitecture
    )


async def load_build(hub):
    major = int(
        hub.exec.reg.read_value(
            hive="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            vname="CurrentBuildNumber",
        ).get("vdata")
    )
    minor = int(
        hub.exec.reg.read_value(
            hive="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            vname="UBR",
        ).get("vdata")
    )

    hub.corn.CORN.osbuild = f"{major}.{minor}"


async def load_osmajorrelease(hub):
    hub.corn.CORN.osmajorrelease = int(
        hub.exec.reg.read_value(
            hive="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            vname="CurrentMajorVersionNumber",
        ).get("vdata")
    )


async def load_build_version(hub):
    hub.corn.CORN.osbuildversion = int(
        hub.exec.reg.read_value(
            hive="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            vname="ReleaseId",
        ).get("vdata")
    )


async def load_codename(hub):
    hub.corn.CORN.oscodename = hub.exec.reg.read_value(
        hive="HKEY_LOCAL_MACHINE",
        key="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
        vname="BuildBranch",
    ).get("vdata")


async def load_finger(hub):
    hub.corn.CORN.osfinger = platform.platform()
