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

scaleFac = 5
obsClea = 110
canvas = genMap()

cv.imshow("Preview",canvas)
cv.waitKey(0)
