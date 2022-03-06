# -*- coding: utf-8 -*-
"""dijkstra_iter_two_copy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_svX9qsXyPuuGSPD_kRet1uKHLi8Rla1
"""

import numpy as np
# import heapq as hq
from queue import PriorityQueue 
# from shapely.geometry import Point
import matplotlib.pyplot as plt
import pygame
import cv2

"""Creating Node Class"""

class Node():
    def __init__(self, c2c, Node_Index_i, Parent_Node_Index_i, a, b):
        self.c2c = c2c # cost to come
        self.Node_Index_i = Node_Index_i
        self.Parent_Node_Index_i = Parent_Node_Index_i
        self.coordinates = [a,b]

"""Function to create a new node object"""

def new_node_object(present_node, child, cost_of_movement): # child is the coordinates of the new node
    new_node_cost = present_node.c2c + cost_of_movement
    new_node_Node_Index_i = all_nodes[-1].Node_Index_i + 1
    new_node_Parent_Node_Index_i = present_node.Node_Index_i
    new_node_coordinates = child
    
    latest_node = Node(new_node_cost, new_node_Node_Index_i, new_node_Parent_Node_Index_i, new_node_coordinates[0], new_node_coordinates[1])  ## creating new node object
    all_nodes.append(latest_node) ## appending that object to an extra list containing all the nodes, open close both
    coordinates_only.append(latest_node.coordinates)
    open_list.put([new_node_cost, new_node_Node_Index_i])

"""initializing the lists"""

open_list = PriorityQueue() # list containing whole node, not only yhe coordinates
closed_list = [] # list containing whole node, not only yhe coordinates
all_nodes = [] # list containing whole node, not only yhe coordinates
obstacle_list = []

"""Function for updating the cost and creating new node object"""

def update_cost(all_nodes, new_node_coord, present_node, cost_this):
    
        if new_node_coord in coordinates_only:   # checking if the new node coordinates are already present in the coordinates list
            index = coordinates_only.index(new_node_coord)
            
            new_cost = present_node.c2c + cost_this 
            
            if (new_cost < all_nodes[index].c2c): # comparing the cost and updating it
                all_nodes[index].c2c = new_cost
                all_nodes[index].Parent_Node_Index_i = present_node.Node_Index_i
              
                for j in open_list.queue: # updating the cost in the open list as well
                    if (j[1] == all_nodes[index].Node_Index_i):
                        j[0] = new_cost                   
        else:
            new_node_object(present_node, new_node_coord, cost_this) # creating object of the generated node

"""creating a list for storing all obatacle points"""

def obstacles(any_list):
    # circle
    for x in range(255, 340, 1):
        for y in range(140, 230, 1):
            if ((x - 300)**2 + (y - 185)**2 < 2025):
                any_list.append([y, x]) 
    # triangle 2            
    for y in range(95, 190, 1):
        for x in range(30, 110, 1):
            if (((y + 0.1136*x - 195) < 0) and ((y + 1.2318*x - 235) > 0) and ((y + 3.2*x - 441) < 0)):
                any_list.append([y, x])  
    # triangle 1
    for y in range(175, 215):
        for x in range(30, 120, 1):
            if (((y - 0.3164*x - 179)< 0) and ((y - 0.8571*x - 116)> 0) and ((y + 0.1136*x - 195) > 0)):
                any_list.append([y, x])  
    # hexagon
    for y in range(55, 145, 1):
        for x in range(160, 240, 1):
            if (x > 165 and x < 235 and ((y-0.577*x-25)<0) and ((y - 0.549*x + 50)>0) and ((y + 0.577*x - 255 )<0) and ((y + 0.549*x - 169)>0)):
                any_list.append([y, x])

"""action sets for all 8 movements"""

def up(present_node):
    
    a = present_node.coordinates[0]
    b = present_node.coordinates[1]

    new_node_coord = [(a + 1), b]  # up movement, increasing the row value

    if (a==249): # checking boundary condition
        return False
    
    elif (new_node_coord[0] == goal[0] and new_node_coord[1] == goal[1]):  # if new node is the goal
        new_node_object(present_node, new_node_coord, 1)
        print('Goal Reached') 
        return True 
       
    elif new_node_coord in obstacle_list:    # check if node is inside obstacle list
        print("node is inside the obstacle")
        return False

    else:
        update_cost(all_nodes, new_node_coord, present_node, 1)
        return False    
                   


def down(present_node):

    a = present_node.coordinates[0]
    b = present_node.coordinates[1]
    new_node_coord = [(a - 1), b] # down movement, decreasing the row value

    if (a==0): # checking boundary conditions
        return False
    
    elif (new_node_coord[0] == goal[0] and new_node_coord[1] == goal[1]):  # if new node is the goal
        new_node_object(present_node, new_node_coord, 1)
        print('Goal Reached')   
        return True
    
    elif new_node_coord in obstacle_list:    # check if node is inside obstacle list
        print("node is inside the obstacle")
        return False

    else:
        update_cost(all_nodes, new_node_coord, present_node, 1)
        return False    
   
    
