#################################################################
#                           Import
# imports node and random
from maze import *
from button import *
#################################################################

def appStarted(app):
    app.maze = Maze(10, 10, app)
    app.maze.dfs()
    d = {'dfs': app.maze.dfsIter, 'prims': app.maze.prims,'kruskals': app.maze.kruskals,'aldousBroder': app.maze.aldousBroder}
    app.buttons = [DropDown((100, 40), d, (app.width//2, 20), 'maze alg')]

def mousePressed(app, event):
    for button in app.buttons:
        button.mousePressed(event)

def redrawAll(app, canvas):
    app.maze.redrawAll(canvas)
    for button in app.buttons:
        button.redrawAll(canvas)

runApp(width=500, height=500)