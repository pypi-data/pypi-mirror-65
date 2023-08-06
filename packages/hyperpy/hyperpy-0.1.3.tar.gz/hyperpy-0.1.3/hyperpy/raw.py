import numpy as np

def rawread(path,height,width):
    '''this fucion read raw files . Made by sunny arya .It takes three arguments  path, height and width.
    Parameters
    ----------
    path : str
    height: int
    width: int
    output:
    --------
    np.array: image matrix from raw binary image
    '''
    img1 = np.fromfile(path, dtype='uint16', sep="")
    img2 = np.reshape(img1, (height, width))
    return img2
