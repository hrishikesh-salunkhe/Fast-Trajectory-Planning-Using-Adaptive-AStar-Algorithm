from minHeap import *
from calendar import c
import matplotlib.pyplot as plt
from time import sleep
from matplotlib.colors import ListedColormap
import time
from copy import copy, deepcopy
from tracemalloc import start
from createGrid import *


class Cell:
    def __init__(self, idx = None, p = None):
        self.h = 0
        self.p = p
        self.g = 0
        self.idx = idx
        self.f = 0

def generatePath(startCell, currentCell):
    result = []
    while True:
        if startCell.idx == currentCell.idx:
            break
        else:
            result.append(currentCell)
            currentCell = currentCell.p

    result.append(currentCell)
    return result

def findDistance(currentCell, goalCell):
    xDiff = goalCell.idx[0] - currentCell.idx[0]
    yDiff = goalCell.idx[1] - currentCell.idx[1]
    distance = (abs(xDiff) + abs(yDiff))
    return distance

def getAdjacentCells(currentCell, maxSize):
    
    adjacentCells = []
    if(currentCell.idx[0] != 0):
        adjacentCells.append(Cell([currentCell.idx[0] - 1, currentCell.idx[1]], currentCell))
    if(currentCell.idx[0] != maxSize - 1):
        adjacentCells.append(Cell([currentCell.idx[0] + 1, currentCell.idx[1]], currentCell))
    if(currentCell.idx[1] != 0):
        adjacentCells.append(Cell([currentCell.idx[0], currentCell.idx[1] - 1], currentCell))
    if(currentCell.idx[1] != maxSize - 1):
        adjacentCells.append(Cell([currentCell.idx[0], currentCell.idx[1] + 1], currentCell))

    return adjacentCells

def runAStar(grid, mGrid, startCell, goalCell, isForward):
    if isForward :
        print("CURRENT CELL: ", startCell.idx)
    else:
        print("CURRENT CELL: ", goalCell.idx)

    startCell.h = findDistance(startCell, goalCell)

    path = []
    openList = minHeap()
    openList.insertElementLargeG(startCell)
    closedList = []
    
    while(not openList.isEmpty()):
        currentCell = openList.deleteElementLargeG()
   
        if not isForward :
            adjacentCells = getAdjacentCells(goalCell, len(mGrid))
        else:
            adjacentCells = getAdjacentCells(startCell, len(mGrid))

        for i in range(0, len(adjacentCells)):
            idx0 = adjacentCells[i].idx[0]
            idx1 = adjacentCells[i].idx[1] 
            mGrid[idx0][idx1] = grid[idx0][idx1]

        if goalCell.idx == currentCell.idx:
            path = generatePath(startCell, currentCell)
            
            if isForward :
                path.reverse()

            for i in range (len(path)):
                if not isForward:
                    backwardMemoryGrid[path[i].idx[0]][path[i].idx[1]] = 3 
                else:
                    forwardMemoryGrid[path[i].idx[0]][path[i].idx[1]] = 3 
                    
            if not isForward :
                if 9 not in backwardMemoryGrid:
                    plot4.imshow(backwardMemoryGrid, cmap=colorMap3)
                else:
                    plot4.imshow(backwardMemoryGrid, cmap=colorMap4)
            else:
                if 9 not in forwardMemoryGrid:
                    plot3.imshow(forwardMemoryGrid, cmap=colorMap3)
                else:
                    plot3.imshow(forwardMemoryGrid, cmap=colorMap4)

            plot.canvas.draw()
            plot.canvas.flush_events()  
            time.sleep(1)
            
            for i in range (len(path)):
                idx0 = path[i].idx[0]
                idx1 = path[i].idx[1]
                if not isForward:
                    backwardMemoryGrid[idx0][idx1] = 1
                else:
                    forwardMemoryGrid[idx0][idx1] = 1
            
            return path
                    

        if currentCell.idx not in closedList:
            closedList.append(currentCell.idx)

        adjacentCells = getAdjacentCells(currentCell, len(mGrid))

        for i in range(0, len(adjacentCells)):
            idx0 = adjacentCells[i].idx[0]
            idx1 = adjacentCells[i].idx[1]
            if(((adjacentCells[i].idx not in closedList) and openList.notInHeap(adjacentCells[i].idx)) and mGrid[idx0][idx1] != 9):
                adjacentCells[i].h = findDistance(adjacentCells[i],goalCell)
                adjacentCells[i].g = currentCell.g + 1
                adjacentCells[i].f = adjacentCells[i].g + adjacentCells[i].h
                openList.insertElementLargeG(adjacentCells[i])

