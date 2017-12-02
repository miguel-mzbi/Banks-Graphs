'''
Utility module that contains the minheap class.
'''

class EdgesMinHeap():
    '''
    MinHeap class for transaction holding.
    Each user account holds a minheap.
    '''
    def __init__(self):
        self.heap = [None]
        self.size = 0

    def __len__(self):
        return self.size

    def __str__(self):
        toReturn = ""
        for index, edge in enumerate(self.heap):
            if index > self.size:
                break
            if index == 0:
                continue
            toReturn += str(edge) + "\n"
        return toReturn

    def parent(self, i):
        '''
        Returns the item's parent.
        Complexity: O(1)
        '''
        return int(i/2)

    def left(self, i):
        '''
        Find left child of index i.
        Complexity: O(1)
        '''
        return 2*i

    def right(self, i):
        '''
        Find rigth child of index i.
        Complexity: O(1)
        '''
        return 2*i +1

    def swap(self, x, y):
        '''
        Swap utility for nodes inside the heap.
        Complexity: O(1)
        '''
        temp = self.heap[x]
        self.heap[x] = self.heap[y]
        self.heap[y] = temp
        return

    def insertEdge(self, edge):
        '''
        Insert operation for the heaps.
        Complexity: O(log(T))
        '''
        self.size += 1
        i = self.size
        self.heap.append(edge) # Insert at end of array

        # Fix min heap property if violated
        while i != 1 and self.heap[self.parent(i)].seeOldestTime() > self.heap[i].seeOldestTime():
            self.swap(self.parent(i), i)
            i = self.parent(i)

        return

    def minHeapify(self, i):
        '''
        MaxHeapify after deletions.
        Complexity: O(log(T))
        '''
        left = self.left(i)
        right = self.right(i)
        smallestAccountIndex = i

        # If left is smaller
        if left < self.size and self.heap[left].seeOldestTime() < self.heap[smallestAccountIndex].seeOldestTime():
            smallestAccountIndex = left
        # If right is smaller
        if right < self.size and self.heap[right].seeOldestTime() < self.heap[smallestAccountIndex].seeOldestTime():
            smallestAccountIndex = right
        # If a smaller child was found
        if smallestAccountIndex != i:
            self.swap(smallestAccountIndex, i)
            self.minHeapify(smallestAccountIndex)

        return

    def getIndexEdge(self, destination):
        '''
        Utility method for transaction finding, that returns also the index.
        Complexity: O(T)
        '''
        for index, edge in enumerate(self.heap):
            if index == 0:
                continue
            if index > self.size:
                return None
            if edge.dest == destination:
                return index, edge
        return 0, None

    def getEdge(self, destination):
        '''
        Utility method for transaction finding.
        Complexity: O(T)
        '''
        for index, edge in enumerate(self.heap):
            if index == 0:
                continue
            if index > self.size:
                return None
            if edge.dest == destination:
                return edge
        return None

    def getTotalEdges(self):
        '''
        Utility method that returns the amount of transactions in the heap.
        Not equivalent to the size. Each item in the heap has different values.
        Complexity: O(T)
        '''
        qty = 0
        for index, edge in enumerate(self.heap):
            if index == 0:
                continue
            if index > self.size:
                break
            qty += edge.uses
        return qty

    def removeOldest(self):
        '''
        Removes the oldest transaction in the heap.
        Complexity: O(log(T))
        '''
        toRemove = self.heap[1]
        r = toRemove.removeO()
        if toRemove.isEmpty():
            self.heap[1] = self.heap[self.size]
            self.size -= 1
            self.heap.pop()

        self.minHeapify(1)

        return r

    def getHeapList(self):
        '''
        Returns the heap's array.
        Complexity: O(1)
        '''
        return self.heap
