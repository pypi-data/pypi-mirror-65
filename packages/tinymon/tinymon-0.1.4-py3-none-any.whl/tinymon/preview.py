from pkg_resources import resource_string,resource_filename
from PIL import Image 
from loguru import logger

cv_installed = None
try:
    import cv2
    cv_installed = True
except ModuleNotFoundError:
    logger.debug('cv2 not installed')    

class Preview():
    def __init__(self, video=0, size=(100,64), not_available_img=None):
        self.size = size
        if not not_available_img:
            not_available_img = resource_filename(__name__, 'image/videonot.png')          
        self.img = Image.open(not_available_img).resize(size, resample=Image.BICUBIC)
        if cv_installed :
            self.video = cv2.VideoCapture(video)
            if video == 0:
                self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    def read(self):
        if not cv_installed :
            return (0, None)
        ret, frame = self.video.read()
        if not ret:
            return (self.size, None)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, self.size, interpolation=cv2.INTER_LANCZOS4)
        #frame = cv2.resize(frame, self.size, interpolation=cv2.INTER_LINEAR)
        return self.size, frame
    def __del__(self):
        if cv_installed :
            if self.video :
                self.video.release()
                # When this func called, logger is not working. 
                # So use print
                print('preview device released')