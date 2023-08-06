from zipfile import ZipFile
import os
import numpy as np

def renameh(dir):
    '''
    This funcion work of VNIR sensor file and does the renaming to .zip for you. works a direcoory level
    '''
    zero=os.path.join(dir,'0_0_0.rawx')
    os.remove(zero)
    ones=os.path.join(dir,'1_0_0.rawx')
    os.remove(ones)
    for filename in os.listdir(dir):
        if filename.endswith('.rawx'):
            src =os.path.join(dir,filename)
            dst =os.path.join(dir,filename[:-5]+".zip")
            os.rename(src, dst) 
        else:
            continue     

def unziph(dir):
    '''
    his funcion works at sensor directory level and unzips the file while removing garabage xml file
    '''
    for filename in os.listdir(dir):
        if filename.endswith('.zip'):
            path=os.path.join(dir,filename)
            with ZipFile(path,'r') as zip: 
                zip.printdir() 
                zip.extractall(dir) 
            dstimg =filename[:-4]+'.raw'
            srcimg = "image.raw"
            src=os.path.join(dir,srcimg)
            dst=os.path.join(dir,dstimg)         
            os.rename(src, dst)
            zippath=os.path.join(dir,filename)
            os.remove(zippath)
        else:
            waste=os.path.join(dir,'info.xml')
            os.remove(waste)
            continue

def raw2nph(direc):
    '''
    Parameter::
    --------
    last child direcoy directory a which files reside
    Output::
    -------
    npy file
    This converts to numpy format and works at directory level
    '''
    for filename in os.listdir(direc):
        if filename.endswith(".raw"):
            src=os.path.join(direc,filename)
            rimg=np.fromfile(src,dtype="uint16",sep="")
            img=rimg.reshape(455,400)
            dst=os.path.join(direc,filename[:-4]+".npy")
            np.save(dst,img)     
            os.remove(src)
        else:
            continue
        
def pick_hyperdir(rootdir):
    '''
    parameter::
    ---------
    str: path of top level file
    output::
    ----------
    list of end level direcory of hyperspecral
    Description:
    -----------
    This custom funcion for IARI file system and will give a list of direcory of speceific sensor from he op level file. The output
    of his funcion can be used as input o oher funcion if you want to apply command a direcory level
    '''
    sensordir=r"VNIR_SV"
    dir_list=[]
    subdir_indiv=os.listdir(rootdir)
    for i in subdir_indiv:
        x=os.path.join(rootdir,i,sensordir)
        dir_list.append(x)
    return dir_list