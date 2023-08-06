from time import sleep, time
from threading import Thread

import numpy as np

from PIL import Image, ImageChops
from loguru import logger

from .textctrl import TextCtrl
from .imagectrl import ImageCtrl

from .previewmanager import PreviewManager, PreviewState, PreviewParam
        
class TinyMon(Thread):
    __textctrl = {}
    __imagectrl = {}
    
    def __init__(self, baseimagepath=None, fbdev=None, previewdev=None, brightness=15, sleep_time=0.02, **kwargs):
        Thread.__init__(self)
        self.__baseimage_dfl = ImageCtrl(path=baseimagepath)
        self.__backgndimg = ImageCtrl()

        logger.info({
            'name'          : 'TinyMon'
            ,'baseimagepath' : baseimagepath
            ,'fbdev'          : fbdev
            ,'previewdev'     : previewdev
            ,'brightness'     : brightness   
            ,'sleep_time'     : sleep_time
            ,'kwargs'         : kwargs
        })
        self.__preview = None
        if previewdev:
            self.__preview = PreviewManager(previewdev, **kwargs)
            self._previewparam = PreviewParam(sts=PreviewState.NONE, line=100, deltapixel=10)
            
            if 'previewline' in kwargs:
                self._previewparam.line = kwargs['previewline']
            if 'previewdeltapixel' in kwargs:
                self._previewparam.deltapixel = kwargs['previewdeltapixel']

        self.__fbdev = fbdev

        self.gray_level = min(15, max(0, brightness))

        self.sleep_time = sleep_time
        self.elpsd_time = 0
        self.fps = 0

    def previewproc(self, param, im, size):
        w, h = size
        if param.targetline > param.currentline:
            param.currentline += param.deltapixel
            if param.currentline > param.line:
                param.currentline = param.line
        elif param.targetline < param.currentline:
            param.currentline -= param.deltapixel
            if param.currentline < 0:
                param.currentline = 0
        else:
            param.sts = PreviewState.NONE
        
        if param.sts != PreviewState.NONE:
            im = im.crop((param.line-param.currentline, 0, w, h))
        if param.currentline > 0:
            self.__backgndimg.im.paste(im, (0,0,param.currentline,h))

    def hidepreview(self):
        logger.debug('hide preview')
        self._previewparam.targetline = 0
        self._previewparam.sts = PreviewState.TOHIDE

    def showpreview(self):
        logger.debug('show preview')
        self._previewparam.targetline = self._previewparam.line
        self._previewparam.sts = PreviewState.TOSHOW
        
    def __makefb(self):
        self.__backgndimg.clear(self.__baseimage_dfl.im)

        if self.__preview:
            size, frame = self.__preview.read()
            im = Image.fromarray(frame, 'L')
            self.previewproc(self._previewparam, im, size)

        for im in self.__imagectrl.values():
            x, y = im.pos
            self.__backgndimg.paste(im, (x + self._previewparam.currentline ,y ))        

        for im in self.__textctrl.values():
            im.draw(self.__backgndimg.im, offset=(self._previewparam.currentline ,0 ))
                    
        self.__fbdev.loadframe(np.asarray(self.__backgndimg.im, dtype=np.uint8))
    
    def __show(self, gray_level=15):
        self.__makefb()
        self.__fbdev.show(gray_level)

    def addctrl(self, id, ctrl):
        if isinstance(ctrl, TextCtrl):
            self.__textctrl[id]=ctrl
        elif isinstance(ctrl, ImageCtrl):
            self.__imagectrl[id]=ctrl
        else:
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
            