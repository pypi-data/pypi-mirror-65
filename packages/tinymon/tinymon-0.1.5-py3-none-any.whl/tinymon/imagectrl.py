from PIL import Image

MAX_WIDTH = 256
MAX_HEIGHT = 64
nullimg = Image.new(mode='L',size=(MAX_WIDTH,MAX_HEIGHT), color=0)
class ImageCtrl():
    def __init__(self, pos=(0,0), size=(MAX_WIDTH,MAX_HEIGHT), path=None):
        self.pos = pos
        self.size = size
        self.path = path
        self.open(path=path, pos=pos, size=size)
            
    def open(self, path, pos=None, size=None):
        if pos:
            self.pos = pos 
        if size:
            self.size = size 
        
        sx, sy = self.pos
        w, h = self.size
        x = min(sx, MAX_WIDTH)
        y = min(sy, MAX_HEIGHT)
        w = min(sx+w, MAX_WIDTH)
        h = min(sy+h, MAX_HEIGHT)
        if path:
            im = Image.open(path).resize((w-x, h-y), resample=Image.BICUBIC)
            self.im = im.convert("L")
        else:
            self.im = Image.new(mode='L',size=self.size, color=0)
    
    def changePos(self, pos):
        self.pos = pos
        
    def paste(self, im, box=(0,0)):
        self.im.paste(im.im, box)
        
    def clear(self, image):
        self.im.paste(image, (0,0))
