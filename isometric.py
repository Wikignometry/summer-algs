#################################################################
#                           Import
import math
import numpy as np
from cmu_112_graphics import * # for testing purposes
#################################################################

# from https://en.wikipedia.org/wiki/Isometric_projection 
def rotation(alpha, beta, M):
    alpha = math.radians(alpha)
    beta = math.radians(beta)
    xM =[
        [1, 0, 0],
        [0, math.cos(alpha), -math.sin(alpha)],
        [0, math.sin(alpha), math.cos(alpha)]
        ]
    yM =[
        [math.cos(beta), 0, math.sin(beta)],
        [0, 1, 0],
        [-math.sin(beta), 0, math.cos(beta)]
        ]
    zM = [
        [math.cos(beta), -math.sin(beta), 0],
        [math.sin(beta), math.cos(beta), 0],
        [0, 0, 1]
        ]
    return np.matmul(np.matmul(xM, zM), M)

def projection(M):
    matrix = [ [1, 0, 0],
                [0, 1, 0],
                [0, 0, 0]
                ]
    return np.matmul(matrix, M)

def transform(M, dx, dy): # destructive and non-destructive
    M[0] += dx
    M[1] += dy
    return M

# makes a toIsometric function that uses a particular offset
def makeToIsometric(offset):
    def toIsometric(M):
        dx, dy = offset
        M = rotation(54, 45, M)
        M = projection(M)
        # transform(M, -dx, -dy) 
        return tuple(transform((np.ndarray.tolist(M)[:2]), dx, dy)) #tuple of x, y
    return toIsometric

# def drawIsoTest(canvas):
#     z = 5
#     x0, y0, x1, y1 = 20, 20, 30, 40
#     coords = [(x0, y0), (x0, y1), (x1, y1), (x1, y0)]

#     toIsometric = makeToIsometric((50, 50))
#     drawCoords = []
#     for x, y in coords: # top plane
#         drawCoords += toIsometric([x, y, z])
#     canvas.create_polygon(drawCoords, fill='', outline='black')

#     drawCoords = [] # left plane
#     for x, y, z0 in [(x0, y0, z), (x1, y0, z), (x1, y0, 0), (x0, y0, 0)]:
#         drawCoords += toIsometric([x, y, z0])
#     canvas.create_polygon(drawCoords, fill='', outline='red')

#     drawCoords = [] # right plane
#     for x, y, z0 in [(x1, y0, z), (x1, y1, z), (x1, y1, 0), (x1, y0, 0)]:
#         drawCoords += toIsometric([x, y, z0])
#     canvas.create_polygon(drawCoords, fill='', outline='black')



# def testIsometric():
#     print('Testing Isometric...', end='') 
#     M = [1, 2, 2]
#     print(toIsometric(M))
#     print('Done')


# def redrawAll(app, canvas):
#     drawIsoTest(canvas)

# runApp(width=500, height=500)

# testIsometric()