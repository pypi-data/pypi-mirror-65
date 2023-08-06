from . import resources
from .custom_server import custom_server
from importlib_metadata import version

__all__ = ["resources", "custom_server"]

__version__ = version("willing_zg")
