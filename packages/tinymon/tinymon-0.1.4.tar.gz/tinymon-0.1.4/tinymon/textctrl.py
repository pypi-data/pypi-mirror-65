from pkg_resources import resource_filename
from PIL import ImageFont, ImageDraw

class TextCtrl():
    def __init__(self, pos=(10,10) , fontsize=14, font=None, text=None):
        if not font:
            font = resource_filename(__name__, 'font/NanumBarunGothicLight.ttf')    
        self.font = ImageFont.truetype(font, fontsize)
        self.pos = pos
        if text:
            self.setText(text)
        
    def setText(self, text):
        if isinstance(text, str):
            self.text = text
        else:
            self.text = str(text)
            
    def draw(self, im=None, fill=255):
        draw = ImageDraw.Draw(im)
        draw.text(self.pos, self.text, font=self.font, fill=fill)
        return im