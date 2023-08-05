from pkg_resources import resource_filename
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, timeout
from threading import Thread
import numpy as np
from PIL import Image 
from loguru import logger

PREVIEW_PORT = 9521
WIDTH=100
HEIGHT=64

class PreviewServer(Thread):
    def __init__(self, port=PREVIEW_PORT, size=(WIDTH, HEIGHT), not_available_img=None):
        Thread.__init__(self)
        self.len = WIDTH*HEIGHT
        self.size = size
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('0.0.0.0',port))

        if not not_available_img:
            not_available_img = resource_filename(__name__, 'image/videonot.png')          
        self.img = Image.open(not_available_img).resize(size, resample=Image.BICUBIC)

        self.sock.settimeout(3)

        self.frame = self.img
        self.start()

    def run(self):
        logger.debug('preview server started')
        len
        while True:
            try:
                frame, addr = self.sock.recvfrom(WIDTH*HEIGHT)
                self.frame = np.asarray(Image.frombytes('L', self.size, frame))
                sleep(0.4)

            except timeout:
                logger.debug(f'sock timeout')
                self.frame = self.img

    def read(self):
        return ((WIDTH,HEIGHT), self.frame)

if __name__ == '__main__':
    preview = PreviewServer()
    preview.join()