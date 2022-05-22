###################################################################
#       Imported Files
from cmu_112_graphics import *
from button import *
###################################################################


class Card(Button):
    def __init__(self, characteristic, action, location=None):
        dimension = (400, 300)
        fill = 'white'
        outline = 'light grey'
        super().__init__(dimension, label=None, location=location, action=action, fill=fill, outline=outline)
        
        self.characteristic = characteristic # stored as string encoded as color ('rpg'),  fill ('012'), number ('123'), shaped('dso')
        self.selected = False


    def draw(self, canvas):
        super().draw(canvas)
        self.drawShape(canvas) #TODO


    

