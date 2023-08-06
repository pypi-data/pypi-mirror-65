import numpy as np
import os
from .raw import read_raw
from zipfile import ZipFile
from hyperpy.utility import read_hdr_file
from .visualize import imshow_gray
from .visualize import imshow_hist
from hyperpy.utility import imshow_fcc

__version__ = "unknown"

try:
    from ._version import __version__
except ImportError:
    pass