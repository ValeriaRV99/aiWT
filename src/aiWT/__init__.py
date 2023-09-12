__author__ = "Pavanello Research Group"
__contact__ = ""
__license__ = "MIT"
__version__ = "1.0.0"
__date__ = "2023-09-11"

from .aiWT import *

try:
    from importlib.metadata import version # python >= 3.8
except Exception :
    try:
        from importlib_metadata import version
    except Exception :
        pass

try:
    __version__ = version("aiWT")
except Exception :
    pass