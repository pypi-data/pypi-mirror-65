from loguru import logger

cv_installed = None
try:
    import cv2
    cv_installed = True
except ModuleNotFoundError:
    logger.debug('cv2 not installed')

class PreviewCV():
    def __init__(self, video=0, pos=(0,0), size=(100,64)):
        assert cv_installed, 'opencv is not installed!!'
        self.size = size
        self.video = cv2.VideoCapture(video)
        if video == 0:
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def read(self):
        assert cv_installed, 'opencv is not installed!!'
        ret, frame = self.video.read()
        if not ret:
            return (self.size, None)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame = cv2.resize(frame, self.size, interpolation=cv2.INTER_LANCZOS4)
        #frame = cv2.resize(frame, self.size, interpolation=cv2.INTER_LINEAR)
        frame = cv2.resize(frame, self.size, interpolation=cv2.INTER_NEAREST)
        return self.size, frame

    def __del__(self):
        if self.video :
            self.video.release()
            # When this func called, logger is not working. 
            # So use print
            print('preview device released')