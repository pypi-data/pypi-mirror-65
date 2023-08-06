import os


async def load_shell(hub):
    hub.corn.CORN.shell = os.environ.get("COMSPEC", r"C:\Windows\system32\cmd.exe")
