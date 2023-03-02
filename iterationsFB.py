from calendar import c
from minHeap import *
from tracemalloc import start
from createGrid import *
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time
import random
from copy import copy, deepcopy
import numpy as np

class Node:
    def __init__(self, index = None, parent = None):
        self.index = index
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

def solution(startNode, currentNode):
    path = []
    while currentNode.index != startNode.index:
        path.append(currentNode)
        currentNode = currentNode.parent

    path.append(currentNode)
    return path
        

def calcDist(currentNode, goalNode):
    return (abs(goalNode.index[0] - currentNode.index[0]) + abs(goalNode.index[1] - currentNode.index[1]))

def getNeighbours(currentNode, gridLength):
    
    neighbours = []
    if(currentNode.index[0] != 0):
        neighbour1 = Node([currentNode.index[0] - 1, currentNode.index[1]], currentNode)
        neighbours.append(neighbour1)
    if(currentNode.index[1] != 0):
        neighbour2 = Node([currentNode.index[0], currentNode.index[1] - 1], currentNode)
        neighbours.append(neighbour2)
    if(currentNode.index[0] != gridLength - 1):
        neighbour3 = Node([currentNode.index[0] + 1, currentNode.index[1]], currentNode)
        neighbours.append(neighbour3)
    if(currentNode.index[1] != gridLength - 1):
        neighbour4 = Node([currentNode.index[0], currentNode.index[1] + 1], currentNode)
        neighbours.append(neighbour4)

    return neighbours

def calculateAStar(grid, mGrid, start, goalNode, flag):
    global forwardExplored
    global backwardExplored
    global forwardImageCounter
    global backwardImageCounter

    start.h = calcDist(start, goalNode)

    open = []
    closed = []
    temppath = []
    open = minHeap()
    open.insertElementLargeG(start)

    while(not open.isEmpty()):
        currentNode = open.deleteElementLargeG()

        if flag == 100:
            neighbours = getNeighbours(start, len(mGrid))
            for i in range(0, len(neighbours)):
                mGrid[neighbours[i].index[0]][neighbours[i].index[1]] = grid[neighbours[i].index[0]][neighbours[i].index[1]]

        else:
            neighbours = getNeighbours(goalNode, len(mGrid))
            for i in range(0, len(neighbours)):
                mGrid[neighbours[i].index[0]][neighbours[i].index[1]] = grid[neighbours[i].index[0]][neighbours[i].index[1]]
        
        if currentNode.index == goalNode.index:
            temppath = solution(start, currentNode)
            
            if flag == 100:
                temppath.reverse()
                for i in range (len(temppath)):
                    MforwardMaze[temppath[i].index[0]][temppath[i].index[1]] = 3 
            else:
                for i in range (len(temppath)):
                    MbackwardMaze[temppath[i].index[0]][temppath[i].index[1]] = 3 
            
            if flag == 100:
                for i in range (len(temppath)):
                    MforwardMaze[temppath[i].index[0]][temppath[i].index[1]] = 1
            
            else:
                for i in range (len(temppath)):
                    MbackwardMaze[temppath[i].index[0]][temppath[i].index[1]] = 1

            return temppath
                    

        if currentNode.index not in closed:
            closed.append(currentNode.index)
            if flag == 100:
                forwardExplored = forwardExplored + 1
            else:
                backwardExplored = backwardExplored + 1


        neighbours = getNeighbours(currentNode, len(mGrid))
        

        for i in range(0, len(neighbours)):
            if(mGrid[neighbours[i].index[0]][neighbours[i].index[1]] != 9 and ((neighbours[i].index not in closed) and open.notInHeap(neighbours[i].index))):
                    neighbours[i].g = currentNode.g + 1
                    neighbours[i].h = calcDist(neighbours[i],goalNode)
                    neighbours[i].f = neighbours[i].g + neighbours[i].h
                    open.insertElementLargeG(neighbours[i])

#ENTER GRID LENGTH HERE!
gridLength = 101

forwardTime = []
backwardTime = []
forwardCells = []
backwardCells = []
indexList = []

for i in range(50):
    indexList.append(i)

