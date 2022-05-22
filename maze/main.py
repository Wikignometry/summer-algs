#################################################################
#                           Import
# imports node and random
from maze import *
from button import *
#################################################################

def appStarted(app):
    app.maze = Maze(10, 10)
    app.maze.dfs()
    d = {'dfs': app.maze.dfsIter, 'prims': app.maze.prims,
        'kruskals': app.maze.kruskals,'aldousBroder': app.maze.aldousBroder}
    app.buttons = [DropDown((100, 40), d, (app.width//2, 20), 'maze alg')]
    app.zRot = 54
    app.xRot = 45
    app.wallHeight = 10
    app.isIsometric = False

def keyPressed(app, event):
    if event.key == 'Up': app.zRot += 5
    if event.key == 'Down': app.zRot -= 5
    if event.key == 'Left':app.xRot += 5
    if event.key == 'Right': app.xRot -= 5
    if event.key == 'w': app.wallHeight += 1
    if event.key == 's': app.wallHeight -= 1
    if event.key == 'i': app.isIsometric = not app.isIsometric

def mousePressed(app, event):
    for button in app.buttons:
        button.mousePressed(event)

def redrawAll(app, canvas):
    app.maze.redrawAll(canvas, app.isIsometric, xRot=app.xRot, zRot=app.zRot, z=app.wallHeight)
    for button in app.buttons:
        button.redrawAll(canvas)

runApp(width=800, height=800)