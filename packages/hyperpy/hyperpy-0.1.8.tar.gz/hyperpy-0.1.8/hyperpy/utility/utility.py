import spectral.io.envi as envi
from spectral import *

def read_hdr_file(path):
    '''
    reads the hdr hyperpsectral image file 
    Parameter:
    -----------------
    str: path of hdr file
    return:
    ---------------
    numpy array : hyperspectral; cube
    '''
    import spectral.io.envi as envi
    img=envi.open(path)
    return img


def imshow_fcc(img,band1,band2,band3):

    imshow(img,(band1,band2,band3))
    '''

    '''