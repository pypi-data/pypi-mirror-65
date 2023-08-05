import win32api


async def load_memdata(hub):
    """
    Return the memory information for Windows systems
    """
    # get the Total Physical memory as reported by msinfo32
    tot_bytes = win32api.GlobalMemoryStatusEx()["TotalPhys"]
    # return memory info in gigabytes
    hub.corn.CORN.mem_total = int(tot_bytes / (1024 ** 2))
