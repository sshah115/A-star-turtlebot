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
from queue import PriorityQueue
import math as math
from math import dist
import matplotlib.pyplot as plt
import matplotlib.patches as patch

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

    # cv.circle(canvas, (xPt,yPt), 1 , (0, 0, 255),-1) 

    return status

def round_thresh(val):

    if val % thresh_for_grid != 0:
        val = np.round(val/thresh_for_grid)*thresh_for_grid
    return val

def check_goal(current):
    
    dt = dist((current[0], current[1]), (goal_x, goal_y))   
          
    if dt < compare_with_this:
        return True
    else:
        return False
    
def child_explored(node, UL,UR):

    node_in_action = copy.deepcopy(node)
    
    current_parent = node_in_action[3]

    clnVis = []

    #lets calculate cost part and check if the path comes in obstacle
    t = 0
    r = 33
    L = 160
    dt = 0.1
    Xn=current_parent[0]
    Yn=current_parent[1]
    clnVis.append((Xn,Yn))
    Thetan = 3.14 * current_parent[2] / 180

    D=0

    while t<1:

        t = t + dt
        Xs = Xn
        Ys = Yn
        Delta_Xn = 0.5*r * (UL + UR) * math.cos(Thetan) * dt
        Delta_Yn = 0.5*r * (UL + UR) * math.sin(Thetan) * dt
        Thetan += (r / L) * (UR - UL) * dt
        D=D+ math.sqrt(math.pow((0.5*r * (UL + UR) * math.cos(Thetan) * dt),2)+math.pow((0.5*r * (UL + UR) * math.sin(Thetan) * dt),2))

        if obstacle_check((Xn, Yn)):
            return

        Xn = Xn + Delta_Xn
        Yn = Yn + Delta_Yn

        clnVis.append((Xn, Yn))
    
    # print(clnVis)

    # print(clnVis)
    Thetan = (180 * (Thetan) / np.pi) % 360

    updated_x =  Xn
    updated_y = Yn
    updated_theta = Thetan  

    current_child = (updated_x, updated_y, updated_theta)

    c2c_moved = node_in_action[1] + D
    
    c2g = dist((updated_x, updated_y), (goal_x, goal_y)) 

    total_cost = c2c_moved + c2g

    if obstacle_check((current_child[0],current_child[1])) == False:
        if v[int(round_thresh(updated_x)/thresh)][int(round_thresh(updated_y)/thresh)] == 0:
            v[int(round_thresh(updated_x)/thresh)][int(round_thresh(updated_y)/thresh)] = 1
            if current_child not in closed_list :

                for i in range(0,(open_list.qsize())):
                    if open_list.queue[i][3] == current_child and open_list.queue[i][0] > total_cost:
                        open_list.queue[i][2] = current_parent
                open_list.put((total_cost, c2c_moved, current_parent, current_child, (UL,UR)))     
                for pt in range(len(clnVis)-1):
                    plt.plot((clnVis[pt][0], clnVis[pt + 1][0]),(clnVis[pt][1], clnVis[pt + 1][1]), color="blue")
                    # plt.pause(0.0001)
                    # if pt % 144*12 == 0:
                    #     plt.pause(0.0001)

compare_with_this = 500  

scaleFac = 5
thresh_for_grid = 5
thresh = 5
obstacle_real= int(round_thresh(float(input("\nEnter obstacle clearance: \n"))))
radius_robot = 105
obsClea = obstacle_real  + radius_robot
x_visited = [] 
y_visited = []
canvas = genMap()

home_x = 0
home_y= 0
home_theta = 45
home_x+= 500
home_y+= 1000

goal_x = 1000
goal_y = -500
goal_x += 500
goal_y += 1000

start_pose = (home_x, home_y, home_theta)
goal_pose = (goal_x, goal_y)

rpm_1= 50 * ((2*np.pi)/60)
rpm_2 = 100 * ((2*np.pi)/60)

print("\nBe patient!!! I am computing the shortest path!! \n")

action_set = [[0, rpm_1],[rpm_1, 0],[rpm_1, rpm_1],[0, rpm_2],[rpm_2, 0],[rpm_2, rpm_2],[rpm_1, rpm_2],[rpm_2, rpm_1]]
v= np.zeros((int(6000/scaleFac), int(2000/scaleFac)))
c2c = 0
parent_pose = None
total_cost = 0
adam_node = (total_cost,c2c,(parent_pose),(start_pose),(0, 0))
open_list = PriorityQueue()
open_list.put(adam_node)

closed_list = {}

fig, ax = plt.subplots(figsize=(6,2.5))

bottom_rectangle = patch.Rectangle((1500,750), 150, 1250, linewidth=1, edgecolor='g', facecolor='g')
top_rectangle = patch.Rectangle((2500,0), 150, 1250, linewidth=1, edgecolor='g', facecolor='g')
center_circle = patch.Circle((4000,1100), 500, linewidth=1, edgecolor='g', facecolor='g')
start_circle = patch.Circle((home_x,home_y), 20, linewidth=1, edgecolor='r', facecolor='r')
goal_circle = patch.Circle((goal_x,goal_y), 20, linewidth=1, edgecolor='r', facecolor='r')
# end_circle = patch.Circle((goal_x,goal_y), compare_with_this/2, linewidth=1, edgecolor='r', facecolor='None')


ax.add_patch(bottom_rectangle)
ax.add_patch(top_rectangle)
ax.add_patch(center_circle)
ax.add_patch(start_circle)
ax.add_patch(goal_circle)
# ax.add_patch(end_circle)

#Plotting the path
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title("Visualising Exploration")
plt.axis([0 , 6000 , 0 ,2000])

while not open_list == None:
    
    current_node = open_list.get() 
    if current_node[3] in closed_list: 
        continue

    x_visited.append(current_node[3][0]) 
    y_visited.append(current_node[3][1])

    closed_list[current_node[3]] = (current_node[2], current_node[4]) 
   
    if check_goal(current_node[3]): 
        goal_pose1 = (current_node[3], current_node[4])
        print("Mission Accomplished...Goal Reached")
        # print(current_node)
        break
        
    else:
        
        for action in action_set:
            current_child=child_explored(current_node, action[0],action[1]) 

plt.show()
