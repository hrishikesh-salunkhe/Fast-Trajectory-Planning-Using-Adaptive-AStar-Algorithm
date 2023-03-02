
# todo add print function, could be used for debugging.
# check any border condition

import sys


class minHeap:
    def __init__(self):
        # intialize heap list
        self.HeapArray = []
        #set initial heap size to 0
        self.size = 0
        # initialize heap from 0 index
        self.HeapArray.append(-1)

    def hasLeftChild(self, elementidx):
        #fetch Heap left child and return whether it is present or not
        if self.size >= elementidx * 2 :
            return True
        else: 
            return False
    def hasRightChild(self, elementidx):
        # fCheck whether the element has a right child
        if (elementidx * 2) + 1 <= self.size:
            return True
        else:
            return False
            
    def getLeftChildidx(self, elementidx):
        # return index of right child
        leftChildidx = elementidx * 2
        return leftChildidx
    
    # function  to get index of right child of element 
    def getRightChildidx(self, elementidx):
        rightChildidx = (elementidx * 2) + 1
        return rightChildidx

# check if the element has a parent in the heap and return a boolean value 
    def hasp(self, idx):
        if  0 < idx//2:
            return True
        else:   
            return False
# check if parent has an index and return index of parent
    def getpidx(self, elementidx):
        pidx = elementidx // 2
        # print("pidx" + str(pidx))
        return pidx

# function to handle repeated swapping of elements to handle heapify actions
    def swapElements(self, x, y):
        # print(x)
        # print(y)
        self.HeapArray[x], self.HeapArray[y] = self.HeapArray[y], self.HeapArray[x]
    
    def HeapSinkSmallG(self):
        idx = 1                               ### Starting with top most element (min)
        while(self.hasLeftChild(idx)):
            smallestChildidx = self.getLeftChildidx(idx)
            # print(self.getLeftChildidx(idx))
            # print(self.getRightChildidx(idx))
            if (self.hasRightChild(idx) and self.HeapArray[self.getLeftChildidx(idx)].f > self.HeapArray[self.getRightChildidx(idx)].f):
                smallestChildidx = self.getRightChildidx(idx)
            
            if (self.hasRightChild(idx) and self.HeapArray[self.getLeftChildidx(idx)].f == self.HeapArray[self.getRightChildidx(idx)].f):
                if (self.hasRightChild(idx) and self.HeapArray[self.getLeftChildidx(idx)].g >= self.HeapArray[self.getRightChildidx(idx)].g):
                    smallestChildidx = self.getRightChildidx(idx)
            
            if self.HeapArray[smallestChildidx].f > self.HeapArray[idx].f:
                break
            elif self.HeapArray[smallestChildidx].f == self.HeapArray[idx].f and self.HeapArray[smallestChildidx].g > self.HeapArray[idx].g:
                break
            else:
                self.swapElements(idx,smallestChildidx)
            
            idx = smallestChildidx

    def HeapSinkLargeG(self):
        idx = 1                               ### Starting with top most element (min)
        # adjust the values of nodes in heap below the root
        while(self.hasLeftChild(idx)):
            smallestChildidx = self.getLeftChildidx(idx)
            # print(self.getLeftChildidx(idx))
            # print(self.getRightChildidx(idx))
            if (self.hasRightChild(idx) and self.HeapArray[self.getLeftChildidx(idx)].f > self.HeapArray[self.getRightChildidx(idx)].f):
                smallestChildidx = self.getRightChildidx(idx)
            
            if (self.hasRightChild(idx) and self.HeapArray[self.getLeftChildidx(idx)].f == self.HeapArray[self.getRightChildidx(idx)].f):
                if (self.hasRightChild(idx) and self.HeapArray[self.getLeftChildidx(idx)].g <= self.HeapArray[self.getRightChildidx(idx)].g):
                    smallestChildidx = self.getRightChildidx(idx)
            
            if self.HeapArray[smallestChildidx].f > self.HeapArray[idx].f:
                break
            elif self.HeapArray[smallestChildidx].f == self.HeapArray[idx].f and self.HeapArray[smallestChildidx].g < self.HeapArray[idx].g:
                break
            else:
                self.swapElements(idx,smallestChildidx)
            
            idx = smallestChildidx

    def bubbleUpSmallG(self):
        #adjust values above last element in heap
        idx = self.size
        # print(idx)
        # print(self.HeapArray)
        while (self.hasp(idx) and self.HeapArray[self.getpidx(idx)].f >= self.HeapArray[idx].f):
            if self.HeapArray[self.getpidx(idx)].f == self.HeapArray[idx].f and self.HeapArray[self.getpidx(idx)].g < self.HeapArray[idx].g:
                break
            self.swapElements(self.getpidx(idx),idx)
            idx = self.getpidx(idx)
    
    def bubbleUpLargeG(self):
        #adjust element above last element in heap
        idx = self.size
        # print(idx)
        # print(self.HeapArray)
        while (self.hasp(idx) and self.HeapArray[self.getpidx(idx)].f >= self.HeapArray[idx].f):
            if self.HeapArray[self.getpidx(idx)].f == self.HeapArray[idx].f and self.HeapArray[self.getpidx(idx)].g > self.HeapArray[idx].g:
                break
            self.swapElements(self.getpidx(idx),idx)
            idx = self.getpidx(idx)

    def insertElementSmallG(self, element):
        self.size = self.size + 1
        self.HeapArray.append(element)
        self.bubbleUpSmallG()
        
    def insertElementLargeG(self, element):
        self.size = self.size + 1
        self.HeapArray.append(element)
        self.bubbleUpLargeG()

    def deleteElementSmallG(self):
        if self.isEmpty():
            print("Queue is Empty")
            sys.exit("Deletion from empty HeapArray")
        minElement = self.HeapArray[1]
        self.HeapArray[1] = self.HeapArray[self.size]
        self.size = self.size - 1
        self.HeapArray.pop()
        self.HeapSinkSmallG()
        return minElement

    def deleteElementLargeG(self):
        if self.isEmpty():
            print("Queue is Empty")
            sys.exit("Deletion from empty HeapArray")
        minElement = self.HeapArray[1]
        self.HeapArray[1] = self.HeapArray[self.size]
        self.size = self.size - 1
        self.HeapArray.pop()
        self.HeapSinkLargeG()
        return minElement
    
    def printHeap(self):
        for i in range (1,len(self.HeapArray)):
            print(self.HeapArray[i].idx)


    def isEmpty(self):
        if self.size == 0:
            return True
        else:
            return False

    #Comparing the idx attribute of Cell in HeapArray:
    def notInHeap(self, idx):
        for i in range(1, len(self.HeapArray)):
            if(self.HeapArray[i].idx == idx):
                return False
        
        return True 


class Cell:
    def __init__(self, idx = None, p = None):
        self.idx = idx
        self.p = p
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
      return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f
