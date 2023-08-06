import platform


async def load_cpuarch(hub):
    hub.corn.CORN.cpuarch = platform.machine()


async def load_nodename(hub):
    hub.corn.CORN.nodename = platform.node()


async def load_kernel_version(hub):
    hub.corn.CORN.kernelversion = platform.version()
