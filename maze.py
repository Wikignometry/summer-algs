#################################################################
#                           Import
from node import *
import random
from cmu_112_graphics import *
#################################################################


# https://en.wikipedia.org/wiki/Maze_generation_algorithm
class Maze:
    def __init__(self, rows, cols, app=False):
        self.nodes = dict() # key = location, value = Node object
        # The Node object never has to be indexed until necessary
        self.rows =  rows #int
        self.cols = cols #int
        self.gridDimensions(app) # gets the grid dimensions (maybe pass in?)
        self.makeNodes() # intialixes all the nodes
        self.pathSize = 10 # width of the path

    def gridDimensions(self, app):
        self.cellSize = 50
        if app:
            print('foo')
            app.width = self.cols * self.cellSize
            app.height = self.cols * self.cellSize
        self.width = self.cols * self.cellSize
        self.height = self.rows * self.cellSize
        self.margin = 20

    # makes unconnected nodes
    def makeNodes(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.nodes[(row, col)] = Node((row, col))
    
    # checks that a row, col is inside the grid
    def isInGrid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    # returns a list of the unvisited neighbours of a particular location
    def getUnvisitedNbors(self, visited, row, col):
        legalNbors = []
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)] # directions
        for drow, dcol in directions:
            if self.isInGrid(drow+row, dcol+col) and (drow+row, dcol+col) not in visited:
                legalNbors.append((drow+row, dcol+col))
        return legalNbors

    # returns a list of the neighbours of a particular location
    def getLegalNbors(self, location):
        row, col = location
        legalNbors = []
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)] # directions
        for drow, dcol in directions:
            if self.isInGrid(drow+row, dcol+col):
                legalNbors.append((drow+row, dcol+col))
        return legalNbors

    # recursive dfs
    def dfs(self):
        visited = set()
        self.dfsHelper((0, 0), visited) # default currCell == 0, 0

    def dfsHelper(self, currCell, visited):
        visited.add(currCell)
        row, col = currCell
        nbors = self.getUnvisitedNbors(visited, row, col)
        while  nbors != []:
            nbor = random.choice(nbors)
            self.nodes[currCell].mutualAddNbor(self.nodes[nbor])
            self.dfsHelper(nbor, visited)
            nbors = self.getUnvisitedNbors(visited, row, col)

    # iterative variation of dfs
    def dfsIter(self):
        visited = set() # adds the 0,0 node
        stack = [(0, 0)] 
        while stack != []:
            currCell = stack.pop()
            row, col = currCell
            visited.add(currCell)
            nbors = self.getUnvisitedNbors(visited, row, col)
            if nbors != []:
                stack.append(currCell)
                nbor = random.choice(nbors)
                self.nodes[currCell].mutualAddNbor(self.nodes[nbor])
                visited.add(nbor)
                stack.append(nbor)

    # returns list of ((row1, col1), (row2, col2)) that potentially connects location with neighbours
    def getEdges(self, location):
        row, col = location
        edges = []
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)] # directions
        for drow, dcol in directions:
            if self.isInGrid(drow+row, dcol+col):
                edges.append(((row, col), (drow+row, dcol+col)))
        return edges

    # returns all the edges that can connect cells in the maze with neighbours
    def getAllEdges(self): # (for kruskals)
        edges = set()
        for row in range(self.rows):
            for col in range(self.cols):
                edges.update(self.getEdges((row, col)))
        return list(edges)

    # returns the set containing the given node
    def getNodeSet(self, node, setList): # (for kruskals)
        for elem in setList: #setList is a list of sets potentially containing given node
            if node in elem:
                return elem
        return None

    def getAllNodeSet(self):
        setList = []
        for row in range(self.rows):
            for col in range(self.cols):
                setList.append({(row, col)})
        return setList

    # prims algorithm for maze gen
    def prims(self):
        visited = set()
        visited.add((0, 0))
        wallList = self.getEdges((0, 0))
        while wallList != []:
            wall = random.choice(wallList)
            if wall[1] not in visited: # because of the way we get the edges, wall[0] doesn't matter
                self.nodes[wall[0]].mutualAddNbor(self.nodes[wall[1]])
                visited.add(wall[1])
                wallList += self.getEdges(wall[1])
            wallList.remove(wall)
    
    # kruskals for maze gen
    def kruskals(self):
        walls = self.getAllEdges()
        setList = self.getAllNodeSet()
        random.shuffle(walls)
        for wall in walls:
            nodeSet = self.getNodeSet(wall[0], setList) # nodeSet containing wall[0]
            if wall[1] not in nodeSet:
                self.nodes[wall[0]].mutualAddNbor(self.nodes[wall[1]])
                otherNodeSet = self.getNodeSet(wall[1], setList)
                setList.remove(otherNodeSet)
                nodeSet.update(otherNodeSet)
            
    def aldousBroder(self):
        visited = set()
        currCell = random.randrange(self.rows), random.randrange(self.cols)
        visited.add(currCell)
        while len(visited) != self.rows * self.cols:
            nbor = random.choice(self.getLegalNbors(currCell))
            if nbor not in visited:
                self.nodes[currCell].mutualAddNbor(self.nodes[nbor])
                visited.add(nbor)
            currCell = nbor

    # inspired by getCellBounds from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    def getCellCenter(self, location):
        row, col = location
        gridWidth  = self.width - 2*self.margin
        gridHeight = self.height - 2*self.margin
        cellWidth = gridWidth / self.cols
        cellHeight = gridHeight / self.rows
        x = self.margin + (col+0.5) * cellWidth
        y = self.margin + (row+0.5) * cellHeight
        return (x, y)
    
    def draw(self, canvas):
        for location in self.nodes:
            node = self.nodes[location]
            for nbor in node.getNbors():
                node.draw(canvas, nbor, self.pathSize, self.getCellCenter)


# def testMaze():
#     print("Testing Maze...")
#     m = Maze(5, 5)
#     m.dfs()
    

def appStarted(app):
    app.m = Maze(10, 10, app)
    app.m.aldousBroder()

def redrawAll(app, canvas):
    app.m.draw(canvas)

runApp(width=500, height=500)

    


        

            


        
    

        