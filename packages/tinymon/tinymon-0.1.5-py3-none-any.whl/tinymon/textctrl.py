from pkg_resources import resource_filename
import numpy as np
from PIL import ImageFont, ImageDraw, Image, ImageOps
from loguru import logger

class TextCtrl():
    def __init__(self, pos=(10,10) , size=None, fontsize=14, font=None, text=None):
        if not font:
            font = resource_filename(__name__, 'font/NanumBarunGothicLight.ttf')
        
        self.font = ImageFont.truetype(font, fontsize)
        self.pos = pos
        x, y = pos
        if size:
            self.size = size 
        else:
            self.size = (255 - x, fontsize+1)   # max width 255

        if text:
            self.setText(text)
        
    def setText(self, text, invert=False, fill=255):
        if isinstance(text, str):
            self.text = text
        else:
            self.text = str(text)
        
        self.backgnd = Image.new('L', size=self.size)
        draw = ImageDraw.Draw(self.backgnd)
        draw.text((0,0), self.text, font=self.font, fill=fill)
        
        self.setInvert(invert=invert)

    def setInvert(self, invert=True):
        if invert:
            self.backgnd = ImageOps.invert(self.backgnd)
            
    def draw(self, im=None):
        im.paste(self.backgnd, self.pos)
        