for i in range (50):
    maze = create_grid(gridLength)
    maze[0][0] = 1
    maze [gridLength - 1][gridLength - 1] = 1
    # print(maze)

    forwardMaze = deepcopy(maze)
    MforwardMaze = create_Mgrid(gridLength)
    forwardExplored = 0

    backwardMaze = deepcopy(maze)
    MbackwardMaze = create_Mgrid(gridLength)
    backwardExplored = 0 

    forwardST = time.time()

    startNode = Node ([0,0])
    goalNode = Node ([gridLength - 1,gridLength - 1])

    #Setting flag=100 for Forward AStar for visualization purpose
    flag = 100 
    while startNode.index!=goalNode.index:
        forwardPath = calculateAStar(forwardMaze, MforwardMaze, startNode, goalNode, flag)
        if forwardPath == None:
            print("PATH NOT FOUND")
            break

        else:
            for i in range(len(forwardPath)):
                if forwardMaze[forwardPath[i].index[0]][forwardPath[i].index[1]] == 9:
                        MforwardMaze[forwardPath[i].index[0]][forwardPath[i].index[1]] = forwardMaze[forwardPath[i].index[0]][forwardPath[i].index[1]]
                        startNode = forwardPath[i-1]
                        break

                else:
                    newNode = Node (forwardPath[i].index)
                    startNode.index = newNode.index

                    neighbours = getNeighbours(forwardPath[i], len(MforwardMaze))
                    for i in range(0, len(neighbours)):
                        if forwardMaze[neighbours[i].index[0]][neighbours[i].index[1]] == 9:
                            MforwardMaze[neighbours[i].index[0]][neighbours[i].index[1]] = forwardMaze[neighbours[i].index[0]][neighbours[i].index[1]]

    forwardET = time.time()

    print("No.of Forward Explored Cells")
    print(forwardExplored)
    forwardElapsedTime = forwardET - forwardST
    print('Forward Execution time:', forwardElapsedTime, 'seconds')

    backwardST = time.time()

    goalNode = Node ([0,0])
    startNode = Node ([gridLength - 1,gridLength - 1])
    #Setting flag=101 for Backward AStar for visualization purpose
    flag = 101

    while startNode.index!=goalNode.index:
        backwardPath = calculateAStar(backwardMaze, MbackwardMaze, startNode, goalNode, flag)
        if backwardPath == None:
            print("PATH NOT FOUND")
            break

        else:
            for i in range(len(backwardPath)):
                if backwardMaze[backwardPath[i].index[0]][backwardPath[i].index[1]] == 9:
                        MbackwardMaze[backwardPath[i].index[0]][backwardPath[i].index[1]] = backwardMaze[backwardPath[i].index[0]][backwardPath[i].index[1]]
                        goalNode = backwardPath[i-1]
                        break

                else:
                    newNode = Node (backwardPath[i].index)
                    goalNode.index = newNode.index

                    neighbours = getNeighbours(backwardPath[i], len(MbackwardMaze))
                    for i in range(0, len(neighbours)):
                        if backwardMaze[neighbours[i].index[0]][neighbours[i].index[1]] == 9:
                            MbackwardMaze[neighbours[i].index[0]][neighbours[i].index[1]] = backwardMaze[neighbours[i].index[0]][neighbours[i].index[1]]

    backwardET = time.time()

    print("No.of Backward Explored Cells")
    print(backwardExplored)
    backwardElapsedTime = backwardET - backwardST
    print('Backward Execution time:', backwardElapsedTime, 'seconds')

    forwardTime.append(forwardElapsedTime * 1000)
    backwardTime.append(backwardElapsedTime * 1000)
    forwardCells.append(forwardExplored)
    backwardCells.append(backwardExplored)   

meanForwardTime = sum(forwardTime) / len(forwardTime)
meanBackwardTime = sum(backwardTime) / len(backwardTime)
meanForwardCells = sum(forwardCells) / len(forwardCells)
meanBackwardCells = sum(backwardCells) / len(backwardCells)

print("meanForwardTime: " + str(meanForwardTime))
print("meanBackwardTime: " + str(meanBackwardTime))
print("meanForwardCells: " + str(meanForwardCells))
print("meanBackwardCells: " + str(meanBackwardCells))

fig = plt.figure()
fig.set_figheight(20)
fig.set_figwidth(20)

fig1 = fig.add_subplot(2,1,1)
fig1.plot(indexList, forwardCells, color = 'blue', label = 'Forward A* Expanded Cells')
fig1.plot(indexList, backwardCells, color = 'orange', label = 'Backward A* Expanded Cells')
fig1.axhline(y=np.nanmean(forwardCells), linestyle='--', color = 'blue', label = 'Forward A* Expanded Cells - Mean')
fig1.axhline(y=np.nanmean(backwardCells), linestyle='--', color = 'orange', label = 'Backward A* Expanded Cells - Mean')
fig1.legend(["Forward A* Expanded Cells", "Backward A* Expanded Cells", "Forward A* Expanded Cells - Mean", "Backward A* Expanded Cells - Mean"], loc ="lower right")
fig1.set_xlabel("Number of sample environments")
fig1.set_ylabel("Number of Expanded Cells")
fig.canvas.draw()
fig.canvas.flush_events()

fig2 = fig.add_subplot(2,1,2)
fig2.plot(indexList, forwardTime, color = 'blue', label = 'Forward A* Runtime')
fig2.plot(indexList, backwardTime, color = 'orange', label = 'Backward A* Runtime')
fig2.axhline(y=np.nanmean(forwardTime), linestyle='--', color = 'blue', label = 'Forward A* Runtime - Mean')
fig2.axhline(y=np.nanmean(backwardTime), linestyle='--', color = 'orange', label = 'Backward A* Runtime - Mean')
fig2.set_xlabel("Number of sample environments")
fig2.set_ylabel("Runtime (in milliseconds)")
fig2.legend(["Forward A* Runtime", "Backward A* Runtime", "Forward A* Runtime - Mean", "Backward A* Runtime - Mean"], loc ="lower right")
fig.canvas.draw()
fig.canvas.flush_events()

plt.show()
