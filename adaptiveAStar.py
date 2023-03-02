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

def calculateHeuristic(currentCell, goalCell):

    heuristic = findDistance(currentCell, goalCell)

    global closedCellsHistory
    for i in range (len(closedCellsHistory)):
        if currentCell.idx == closedCellsHistory[i].idx:
            heuristic = closedCellsHistory[i].h

    return heuristic

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

def runAdaptiveAStar(grid, mGrid, startCell, goalCell):
    
    print("CURRENT CELL: ", startCell.idx)
    
    startCell.h = calculateHeuristic(startCell, goalCell)

    path = []
    openList = minHeap()
    openList.insertElementLargeG(startCell)
    closedCells = []
    notClosed = True
    closedList = []
    
    
    while(not openList.isEmpty()):
        currentCell = openList.deleteElementLargeG()
   
        if currentCell.idx == startCell.idx:    
            adjacentCells = getAdjacentCells(currentCell, len(mGrid))

            for i in range(0, len(adjacentCells)):
                idx0 = adjacentCells[i].idx[0]
                idx1 = adjacentCells[i].idx[1] 
                mGrid[idx0][idx1] = grid[idx0][idx1]

        if goalCell.idx == currentCell.idx:
            path = generatePath(startCell, currentCell)
            
            path.reverse()

            for i in range (len(path)):
                forwardMemoryGrid[path[i].idx[0]][path[i].idx[1]] = 3 
            
            for i in range (len(closedCells)):
                closedCells[i].h = (len(path) - 1) - closedCells[i].g
                for j in range (len(closedCellsHistory)):
                    if closedCells[i].idx == closedCellsHistory[j].idx:
                        closedCellsHistory[j].h = closedCells[i].h
                        notClosed = False

                if notClosed:
                    closedCellsHistory.append(closedCells[i])

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
                forwardMemoryGrid[idx0][idx1] = 1
            
            return path
                    

        if currentCell.idx in closedList:
            for i in range (len(closedCells)):
                if closedCells[i].idx == currentCell.idx:
                    closedCells[i].h = currentCell.h
        else:
            closedList.append(currentCell.idx)
            closedCells.append(currentCell)
            
        adjacentCells = getAdjacentCells(currentCell, len(mGrid))

        for i in range(0, len(adjacentCells)):
            idx0 = adjacentCells[i].idx[0]
            idx1 = adjacentCells[i].idx[1]
            if(((adjacentCells[i].idx not in closedList) and openList.notInHeap(adjacentCells[i].idx)) and mGrid[idx0][idx1] != 9):
                adjacentCells[i].h = calculateHeuristic(adjacentCells[i],goalCell)
                adjacentCells[i].g = currentCell.g + 1
                adjacentCells[i].f = adjacentCells[i].g + adjacentCells[i].h
                openList.insertElementLargeG(adjacentCells[i])

maxSize = 21

grid = create_grid(maxSize)
grid[0][0] = 1
grid [maxSize - 1][maxSize - 1] = 1

closedCellsHistory = []

goalCell = Cell ([maxSize - 1,maxSize - 1])
startCell = Cell ([0,0])

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
plot3.set_title("Adaptive A*")
plot3.imshow(forwardMemoryGrid, cmap=colorMap4)
plot.canvas.draw()
plot.canvas.flush_events()

plt.show()

while goalCell.idx != startCell.idx:
    
    forwardPath = runAdaptiveAStar(forwardGrid, forwardMemoryGrid, startCell, goalCell)
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

time.sleep(3)

