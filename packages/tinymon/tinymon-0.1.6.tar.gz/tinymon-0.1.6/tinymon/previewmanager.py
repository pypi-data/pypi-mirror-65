import os, sys
from enum import Enum 
from loguru import logger

from pkg_resources import resource_filename

import numpy as np
from PIL import Image 

#sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from .preview_cv import PreviewCV
from .preview_udp import PreviewServer

class PreviewState(int, Enum):
    TOHIDE = -1
    NONE = 0
    TOSHOW = 1

class PreviewParam:
    def __init__(self, sts=PreviewState.NONE, line=100, deltapixel=10):
        self.sts = sts
        self.line = line
        self.deltapixel = deltapixel
        self.targetline = self.line
        self.currentline = self.line
    
class PreviewType(str, Enum):
    UDP = 'udp'
    CV = 'cv'

class PreviewManager:
    def __init__(self, previewdev='udp', pos=(0,0), size=(100,64), **kwargs):
        if previewdev == 'udp':
            devtype = PreviewType.UDP
        else:
            devtype = PreviewType.CV

        if not 'not_available_img' in kwargs:
            not_available_img = resource_filename(__name__, 'image/videonot.png') 
        
        logger.info(f'not_available_img : {not_available_img}')
        self.img = np.asarray(Image.open(not_available_img).resize(size, resample=Image.BICUBIC).convert('L'))
        
        if (devtype is PreviewType.UDP) and (not 'port' in kwargs):
            kwargs['port'] = 9521

        self.dev = {
            'udp'   : lambda : PreviewServer(port=kwargs['port'], pos=pos, size=size),
            'cv'  : lambda : PreviewCV(video=previewdev, pos=pos, size=size),            
        }.get(devtype, None)()

    def read(self):
        size, frame = self.dev.read()
        if not isinstance(frame, np.ndarray):
            frame = self.img 
        return (size, frame)

if __name__ == '__main__':
    #mgr = PreviewManager(previewdev=1)
    mgr = PreviewManager(previewdev='udp', port=9521)
    print(mgr)