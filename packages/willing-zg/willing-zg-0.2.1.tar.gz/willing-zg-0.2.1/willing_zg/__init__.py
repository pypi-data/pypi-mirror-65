from . import resources
from .custom_server import custom_server
from .deployment import deployment
from importlib_metadata import version

__all__ = ["resources", "custom_server", "deployment"]

__version__ = version("willing_zg")
