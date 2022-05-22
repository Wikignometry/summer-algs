
# from hack112
###################################################################
#       Imported Files
from cmu_112_graphics import * # for testing purposes
from helper import *
###################################################################

# Button is the superclass for every pressable object in the program
#           –> button must be rectangular

class Button():

    def __init__(self, dimension, label=None, location=None, action=(lambda: None), fill='light grey', outline=None):
        # tuples(x, y) of center of button or None 
        self.location = location

        self.label = label

        # tuples(width, height)
        self.width, self.height = dimension

        # functions that perform a given action when the button is pressed
        self.action = action

        # color name
        self.fill = fill
        self.outline = outline

    def __repr__(self):
        return self.label

    # returns True if the button isPressed
    #       –> assumes that button is rectangular (doesn't account for rounded corners)
    def isPressed(self, x, y):
        # to prevent indexOutOfBounds error
        if self.location == None: 
            return False
        return (abs(self.location[0] - x) < self.width/2 and
                abs(self.location[1] - y) < self.height/2)

    # actual method called in keypressed
    def keyPressed(self, event):
        if self.isPressed(event.x, event.y):
            self.action()

    # draws a rounded square button
    def draw(self, canvas):
        if self.location == None: return # does not draw if location is None
        x, y = self.location
        create_roundedRectangles(canvas, x - self.width//2, y - self.height//2,
                                x + self.width//2, y + self.height//2,
                                fill=self.fill, outline=self.outline)
        canvas.create_text(x, y, 
                    text=f'{self.label}', 
                    font = ('Calbri', 12),
                    anchor='center', 
                    justify='center', 
                    fill='black')


###################################################################
#       Test Functions

def testButtonClass():
    print('Testing Button...', end='')
    button1 = Button((5,10), location=(10,20), action=lambda: 'foo')
    assert(button1.action() == 'foo')
    assert(button1.location[0] == 10)
    assert(button1.location[1] == 20)
    assert(button1.isPressed(12, 21) == True)
    assert(button1.isPressed(9, 18) == True)
    assert(button1.isPressed(5, 27) == False)
    print('Passed!')

# def appStarted(app):
#     app.button = Button((50,30), location=(100,100), label='yay', action=lambda: print('foo'), fill='royalBlue')

# def mousePressed(app, event):
#     if app.button.isPressed(event.x, event.y):
#         app.button.action()

# def redrawAll(app, canvas):
#     app.button.draw(canvas)

###################################################################
#       Code to run

testButtonClass()
# runApp(width=200, height=200)



