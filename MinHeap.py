
class EdgesMinHeap():
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

    # Find parent of index i
    def parent(self, i):
        return int(i/2)

    # Find left child of index i
    def left(self, i):
        return 2*i
    
    # Find rigth child of index i
    def right(self, i):
        return 2*i +1
    
    # Swap utility for nodes inside the heap
    def swap(self, x, y):
        temp = self.heap[x]
        self.heap[x] = self.heap[y]
        self.heap[y] = temp
        return
    
    # Insert operation for the heaps
    def insertEdge(self, edge):
        
        self.size += 1
        i = self.size
        self.heap.append(edge) # Insert at end of array

        # Fix min heap property if violated
        while i != 1 and self.heap[self.parent(i)].seeOldestTime() > self.heap[i].seeOldestTime():
            self.swap(self.parent(i), i)
            i = self.parent(i)

        return
    
    # MinHeapify after deletions
    def minHeapify(self, i):
        
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

    # Utility method for edge finding, that returns also the index
    def getIndexEdge(self, destination):
        for index, edge in enumerate(self.heap):
            if index == 0:
                continue
            if index > self.size:
                return None
            if edge.dest == destination:
                return index, edge
        return 0, None

    # Utility method for edge finding
    def getEdge(self, destination):
        for index, edge in enumerate(self.heap):
            if index == 0:
                continue
            if index > self.size:
                return None
            if edge.dest == destination:
                return edge
        return None 

    # Total number of edges (Including multiple conections per destination)
    def getTotalEdges(self):
        qty = 0
        for index, edge in enumerate(self.heap):
            if index == 0:
                continue
            if index > self.size:
                break
            qty += edge.uses
        return qty

    # Removes oldest of heap (Basically a extract min)
    def removeOldest(self):
        
        toRemove = self.heap[1]
        r = toRemove.removeO()
        if toRemove.isEmpty():
            self.heap[1] = self.heap[self.size]
            self.size -= 1
            self.heap.pop()

        self.minHeapify(1)

        return r

    def getHeapList(self):
        return self.heap

if __name__ == "__main__":
    print()