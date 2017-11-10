class AccountsMaxHeap():
    def __init__(self):
        self.heap = [None]
        self.size = 0

    def __len__(self):
        return self.size

    def __str__(self):
        toReturn = ""
        for index, account in enumerate(self.heap):
            if index > self.size:
                break
            if index == 0:
                continue
            toReturn += str(account) + "\n"
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
    def insertAccount(self, account):
        
        self.size += 1
        i = self.size
        self.heap.append(account) # Insert at end of array

        # Fix max heap property if violated
        while i != 1 and self.heap[self.parent(i)].frequency < self.heap[i].frequency:
            self.swap(self.parent(i), i)
            i = self.parent(i)

        return
    
    # MinHeapify after deletions
    def maxHeapify(self, i):
        
        left = self.left(i)
        right = self.right(i)
        biggestAccountIndex = i

        # If left is bigger
        if left < self.size and self.heap[left].frequency > self.heap[biggestAccountIndex].frequency :
            biggestAccountIndex = left
        # If right is bigger
        if right < self.size and self.heap[right].frequency > self.heap[biggestAccountIndex].frequency:
            biggestAccountIndex = right
        # If a bigger child was found
        if biggestAccountIndex != i:
            self.swap(biggestAccountIndex, i)
            self.maxHeapify(biggestAccountIndex)
        
        return
    
    # Remove account from heap
    def removeAccount(self, idAccount):
        
        i, toRemove = self.findAccountIndexObj(idAccount)
        self.heap[i] = self.heap[self.size]
        self.size -= 1
        self.heap.pop()

        print(i)
        print(toRemove)

        self.maxHeapify(i)
        
        
        return
    
    # When account is used, key is increased and heap is fixed
    def increaseKey(self, idAccount):
        
        i, account = self.findAccountIndexObj(idAccount)
        if(account is not None):
            account.frequency += 1

            # Fix max heap property if violated
            while i != 1 and self.heap[self.parent(i)].frequency < self.heap[i].frequency:
                self.swap(self.parent(i), i)
                i = self.parent(i)

            return

    # Utility method for account finding, that returns also the index
    def findAccountIndexObj(self, idAccount):
        for index, account in enumerate(self.heap):
            if index > self.size:
                return None
            if index == 0:
                continue
            if account.idAccount == idAccount:
                return (index, account)
        return 0, None  
    
    # Utility method for account finding
    def findAccountObj(self, idAccount):
        for index, account in enumerate(self.heap):
            if index > self.size:
                return None
            if index == 0:
                continue
            if account.idAccount == idAccount:
                return account
        return None  
    
    def getHeapList(self):
        return self.heap

if __name__ == "__main__":
    print()