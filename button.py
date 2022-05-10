###################################################################
#       Imported Files
from cmu_112_graphics import *
###################################################################

class Button():

    def __init__(self, dimension, location=None, action=None, 
                fill='blue', outline=None, label=None, textFill='black',
                fontSize=12, textAnchor='center', font='Calbri', style='roman',
                ):
        
        # tuples(x, y) of center of button or None 
        self.location = location

        # tuples(width, height)
        self.width, self.height = dimension

        # functions that perform a given action when the button is pressed
        self.action = action

        # color name
        self.fill = fill
        self.outline = outline
        self.label = label
        self.textFill = textFill

        self.font = font
        self.style = style # bold underline italics roman
        self.fontAnchor = textAnchor # supports center and se

        # int
        self.fontSize = fontSize 

    def __repr__(self):
        if self.label != None:
            return self.label
        elif self.action != None:
            return self.action.__name__
        else: return 'unknown button'

    def __eq__(self, other):
        if (isinstance(other, Button) and (self.action == None or other.action == None)):
            return False
        return self.action == other.action

    # returns True if the button isPressed
    #       –> assumes that button is rectangular (doesn't account for rounded corners)
    def isPressed(self, x, y):
        # to prevent indexOutOfBounds error
        if self.location == None: 
            return False
        return (abs(self.location[0] - x) < self.width/2 and
                abs(self.location[1] - y) < self.height/2)
            
    def mousePressed(self, event):
        if self.isPressed(event.x, event.y): self.action()

    # draws a rectangular button
    def redrawAll(self, canvas):
        if self.location == None: return # does not draw if location is None
        x, y = self.location
        canvas.create_rectangle(x - self.width//2, y - self.height//2,
                                x + self.width//2, y + self.height//2,
                                fill=self.fill, outline=self.outline)        

        if self.label != None:
            if self.fontAnchor == 'center':
                canvas.create_text(x, y, 
                        text=f'{self.label}', 
                        font = (self.font, self.fontSize, self.style),
                        anchor='center', 
                        justify='center', 
                        fill=self.textFill)
            else:
                margin=10
                canvas.create_text(x+self.width//2-margin, y+self.height//2-margin, 
                        text=f'{self.label}', 
                        font = (self.font, self.fontSize, self.style),
                        anchor='se', 
                        justify='right', 
                        fill=self.textFill)
    
class DropDown(Button):

    def __init__(self, dimension, childButtons, location, label):
        super().__init__(dimension, location=location, label=label, fill='light grey')
        self.isDrop = False
        self.childButtons = self.makeChildButtons(childButtons) #input dictionary output Button list
        self.action = self.toggleIsDrop

    def toggleIsDrop(self):
        self.isDrop = not self.isDrop

    def makeChildButtons(self, childButtons):
        children = []
        x, y = self.location
        for label in childButtons:
            action = childButtons[label]
            y += self.height
            children += [Button((self.width, self.height), location=(x, y), label=label, action=action, fill='light grey')]
        return children

    def mousePressed(self, event):
        super().mousePressed(event)
        if self.isDrop:
            for button in self.childButtons:
                button.mousePressed(event)

    def redrawAll(self, canvas):
        super().redrawAll(canvas)
        if self.isDrop:
            for button in self.childButtons:
                button.redrawAll(canvas)

        