def right(present_node):
    
    a = present_node.coordinates[0]
    b = present_node.coordinates[1]
    new_node_coord = [a, (b + 1)]


    if (b==399):
        return False
    
    elif (new_node_coord[0] == goal[0] and new_node_coord[1] == goal[1]):
        new_node_object(present_node, new_node_coord, 1)
        print('Goal Reached')  
        return True
   
    elif new_node_coord in obstacle_list:    
        print("node is inside the obstacle")
        return False

    else:
        update_cost(all_nodes, new_node_coord, present_node, 1)
        return False
    

def left(present_node):
   
    a = present_node.coordinates[0]
    b = present_node.coordinates[1]
    new_node_coord = [a, (b - 1)]
   
    if (b==0):
        
        return False

    elif (new_node_coord[0] == goal[0] and new_node_coord[1] == goal[1]):  
        new_node_object(present_node, new_node_coord, 1)
        print('Goal Reached')   
        return True
    
  
    elif new_node_coord in obstacle_list:    
        print("node is inside the obstacle")
        return False

    else:
        update_cost(all_nodes, new_node_coord, present_node, 1)
        return False
      


def up_right(present_node):
  
    a = present_node.coordinates[0]
    b = present_node.coordinates[1]
    new_node_coord = [(a + 1), (b + 1)]

    if (a==249 or b==399):
        return False

    elif (new_node_coord[0] == goal[0] and new_node_coord[1] == goal[1]): 
        new_node_object(present_node, new_node_coord, 1.4)
        print('Goal Reached') 
        return True
    
    elif new_node_coord in obstacle_list:    
        print("node is inside the obstacle")
        return False

    else:
        update_cost(all_nodes, new_node_coord, present_node, 1.4)
        return False
    


def down_right(present_node):
    a = present_node.coordinates[0]
    b = present_node.coordinates[1]
    new_node_coord = [(a - 1), (b + 1)]
    
    if (a==0 or b==399):
        return False

    elif (new_node_coord[0] == goal[0] and new_node_coord[1] == goal[1]): 
        new_node_object(present_node, new_node_coord, 1.4)
        print('Goal Reached')   
        return True
    
    elif new_node_coord in obstacle_list:    
        print("node is inside the obstacle")
        return False

    else:
        update_cost(all_nodes, new_node_coord, present_node, 1.4)
        return False


def up_left(present_node):
    a = present_node.coordinates[0]
    b = present_node.coordinates[1]
    new_node_coord = [(a + 1), (b - 1)]
    if (a==249 or b==0):
        return False

    elif (new_node_coord[0] == goal[0] and new_node_coord[1] == goal[1]):  
        new_node_object(present_node, new_node_coord, 1.4)
        print('Goal Reached')   
        return True
    
              
    elif new_node_coord in obstacle_list:    
        print("node is inside the obstacle")
        return False

    else:    
        update_cost(all_nodes, new_node_coord, present_node, 1.4)
        return False

    

def down_left(present_node):
    a = present_node.coordinates[0]
    b = present_node.coordinates[1]
    new_node_coord = [(a - 1), (b - 1)]  
    if (a==0 or b==0):
        return False

    elif (new_node_coord[0] == goal[0] and new_node_coord[1] == goal[1]): 
        new_node_object(present_node, new_node_coord, 1.4)
        print('Goal Reached')  
        return True
    
    elif new_node_coord in obstacle_list:    
        print("node is inside the obstacle")
        return False

    else:
        update_cost(all_nodes, new_node_coord, present_node, 1.4)
        return False

"""Function for movement"""

def movement(present_node):
    if (up(present_node)):
        return True
    elif (up_right(present_node)):
        return True
    if (right(present_node)):
        return True
    elif (down_right(present_node)):
        return True
    elif (down(present_node)):
        return True
    elif (down_left(present_node)):
        return True
    elif (left(present_node)):
        return True
    elif (up_left(present_node)):
        return True
    else:
        return False

"""Function for exploring"""

def func_explore(goal, open_list, all_nodes, closed_list):
    
      if (len(open_list.queue)>0):
          popping = open_list.get() # getting the least cost element out
          temp = popping[1] # [1] is the index representing node index
          node_now = all_nodes[temp-1]
          closed_list.append(node_now) # appending the new node to the closed list
          if (movement(node_now)):   
          
              return True
          else:
              return False
      else:
          print("unsolvable") # if list of open nodes becomes, then either the goal can't be reached or the goal is already reached (goal already reached condition checked earlier)
          return True

"""Function for backtracking"""

def backtrack(present_node, all_nodes, b):
    count = 0
    while (present_node.Parent_Node_Index_i != 0): # run the loop till the parent node index of present node becomes zero
        if (count == 0):
            temp = all_nodes[-1].Parent_Node_Index_i
            b.append(all_nodes[-1])
        else:
            temp = all_nodes[data].Parent_Node_Index_i
        data = temp - 1
        b.append(all_nodes[data])
        count = count + 1
        present_node = all_nodes[data]

"""function for taking user input for initial node"""

