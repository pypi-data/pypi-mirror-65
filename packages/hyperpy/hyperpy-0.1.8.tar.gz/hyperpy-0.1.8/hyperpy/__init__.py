from .raw import read_raw
from hyperpy.utility import read_hdr_file
from hyperpy.utility import imshow_fcc

from .visualize import imshow_gray
from .visualize import imshow_hist
import matplotlib.pyplot as plt

__version__ = "unknown"

try:
    from ._version import __version__
except ImportError:
    pass