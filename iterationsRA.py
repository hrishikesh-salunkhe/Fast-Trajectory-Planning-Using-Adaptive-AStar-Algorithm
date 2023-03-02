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

def updateHValues(inputNode, goalNode):
    global globalClosedList

    newHValue = calcDist(inputNode, goalNode)
    for i in range (len(globalClosedList)):
        if globalClosedList[i].index == inputNode.index:
            newHValue = globalClosedList[i].h

    return newHValue

def calculateAStar(grid, mGrid, start, goalNode):
    global forwardExplored

    start.h = calcDist(start, goalNode)

    open = []
    closed = []
    temppath = []
    open = minHeap()
    open.insertElementLargeG(start)

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
            forwardExplored = forwardExplored + 1

        mGrid[currentNode.index[0]][currentNode.index[1]] = 5


        neighbours = getNeighbours(currentNode, len(mGrid))
        

        for i in range(0, len(neighbours)):
            if(mGrid[neighbours[i].index[0]][neighbours[i].index[1]] != 9 and ((neighbours[i].index not in closed) and open.notInHeap(neighbours[i].index))):
                    neighbours[i].g = currentNode.g + 1
                    neighbours[i].h = calcDist(neighbours[i],goalNode)
                    neighbours[i].f = neighbours[i].g + neighbours[i].h
                    open.insertElementLargeG(neighbours[i])

def calculateAdaptiveStar(grid, mGrid, start, goalNode):
    global adaptiveExplored
    global globalClosedList
    
    start.h = updateHValues(start, goalNode)

    open = []
    closed = []
    closedNodes = []
    temppath = []
    elementfound = 0
    open = minHeap()
    open.insertElementLargeG(start)

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
            for i in range (len(temppath)):
                aMforwardMaze[temppath[i].index[0]][temppath[i].index[1]] = 3 
            
            for i in range (len(closedNodes)):
                closedNodes[i].h = (len(temppath) - 1) - closedNodes[i].g
                for j in range (len(globalClosedList)):
                    if closedNodes[i].index == globalClosedList[j].index:
                        globalClosedList[j].h = closedNodes[i].h
                        elementfound = 1

                if elementfound != 1:
                    globalClosedList.append(closedNodes[i])

            for i in range (len(temppath)):
                aMforwardMaze[temppath[i].index[0]][temppath[i].index[1]] = 1
            
            return temppath
                    

        if currentNode.index not in closed:
            closed.append(currentNode.index)
            closedNodes.append(currentNode)
            adaptiveExplored = adaptiveExplored + 1
        
        else:
            for i in range (len(closedNodes)):
                if closedNodes[i].index == currentNode.index:
                    closedNodes[i].h = currentNode.h

        mGrid[currentNode.index[0]][currentNode.index[1]] = 5


        neighbours = getNeighbours(currentNode, len(mGrid))

        for i in range(0, len(neighbours)):
            if(mGrid[neighbours[i].index[0]][neighbours[i].index[1]] != 9 and ((neighbours[i].index not in closed) and open.notInHeap(neighbours[i].index))):
                    neighbours[i].g = currentNode.g + 1
                    neighbours[i].h = updateHValues(neighbours[i],goalNode)
                    neighbours[i].f = neighbours[i].g + neighbours[i].h
                    open.insertElementLargeG(neighbours[i])

#ENTER GRID LENGTH HERE!
gridLength = 101

forwardAStarTime = []
adaptiveAStarTime = []
forwardAStarCells = []
adaptiveAStarCells = []
indexList = []

for i in range(50):
    indexList.append(i)