def take_initial():
    x= int(input("Enter the x coordinate of the start:  "))
    y= int(input("Enter the y coordinate of the start:  "))
    initial = [y,x]
    if (initial[0] < 0 or initial[0] > 249 or initial[1] < 0 or initial[1] > 399): # checking the boundary conditions
        print("wrong input") 
        take_initial()
    else:
        if initial in obstacle_list:
            print('initial point is inside the obstacle list') # checking the obstacle space 
            take_initial()
    return initial

"""function for taking user input for goal node"""

def take_goal():
    x= int(input("Enter the x coordinate of the start:  "))
    y= int(input("Enter the y coordinate of the start:  "))
    goal = [y,x]
    if (goal[0] < 0 or goal[0] > 249 or goal[1] < 0 or goal[1] > 399): # checking the boundary conditions
        print("wrong goal") 
        take_goal()
    else:
        if goal in obstacle_list:
            print('goal point is inside the obstacle list') # checking the obstacle space
            take_goal()
    return goal

"""taking start and goal inputs, and creating initial object"""

coordinates_only = []
backtrack_list = []

obstacles(obstacle_list)

initial = take_initial()
goal = take_goal()

initial_node = Node(0, 1, 0, initial[0], initial[1])    

open_list.put([initial_node.c2c, initial_node.Node_Index_i])
all_nodes.append(initial_node)
coordinates_only.append(initial)

while (1):
    if (func_explore(goal, open_list, all_nodes, closed_list)):
        break  
    else:
        # print("")
        pass

backtrack(all_nodes[-1], all_nodes, backtrack_list)


## THE CODE BELOW IS TO PLOT A STILL IMAGE OF THE OBSTACLES ALONG WITH THE BACKTRACKED PATH USING MATPLOTLIB ##

# listx = []
# listy= []
# backtrack_x = []
# backtrack_y = []
# for i in backtrack_list:
#     backtrack_x.append(i.coordinates[0])
#     backtrack_y.append(i.coordinates[1])

# for i in obstacle_list:
#     listx.append(i[0])
#     listy.append(i[1])

# plt.pause(0.5)
# plt.scatter(listy, listx, c = 'r', s = 0.5)
# plt.plot(backtrack_y, backtrack_x, c = 'g')
# plt.axis([0, 400, 0, 250])
# plt.pause(0.5)
# plt.show()

##############################################

new_canvas = np.zeros((401,251,3),np.uint8) 
#for every point that belongs within the obstacle
for pp in (obstacle_list): 
    x = pp[1]
    y = pp[0]
    new_canvas[(x,y)]=[0,255,0] #assigning a green coloured pixel
#rotating the image for correct orientation
new_canvas =  cv2.rotate(new_canvas, cv2.ROTATE_90_COUNTERCLOCKWISE)
new_canvas_copy_backtrack = new_canvas.copy()
#making a copy for showing the visited nodes on the obstacle space
#can be used for the animation
new_canvas_copy_visited = new_canvas.copy()
new_canvas_copy_visited = cv2.resize(new_canvas_copy_visited,(600,400))
#showing the obstacle map
cv2.imshow('new_canvas',new_canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()

backtrack_coord = []
for i in backtrack_list:
    backtrack_coord.append(i.coordinates)

all_nodes_coord = []
for i in all_nodes:
    all_nodes_coord.append(i.coordinates)    

closed_list_coord = []
for i in closed_list:
    closed_list_coord.append(i.coordinates)

pygame.init()

display_width = 400
display_height = 250

gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)
pygame.display.set_caption('Covered Nodes- Animation')

black = (0,0,0)
white = (0,255,255)
surf = pygame.surfarray.make_surface(new_canvas_copy_visited)

clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:  
            done = True   
 
    gameDisplay.fill(black)
    for path in all_nodes_coord:
        if path not in new_canvas_copy_visited:
            x = path[0]
            y = abs(200-path[1])
            pygame.draw.rect(gameDisplay, white, [x,y,1,1])
            pygame.display.flip()
    for path in backtrack_coord:
        
        pygame.time.wait(5)
        x = path[0]
        y = abs(200-path[1])
        pygame.draw.rect(gameDisplay, (0,0,255), [x,y,1,1])
        pygame.display.flip()
        
    done = True
pygame.quit()

# visited path
for path in closed_list_coord:
    #print(path)
    x = path[0]
    y = path[1]
    new_canvas_copy_backtrack[(200-y,x)]=[255,0,0] # setting every backtracked pixel to white
# showing the final backtracked path
new_backtracked = cv2.resize(new_canvas_copy_backtrack,(600,400))
cv2.imshow('visited',new_backtracked)
cv2.waitKey(0)
cv2.destroyAllWindows()

#backtracked path
for path in backtrack_list:
    x = path[0]
    y = path[1]
    new_canvas_copy_backtrack[(200-y,x)]=[0,255,0] # setting every backtracked pixel to green
# showing the final backtracked path
new_backtracked = cv2.resize(new_canvas_copy_backtrack,(600,400))
cv2.imshow('new_backtracked',new_backtracked)
cv2.waitKey(0)
cv2.destroyAllWindows()