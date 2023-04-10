'''
****************************Project-3 | Phase-2*****************************

Course  : ENPM661 - Planning
Team    : Krishna Hundekari (119239049) & Shail Shah (119340547)
UIDs    : krishnah & sshah115
github link : https://github.com/sshah115/A-star-turtlebot.git

****************************************************************************
'''

# Importing required modules/libraries
import numpy as np
import cv2 as cv
import copy

# Function to generate map with obstacles using cv functions
def genMap():

    # Generating a black background arena
    arena = np.zeros((2000,6000, 3), dtype="uint8")
    
    # Defining colors
    white = (255,255,255)
    blue = (255, 0, 0)
    orange = (0, 165, 255)

    # Drawing rectangle obstacles and image border
    cv.rectangle(arena, (1500,0), (1650,1250), blue, -1)
    cv.rectangle(arena, (1500 - (obsClea//2),- (obsClea//2)), (1650 + (obsClea//2),1250 + (obsClea//2)), white, obsClea)
    cv.rectangle(arena, (2500,750), (2650,2000), blue, -1)
    cv.rectangle(arena, (2500 - (obsClea//2),750 - (obsClea//2)), (2650 + (obsClea//2),2000 + (obsClea//2)), white, obsClea)
    cv.rectangle(arena, (-1, -1), (6000, 2000), white, 2*obsClea)

    # Drawing all polygon shaped obstacles
    cv.circle(arena, (4000,900), 500, orange,-1)
    cv.circle(arena, (4000,900), 500 + (obsClea//2), white,obsClea) 
  
    return cv.resize(arena, (int(6000/scaleFac),int(2000/scaleFac)))


# Checking coordinates if it lies in obstacle space
def obstacle_check(node_c):
    # This function will check if the points are okay, on border or
    # inside obstacle

    node = copy.deepcopy(node_c)

    xPt = int(node[0]/scaleFac)

    yPt = int((2000 - node[1])/scaleFac)

    if yPt < int(2000/scaleFac) and xPt < int(6000/scaleFac):

        print(f"The pixel value of coordinate {(node[0], node[1])} is: ", canvas[yPt, xPt])

        if canvas[yPt, xPt][0] == 0 and canvas[yPt, xPt][1] == 0 and canvas[yPt, xPt][2] == 0:
            status = False
        elif canvas[yPt, xPt][0] == 255 and canvas[yPt, xPt][1] == 255 and canvas[yPt, xPt][2] == 255:
            status = True
        else:
            status = True   

    else:
        status = True 
        print("Out of arena")

    cv.circle(canvas, (xPt,yPt), 1 , (0, 0, 255),-1) 

    return status

scaleFac = 5
thresh_for_grid = 5
obsClea = 110
canvas = genMap()

node = [1500, 1000]
stat = obstacle_check(node)

if stat:
    print("Obstacle")
else:
    print("Good to go")

cv.imshow("Preview",canvas)
cv.waitKey(0)
