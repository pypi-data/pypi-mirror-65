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
    def __init__(self, port=PREVIEW_PORT, pos=(0,0),size=(WIDTH, HEIGHT)):
        Thread.__init__(self)
        self.size = size
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('localhost',port))
        self.sock.settimeout(3)
        self.frame = None
        logger.info({
            "preview udp":''
            ,"port": port
            ,"pos": pos
            ,"size": size
            })
        self.start()

    def run(self):
        logger.debug('preview server started')
        while True:
            try:
                frame, addr = self.sock.recvfrom(WIDTH*HEIGHT)
                self.frame = np.asarray(Image.frombytes('L', self.size, frame))

            except timeout:
                logger.debug(f'sock timeout')
                self.frame = None

    def read(self):
        return ((WIDTH,HEIGHT), self.frame)

if __name__ == '__main__':
    preview = PreviewServer()
    preview.join()