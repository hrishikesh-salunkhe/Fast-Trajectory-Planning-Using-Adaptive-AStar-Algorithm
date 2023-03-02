import random
import numpy as numpy



#Function to get adjacent nodes for a given input node
def adjacentnodes(i, j, length):
    adjnodes = []
    
    if j != 0:
        adjnodes.append([i,j - 1])
    if j != length - 1:
        adjnodes.append([i,j + 1])
    if i != 0:
        adjnodes.append([i - 1,j])
    if i != length - 1:
        adjnodes.append([i + 1,j])
    
    random.shuffle(adjnodes)
    return adjnodes

#DFS implementation to traverse the graph and create a maze
def dfs(grid, inputStack, length):
    visitednodes = []
    while(len(inputStack) > 0):
        currentNode = inputStack.pop()

        
        if(currentNode not in visitednodes):
            visitednodes.append(currentNode)
            tempNeighbour = adjacentnodes(currentNode[0], currentNode[1], length)
            for i in range(0, len(tempNeighbour)):
                if grid[tempNeighbour[i][0]][tempNeighbour[i][1]] == 0:
                    #Setting the given node as blocked or unblocked based on a probability 
                    #of 70% to be unblocked and 30% to be blocked to randomize maze creation
                    grid[tempNeighbour[i][0]][tempNeighbour[i][1]] = numpy.random.choice([1,9], p=[0.7, 0.3])


                if((tempNeighbour[i] not in visitednodes) and (tempNeighbour[i] not in inputStack) and (grid[tempNeighbour[i][0]][tempNeighbour[i][1]] != 9)):
                    inputStack = inputStack + [tempNeighbour[i]]

#Function to print the created grid
def print_grid(grid):
    for i in range(0,len(grid)):
        print ( grid[i] )

#Main function to create grid
def create_grid(length):
    #Initialization to zero
    grid = numpy.zeros([length, length], dtype = int)

    inputStack = [[random.randrange(length),random.randrange(length)]]
    grid[inputStack[0][0]][inputStack[0][1]] = 1
    dfs(grid, inputStack, length)


    for i in range(0, length):
        for j in range(0, length):
            if(grid[i][j] == 0):
                inputStack.append([i,j])
                grid[inputStack[0][0]][inputStack[0][1]] = 1
                dfs(grid, inputStack, length)

    return grid

#Main function to create memory grid for AStar implementation
def create_Mgrid(length):
    grid = numpy.zeros([length, length], dtype = int)
    for i in range(0, length):
        for j in range(0, length):
            grid[i][j] = 1

    return grid


# newgrid = create_grid(10)
# print_grid(newgrid)
    