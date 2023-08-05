import sys


async def load_kernel(hub):
    """
    Verify that POP linux is running on windows
    """
    if sys.platform.startswith("win"):
        hub.corn.CORN.kernel = "Windows"
    else:
        raise OSError("POP-Windows is only intended for Windows systems")

    # Hard coded corns for windows systems
    hub.corn.CORN.init = "Windows"
    hub.corn.CORN.like = ["Windows"]
    hub.corn.CORN.os = "Windows"
    hub.corn.CORN.os_family = "Windows"
    hub.corn.CORN.ps = "tasklist.exe"