maxSize = 21

grid = create_grid(maxSize)
grid[0][0] = 1
grid [maxSize - 1][maxSize - 1] = 1

goalCell = Cell ([maxSize - 1,maxSize - 1])
startCell = Cell ([0,0])

backwardGrid = deepcopy(grid)
backwardMemoryGrid = create_Mgrid(maxSize)

plt.ion()

forwardGrid = deepcopy(grid)
forwardMemoryGrid = create_Mgrid(maxSize)

colorMap4 = ListedColormap(['white', 'red', 'gray', 'black'], N=4)
colorMap = ListedColormap(['white', 'red', 'gray', 'black'], N=4)
colorMap3 = ListedColormap(['white', 'red', 'gray'], N=3)

plot = plt.figure()
plot.set_figheight(10)
plot.set_figwidth(10)

plot1 = plot.add_subplot(2,2,1)
plot1.set_title("Maze")
plot1.imshow(forwardGrid, cmap=colorMap4)
plot.canvas.draw()
plot.canvas.flush_events()

plot3 = plot.add_subplot(2,2,2)
plot3.set_title("Repeated Forward A*")
plot3.imshow(forwardMemoryGrid, cmap=colorMap4)
plot.canvas.draw()
plot.canvas.flush_events()

plot2 = plot.add_subplot(2,2,3)
plot2.set_title("Maze")
plot2.imshow(backwardGrid, cmap=colorMap4)
plot.canvas.draw()
plot.canvas.flush_events()

plot4 = plot.add_subplot(2,2,4)
plot4.set_title("Repeated Backward A*")
plot4.imshow(backwardMemoryGrid, cmap=colorMap4)
plot.canvas.draw()
plot.canvas.flush_events()

plt.show()

isForward = True 
while goalCell.idx != startCell.idx:
    
    forwardPath = runAStar(forwardGrid, forwardMemoryGrid, startCell, goalCell, isForward)
    if forwardPath != None:
        path = ""
        for i in range (len(forwardPath)):
            path += str(forwardPath[i].idx)
            if i != len(forwardPath) - 1:
                path += " -> "
            
        print("PATH:", path)
        print()

        for i in range(len(forwardPath)):
            idx0 = forwardPath[i].idx[0]
            idx1 = forwardPath[i].idx[1]
            if forwardGrid[idx0][idx1] == 9:
                    forwardMemoryGrid[idx0][idx1] = forwardGrid[idx0][idx1]
                    startCell = forwardPath[i-1]

                    break
                    
                

            else:
                newCell = Cell (forwardPath[i].idx)
                startCell.idx = newCell.idx

                adjacentCells = getAdjacentCells(forwardPath[i], len(forwardMemoryGrid))
                for i in range(0, len(adjacentCells)):
                    idx0 = adjacentCells[i].idx[0]
                    idx1 = adjacentCells[i].idx[1]
                    if forwardGrid[idx0][idx1] == 9:
                        forwardMemoryGrid[idx0][idx1] = forwardGrid[idx0][idx1]

    else:
        print("PATH NOT FOUND")
        print()
        break

goalCell = Cell ([0,0])
startCell = Cell ([maxSize - 1,maxSize - 1])

isForward = False

while startCell.idx!=goalCell.idx:
    backwardPath = runAStar(backwardGrid, backwardMemoryGrid, startCell, goalCell, isForward)
    if backwardPath == None:
        print("PATH NOT FOUND")
        print()
        break

    else:
        path = ""
        for i in range (len(backwardPath)):
            path += str(backwardPath[i].idx)
            if i != len(backwardPath) - 1:
                path += " -> "

        print("PATH: ", path)
        print()

        for i in range(len(backwardPath)):
            idx0 = backwardPath[i].idx[0]
            idx1 = backwardPath[i].idx[1]
            if backwardGrid[idx0][idx1] == 9:
                    backwardMemoryGrid[idx0][idx1] = backwardGrid[idx0][idx1]
                    goalCell = backwardPath[i-1]

                    break

            else:

                newCell = Cell (backwardPath[i].idx)
                goalCell.idx = newCell.idx

                adjacentCells = getAdjacentCells(backwardPath[i], len(backwardMemoryGrid))
                for i in range(0, len(adjacentCells)):
                    index0 = adjacentCells[i].idx[0]
                    index1 = adjacentCells[i].idx[1]
                    if backwardGrid[index0][index1] == 9:
                        backwardMemoryGrid[index0][index1] = backwardGrid[index0][index1]

time.sleep(3)

