'''
Utility module that contains the maxheap class.
'''

class AccountsMaxHeap():
    '''
    MaxHeap class for account holding.
    Each user holds a maxheap.
    '''
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

    def insertAccount(self, account):
        '''
        Insert operation for the heaps.
        Complexity: O(log(A))
        '''
        self.size += 1
        i = self.size
        self.heap.append(account) # Insert at end of array

        # Fix max heap property if violated
        while i != 1 and self.heap[self.parent(i)].frequency < self.heap[i].frequency:
            self.swap(self.parent(i), i)
            i = self.parent(i)

        return

    def maxHeapify(self, i):
        '''
        MaxHeapify after deletions.
        Complexity: O(log(A))
        '''
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

    def removeAccount(self, idAccount):
        '''
        Remove account from heap.
        Complexity: O(log(A))
        '''
        i, toRemove = self.findAccountIndexObj(idAccount)
        self.heap[i] = self.heap[self.size]
        self.size -= 1
        self.heap.pop()

        print(i)
        print(toRemove)

        self.maxHeapify(i)

        return

    def increaseKey(self, idAccount):
        '''
        When account is used, key is increased and heap is fixed.
        Complexity: O(log(A))
        '''
        i, account = self.findAccountIndexObj(idAccount)
        if account is not None:
            account.frequency += 1
            # Fix max heap property if violated
            while i != 1 and self.heap[self.parent(i)].frequency < self.heap[i].frequency:
                self.swap(self.parent(i), i)
                i = self.parent(i)

            return

    def findAccountIndexObj(self, idAccount):
        '''
        Utility method for account finding, that returns also the index.
        Complexity: O(A)
        '''
        for index, account in enumerate(self.heap):
            if index > self.size:
                return None
            if index == 0:
                continue
            if account.idAccount == idAccount:
                return (index, account)
        return 0, None

    def findAccountObj(self, idAccount):
        '''
        Utility method for account finding.
        Complexity: O(A)
        '''
        for index, account in enumerate(self.heap):
            if index > self.size:
                return None
            if index == 0:
                continue
            if account.idAccount == idAccount:
                return account
        return None

    def getHeapList(self):
        '''
        Returns the heap's array.
        Complexity: O(1)
        '''
        return self.heap
