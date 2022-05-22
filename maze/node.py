#################################################################
#                           Import
from isometric import *
#################################################################

class Node:
    def __init__(self, location):
        self.location = location # client can decide how it is stored
        self.nbors = set() # set of nodes

    def __hash__(self):
        return hash(self.location)

    def getNbors(self): # O(1)
        return self.nbors

    def getLoc(self): # O(1)
        return self.location

    def addNbor(self, other): 
        self.nbors.add(other)

    def mutualAddNbor(self, other):
        self.nbors.add(other)
        other.nbors.add(self)

    def removeNeighbour(self, other):
        self.nbors.discard(other)

    def mutualRemoveNeighbour(self, other):
        self.nbors.discard(other)
        other.nbors.discard(self)

    def hasEdge(self, other):
        return other in self.nbors

    # this only works with horizontal/vertical lines
    def draw(self, canvas, other, margin, convertToCoords): 
        # convertToCoords is a function, margin is an int
        xSelf, ySelf = convertToCoords(self.location)
        xOther, yOther = convertToCoords(other.location)
        x0, y0, x1, y1 = xSelf-margin, ySelf-margin, xOther+margin, yOther+margin
        canvas.create_rectangle(x0, y0, x1, y1, fill='black')
        # canvas.create_oval(xSelf-25, ySelf-25, xSelf+25, ySelf+25)
        # canvas.create_oval(xOther-25, yOther-25, xOther+25, yOther+25)
        
    def drawIso(self, canvas, other, margin, convertToCoords, z, offset, xRot, zRot):
        
        xSelf, ySelf = convertToCoords(self.location)
        xOther, yOther = convertToCoords(other.location)
        x0, y0, x1, y1 = xSelf-margin, ySelf-margin, xOther+margin, yOther+margin
        coords = [(x0, y0), (x0, y1), (x1, y1), (x1, y0)]

        toIsometric = makeToIsometric(offset, xRot, zRot) # returns function that uses offset

        
        if ySelf == yOther:
            drawCoords = [] # right plane
            for x, y, z0 in [(x1, y0, z), (x1, y1, z), (x1, y1, 0), (x1, y0, 0)]:
                drawCoords += toIsometric([x, y, z0])
            canvas.create_polygon(drawCoords, fill='#C9F0F5')

        drawCoords = [] # left plane
        for x, y, z0 in [(x0, y1, z), (x1, y1, z), (x1, y1, 0), (x0, y1, 0)]:
            drawCoords += toIsometric([x, y, z0])
        canvas.create_polygon(drawCoords, fill='#6B9A9E')

        if ySelf != yOther:
            drawCoords = [] # right plane
            for x, y, z0 in [(x1, y0, z), (x1, y1, z), (x1, y1, 0), (x1, y0, 0)]:
                drawCoords += toIsometric([x, y, z0])
            canvas.create_polygon(drawCoords, fill='#C9F0F5')

        drawCoords = []
        for x, y in coords: # top plane
            drawCoords += toIsometric([x, y, z])
        canvas.create_polygon(drawCoords, fill='#9DCDD2')
        










    