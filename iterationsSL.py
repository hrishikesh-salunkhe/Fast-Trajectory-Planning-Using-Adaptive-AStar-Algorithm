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


def calculateAStarLargeG(grid, mGrid, start, goalNode):
    global largeGExplored
    
    start.h = calcDist(start, goalNode)

    open = []
    closed = []
    temppath = []
    open = minHeap()
    open.insertElementLargeG(start)

    count = 0
    while(not open.isEmpty()):
        currentNode = open.deleteElementLargeG()

        if currentNode.index == start.index:
            neighbours = getNeighbours(currentNode, len(mGrid))
            for i in range(0, len(neighbours)):
                mGrid[neighbours[i].index[0]][neighbours[i].index[1]] = grid[neighbours[i].index[0]][neighbours[i].index[1]]
                
        
        if currentNode.index == goalNode.index:
            mGrid[currentNode.index[0]][currentNode.index[1]] = 5
            
            temppath = solution(start, currentNode)
            
            temppath.reverse()
            return temppath
                    

        if currentNode.index not in closed:
            closed.append(currentNode.index)
            largeGExplored = largeGExplored + 1

        mGrid[currentNode.index[0]][currentNode.index[1]] = 5


        neighbours = getNeighbours(currentNode, len(mGrid))
        

        for i in range(0, len(neighbours)):
            if(mGrid[neighbours[i].index[0]][neighbours[i].index[1]] != 9 and ((neighbours[i].index not in closed) and open.notInHeap(neighbours[i].index))):
                    neighbours[i].g = currentNode.g + 1
                    neighbours[i].h = calcDist(neighbours[i],goalNode)
                    neighbours[i].f = neighbours[i].g + neighbours[i].h
                    open.insertElementLargeG(neighbours[i])

def calculateAStarSmallG(grid, mGrid, start, goalNode):
    global smallGExplored
    
    start.h = calcDist(start, goalNode)

    open = []
    closed = []
    temppath = []
    open = minHeap()
    open.insertElementSmallG(start)

    count = 0
    while(not open.isEmpty()):
        currentNode = open.deleteElementSmallG()

        if currentNode.index == start.index:
            neighbours = getNeighbours(currentNode, len(mGrid))
            for i in range(0, len(neighbours)):
                mGrid[neighbours[i].index[0]][neighbours[i].index[1]] = grid[neighbours[i].index[0]][neighbours[i].index[1]]
                
        
        if currentNode.index == goalNode.index:
            mGrid[currentNode.index[0]][currentNode.index[1]] = 5
            
            temppath = solution(start, currentNode)
            
            temppath.reverse()
            return temppath
                    

        if currentNode.index not in closed:
            closed.append(currentNode.index)
            smallGExplored = smallGExplored + 1

        mGrid[currentNode.index[0]][currentNode.index[1]] = 5


        neighbours = getNeighbours(currentNode, len(mGrid))
        

        for i in range(0, len(neighbours)):
            if(mGrid[neighbours[i].index[0]][neighbours[i].index[1]] != 9 and ((neighbours[i].index not in closed) and open.notInHeap(neighbours[i].index))):
                    neighbours[i].g = currentNode.g + 1
                    neighbours[i].h = calcDist(neighbours[i],goalNode)
                    neighbours[i].f = neighbours[i].g + neighbours[i].h
                    open.insertElementSmallG(neighbours[i])

#ENTER GRID LENGTH HERE!
gridLength = 101

largeGTime = []
smallGTime = []
largeGCells = []
smallGCells = []
indexList = []
for i in range(50):
    indexList.append(i)

