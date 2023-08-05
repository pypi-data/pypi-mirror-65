"""
TODO These grains are collected in salt, but some work regarding minion and master confs
needs to be done before they can be useful here
"""
import logging
import os

log = logging.getLogger(__name__)


async def load_salt_path(hub):
    try:
        import salt

        hub.corn.CORN.saltpath = os.path.dirname(os.path.abspath(salt.__file__))
    except (ImportError, ModuleNotFoundError):
        hub.corn.CORN.saltpath = "unknown"


async def load_salt_version(hub):
    try:
        from salt.version import __version__, __version_info__

        hub.corn.CORN.saltversion = __version__
        hub.corn.CORN.saltversioninfo = __version_info__
    except (ImportError, ModuleNotFoundError):
        hub.corn.CORN.saltversion = "unknown"
        hub.corn.CORN.saltversioninfo = "unknown"
