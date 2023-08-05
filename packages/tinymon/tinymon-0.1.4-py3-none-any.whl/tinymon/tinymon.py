from time import sleep, time
from threading import Thread

import numpy as np

from PIL import Image
from loguru import logger

from .textctrl import TextCtrl
from .imagectrl import ImageCtrl
from .preview import Preview
        
class TinyMon(Thread):
    __textctrl = {}
    __imagectrl = {}
    
    def __init__(self, baseimagepath=None, fbdev=None, previewdev=None, brightness=15, sleep_time=0.01):
        Thread.__init__(self)
        self.__baseimage_dfl = ImageCtrl(path=baseimagepath)
        self.__baseimage = ImageCtrl()
        self.__previewdev = previewdev
        if self.__previewdev != None:
            self.__preview = Preview(self.__previewdev)
        self.__fbdev = fbdev
        if brightness > 15:
            self.gray_level = 15
        elif brightness < 0:
            self.gray_level = 0
        else:
            self.gray_level = brightness

        self.sleep_time = sleep_time
        self.elpsd_time = 0
        self.fps = 0
        
    def __makefb(self):
        self.__baseimage.clear(self.__baseimage_dfl.im)
        for im in self.__imagectrl.values():
            self.__baseimage.paste(im, im.pos)
            
        if self.__previewdev:
            size, frame = self.__preview.read()
            w, h = size
            try:
                if frame.any():
                    im = Image.fromarray(frame, 'L')
                    self.__baseimage.im.paste(im, (0,0,w,h))
            except AttributeError:
                self.__baseimage.im.paste(self.__preview.img, (0,0,w,h))

        for im in self.__textctrl.values():
            im.draw(self.__baseimage.im)
                    
        self.__fbdev.loadframe(np.asarray(self.__baseimage.im, dtype=np.uint8))
    
    def __show(self, gray_level=15):
        self.__makefb()
        self.__fbdev.show(gray_level)
        
    def addctrl(self, id, ctrl):
        if isinstance(ctrl, TextCtrl):
            self.__textctrl[id]=ctrl
        elif isinstance(ctrl, ImageCtrl):
            self.__imagectrl[id]=ctrl
        else:
            #need exception
            logger.error(f"doesn't allowed ctrl {ctrl}")
            raise TypeError(f"doesn't allowed ctrl {ctrl}")

    def delImageCtrl(self, id):
        try:
            del(self.__imagectrl[id])
        except KeyError:
            logger.error(f'Cannot delete {id}, not founded.')
    def delTextCtrl(self, id):
        try:
            del(self.__textctrl[id])
        except KeyError:
            logger.error(f'Cannot delete {id}, not founded.')
        

    def run(self):
        while True:
            start = time()
            self.__show(self.gray_level)
            sleep(self.sleep_time)
            self.elpsd_time = time()-start
            self.fps = 1/self.elpsd_time
            