for i in range (50):
    maze = create_grid(gridLength)
    maze[0][0] = 1
    maze [gridLength - 1][gridLength - 1] = 1
    # print(maze)

    largeGMaze = deepcopy(maze)
    MlargeGMaze = create_Mgrid(gridLength)
    largeGExplored = 0

    smallGMaze = deepcopy(maze)
    MsmallGMaze = create_Mgrid(gridLength)
    smallGExplored = 0 

    largeGST = time.time()

    startNode = Node ([0,0])
    goalNode = Node ([gridLength - 1,gridLength - 1])

    while startNode.index!=goalNode.index:
        largeGPath = calculateAStarLargeG(largeGMaze, MlargeGMaze, startNode, goalNode)
        if largeGPath == None:
            print("PATH NOT FOUND")
            break

        else:
            for i in range(len(largeGPath)):
                if largeGMaze[largeGPath[i].index[0]][largeGPath[i].index[1]] == 9:
                        MlargeGMaze[largeGPath[i].index[0]][largeGPath[i].index[1]] = largeGMaze[largeGPath[i].index[0]][largeGPath[i].index[1]]
                        startNode = largeGPath[i-1]
                        break

                else:
                    newNode = Node (largeGPath[i].index)
                    startNode.index = newNode.index

                    neighbours = getNeighbours(largeGPath[i], len(MlargeGMaze))
                    for i in range(0, len(neighbours)):
                        if largeGMaze[neighbours[i].index[0]][neighbours[i].index[1]] == 9:
                            MlargeGMaze[neighbours[i].index[0]][neighbours[i].index[1]] = largeGMaze[neighbours[i].index[0]][neighbours[i].index[1]]

    largeGET = time.time()

    print("No.of largeG Explored Cells")
    print(largeGExplored)
    largeGElapsedTime = largeGET - largeGST
    print('largeG Execution time:', largeGElapsedTime, 'seconds')

    smallGST = time.time()

    goalNode = Node ([0,0])
    startNode = Node ([gridLength - 1,gridLength - 1])
    
    while startNode.index!=goalNode.index:
        smallGPath = calculateAStarSmallG(smallGMaze, MsmallGMaze, startNode, goalNode)
        if smallGPath == None:
            print("PATH NOT FOUND")
            break

        else:
            for i in range(len(smallGPath)):
                if smallGMaze[smallGPath[i].index[0]][smallGPath[i].index[1]] == 9:
                        MsmallGMaze[smallGPath[i].index[0]][smallGPath[i].index[1]] = smallGMaze[smallGPath[i].index[0]][smallGPath[i].index[1]]
                        startNode = smallGPath[i-1]
                        break

                else:
                    newNode = Node (smallGPath[i].index)
                    startNode.index = newNode.index

                    neighbours = getNeighbours(smallGPath[i], len(MsmallGMaze))
                    for i in range(0, len(neighbours)):
                        if smallGMaze[neighbours[i].index[0]][neighbours[i].index[1]] == 9:
                            MsmallGMaze[neighbours[i].index[0]][neighbours[i].index[1]] = smallGMaze[neighbours[i].index[0]][neighbours[i].index[1]]

    smallGET = time.time()

    print("No.of smallG Explored Cells")
    print(smallGExplored)
    smallGElapsedTime = smallGET - smallGST
    print('smallG Execution time:', smallGElapsedTime, 'seconds')

    largeGTime.append(largeGElapsedTime * 1000)
    smallGTime.append(smallGElapsedTime * 1000)
    largeGCells.append(largeGExplored)
    smallGCells.append(smallGExplored)   

meanlargeGTime = sum(largeGTime) / len(largeGTime)
meansmallGTime = sum(smallGTime) / len(smallGTime)
meanlargeGCells = sum(largeGCells) / len(largeGCells)
meansmallGCells = sum(smallGCells) / len(smallGCells)

print("meanlargeGTime: " + str(meanlargeGTime))
print("meansmallGTime: " + str(meansmallGTime))
print("meanlargeGCells: " + str(meanlargeGCells))
print("meansmallGCells: " + str(meansmallGCells))

fig = plt.figure()
fig.set_figheight(20)
fig.set_figwidth(20)

fig1 = fig.add_subplot(2,1,1)
# fig1.set_title("Large G Values vs. Small G Values: Number of expanded cells")
fig1.plot(indexList, largeGCells, color = 'blue', label = 'Large G Values Expanded Cells')
fig1.plot(indexList, smallGCells, color = 'orange', label = 'Small G Values Expanded Cells')
fig1.axhline(y=np.nanmean(largeGCells), linestyle='--', color = 'blue', label = 'Large G Values Expanded Cells - Mean')
fig1.axhline(y=np.nanmean(smallGCells), linestyle='--', color = 'orange', label = 'Small G Values Expanded Cells - Mean')
fig1.legend(["Large G Values Expanded Cells", "Small G Values Expanded Cells", "Large G Values Expanded Cells - Mean", "Small G Values Expanded Cells - Mean"], loc ="lower right")
fig1.set_xlabel("Number of sample environments")
fig1.set_ylabel("Number of Expanded Cells")
fig.canvas.draw()
fig.canvas.flush_events()

fig2 = fig.add_subplot(2,1,2)
# fig2.set_title("Large G Values vs. Small G Values: Runtime (in milliseconds)")
fig2.plot(indexList, largeGTime, color = 'blue', label = 'Large G Values Runtime')
fig2.plot(indexList, smallGTime, color = 'orange', label = 'Small G Values Runtime')
fig2.axhline(y=np.nanmean(largeGTime), linestyle='--', color = 'blue', label = 'Large G Values Runtime - Mean')
fig2.axhline(y=np.nanmean(smallGTime), linestyle='--', color = 'orange', label = 'Small G Values Runtime - Mean')
fig2.set_xlabel("Number of sample environments")
fig2.set_ylabel("Runtime (in milliseconds)")
fig2.legend(["Large G Values Runtime", "Small G Values Runtime", "Large G Values Runtime - Mean", "Small G Values Runtime - Mean"], loc ="lower right")
fig.canvas.draw()
fig.canvas.flush_events()

plt.show()