for i in range(0, 50):
    maze = create_grid(gridLength)
    maze[0][0] = 1
    maze [gridLength - 1][gridLength - 1] = 1
    
    forwardMaze = deepcopy(maze)
    MforwardMaze = create_Mgrid(gridLength)
    forwardExplored = 0

    aforwardMaze = deepcopy(maze)
    aMforwardMaze = create_Mgrid(gridLength)
    globalClosedList = []
    adaptiveExplored = 0

    forwardAStarST = time.time()

    startNode = Node ([0,0])
    goalNode = Node ([gridLength - 1,gridLength - 1])

    while startNode.index!=goalNode.index:
        forwardPath = calculateAStar(forwardMaze, MforwardMaze, startNode, goalNode)
        if forwardPath == None:
            break

        else:
            for i in range(len(forwardPath)):
                if forwardMaze[forwardPath[i].index[0]][forwardPath[i].index[1]] == 9:
                        MforwardMaze[forwardPath[i].index[0]][forwardPath[i].index[1]] = forwardMaze[forwardPath[i].index[0]][forwardPath[i].index[1]]
                        startNode = forwardPath[i-1]
                        break   

                else:
                    newNode = Node (forwardPath[i].index)
                    startNode = newNode

                    neighbours = getNeighbours(forwardPath[i], len(MforwardMaze))
                    for i in range(0, len(neighbours)):
                        if forwardMaze[neighbours[i].index[0]][neighbours[i].index[1]] == 9:
                            MforwardMaze[neighbours[i].index[0]][neighbours[i].index[1]] = forwardMaze[neighbours[i].index[0]][neighbours[i].index[1]]

    forwardAStarET = time.time()

    print("Forward A* - No. of Explored Cells")
    print(forwardExplored)
    forwardAStarElapsedTime = forwardAStarET - forwardAStarST
    print('Forward A* Execution time:', forwardAStarElapsedTime, 'seconds')

    adaptiveAStarST = time.time()

    startNode = Node ([0,0])
    goalNode = Node ([gridLength - 1,gridLength - 1])
    
    while startNode.index!=goalNode.index:
        forwardPath = calculateAdaptiveStar(aforwardMaze, aMforwardMaze, startNode, goalNode)
        if forwardPath == None:
            break

        else:
            for i in range(len(forwardPath)):
                if aforwardMaze[forwardPath[i].index[0]][forwardPath[i].index[1]] == 9:
                        aMforwardMaze[forwardPath[i].index[0]][forwardPath[i].index[1]] = aforwardMaze[forwardPath[i].index[0]][forwardPath[i].index[1]]
                        startNode = forwardPath[i-1]
                        break   

                else:
                    newNode = Node (forwardPath[i].index)
                    startNode.index = newNode.index

                    neighbours = getNeighbours(forwardPath[i], len(aMforwardMaze))
                    for i in range(0, len(neighbours)):
                        if aforwardMaze[neighbours[i].index[0]][neighbours[i].index[1]] == 9:
                            aMforwardMaze[neighbours[i].index[0]][neighbours[i].index[1]] = aforwardMaze[neighbours[i].index[0]][neighbours[i].index[1]]

    adaptiveAStarET = time.time()

    print("Adaptive A* - No. of Explored Cells")
    print(adaptiveExplored)
    adaptiveAStarElapsedTime = adaptiveAStarET - adaptiveAStarST
    
    print('Adaptive A* Execution time:', adaptiveAStarElapsedTime, 'seconds')

    forwardAStarCells.append(forwardExplored)    
    adaptiveAStarCells.append(adaptiveExplored)    
    adaptiveAStarTime.append(adaptiveAStarElapsedTime * 1000)    
    forwardAStarTime.append(forwardAStarElapsedTime * 1000)    

meanadaptiveAStarTime = sum(adaptiveAStarTime) / len(adaptiveAStarTime)
meanforwardAStarTime = sum(forwardAStarTime) / len(forwardAStarTime)
meanadaptiveAStarCells = sum(adaptiveAStarCells) / len(adaptiveAStarCells)
meanforwardAStarCells = sum(forwardAStarCells) / len(forwardAStarCells)

print("meanadaptiveAStarTime: " + str(meanadaptiveAStarTime))
print("meanforwardAStarTime: " + str(meanforwardAStarTime))
print("meanadaptiveAStarCells: " + str(meanadaptiveAStarCells))
print("meanforwardAStarCells: " + str(meanforwardAStarCells))

fig = plt.figure()
fig.set_figheight(20)
fig.set_figwidth(20)

fig1 = fig.add_subplot(2,1,1)
# fig1.set_title("Forward A* vs. Adaptive A*: Number of expanded cells")
fig1.plot(indexList, forwardAStarCells, color = 'blue', label = 'Forward A* Number of Expanded Cells')
fig1.plot(indexList, adaptiveAStarCells, color = 'orange', label = 'Adaptive A* Number of Expanded Cells')
fig1.axhline(y=np.nanmean(forwardAStarCells), linestyle='--', color = 'blue', label = 'Forward A* Number of Expanded Cells - Mean')
fig1.axhline(y=np.nanmean(adaptiveAStarCells), linestyle='--', color = 'orange', label = 'Adaptive A* Number of Expanded Cells - Mean')
fig1.legend(["Forward A* Number of Expanded Cells", "Adaptive A* Number of Expanded Cells", "Forward A* Number of Expanded Cells - Mean", "Adaptive A* Number of Expanded Cells - Mean"], loc ="lower right")
fig1.set_xlabel("Number of sample environments")
fig1.set_ylabel("Number of Expanded Cells")
fig.canvas.draw()
fig.canvas.flush_events()

fig2 = fig.add_subplot(2,1,2)
# fig2.set_title("Forward A* vs. Adaptive A*: Runtime (in milliseconds)")
fig2.plot(indexList, forwardAStarTime, color = 'blue', label = 'Forward A* Runtime')
fig2.plot(indexList, adaptiveAStarTime, color = 'orange', label = 'Adaptive A* Runtime')
fig2.axhline(y=np.nanmean(forwardAStarTime), linestyle='--', color = 'blue', label = 'Forward A* Runtime - Mean')
fig2.axhline(y=np.nanmean(adaptiveAStarTime), linestyle='--', color = 'orange', label = 'Adaptive A* Runtime - Mean')
fig2.set_xlabel("Number of sample environments")
fig2.set_ylabel("Runtime (in milliseconds)")
fig2.legend(["Forward A* Runtime", "Adaptive A* Runtime", "Forward A* Runtime - Mean", "Adaptive A* Runtime - Mean"], loc ="lower right")
fig.canvas.draw()
fig.canvas.flush_events()

plt.show()

