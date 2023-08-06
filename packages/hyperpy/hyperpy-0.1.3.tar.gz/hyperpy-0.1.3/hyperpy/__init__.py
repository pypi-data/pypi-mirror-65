import numpy as np
import os
from .raw import rawread
from zipfile import ZipFile

__version__ = "unknown"

try:
    from ._version import __version__
except ImportError:
    pass