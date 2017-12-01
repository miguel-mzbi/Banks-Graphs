class BankHash:
    def __init__(self):
        self.capacity = 25
        self.buckets = [None] * self.capacity
        self.alpha = .75
        self.size = 0

    def __str__(self):
        toPrint = ""
        for bucket in self.buckets:
            if bucket != None:
                toPrint += str(bucket) + "\n"
        return toPrint

    def exists(self, id):
        start = hashedkey = hash(id) % self.capacity
        done = False

        while not done:
            if self.buckets[hashedkey].getId() == id:
                val = self.buckets[hashedkey]
                return True
            else:
                hashedkey = (hashedkey + 1) % self.capacity
                if hashedkey == start or self.buckets[hashedkey] is None:
                    return False
        return val

    def resize(self):
        import copy
        l = len(self.buckets)//2
        temp = copy.deepcopy(self.buckets)

        for i in range(len(self.buckets)):
            self.buckets[i] = None

        self.capacity += len(self.buckets) + l
        self.size = 0
        self.buckets = [None] * self.capacity
        
        for element in temp:
            self.put(element)

    def put(self, item):
        if self.size/self.capacity >= self.alpha:
            self.resize()

        hashedkey = hash(item) % self.capacity

        if self.buckets[hashedkey] is None:
            self.buckets[hashedkey] = item
            self.size += 1

        else:
            hashedkey = (hashedkey + 1) % self.capacity
            i = 0
            while self.buckets[hashedkey] != None and i < self.capacity:
                hashedkey = (hashedkey + 1) % self.capacity
                i += 1
            if self.buckets[hashedkey] is None:
                self.buckets[hashedkey] = item
                self.size += 1

    def get(self, id):
        start = hashedkey = hash(id) % self.capacity
        val = None
        done = False

        while not done:
            if self.buckets[hashedkey] is not None and self.buckets[hashedkey].getId() == id:
                val = self.buckets[hashedkey]
                done = True

            else:
                hashedkey = (hashedkey + 1) % self.capacity
                if hashedkey == start or self.buckets[hashedkey] is None:
                    done = True
        return val

    def getAll(self):
        return [item for item in self.buckets if item is not None]

    def getRandomItem(self):
        import numpy as np
        i = 0
        while True:
            num = int(np.random.uniform(0, self.capacity))
            if self.buckets[num] is not None:
                return self.buckets[num]


    def delete(self,removedID):
        hashedkey = hash(removedID)% self.capacity
        i = hashedkey
        prev = self.buckets[hashedkey]
        while prev.getId() != removedID:
            if prev != None:
                i = (hashedkey + 1) % self.capacity
                prev = self.buckets[i]
                
            else:
                return None
        
        toReturn = self.buckets[i]
        self.buckets[i] = None

        while self.buckets[(i + 1) % self.capacity] != None and hash(self.buckets[(i + 1) % self.capacity].getId())%self.capacity == hashedkey:
            self.buckets[i] = self.buckets [(i+1) % self.capacity]
            i = (i + 1) % self.capacity
            self.buckets[i] = None
        
        return toReturn

    def __getitem__(self,key):
        return self.get(key)
