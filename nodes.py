import time

class User:
    def __init__(self, idUser, name):
        self.idUser = idUser
        self.name = name
        self.accounts = AccountsMaxHeap()

    def __str__(self):
        return str(self.idUSer)

    def __hash__(self):
        return hash(self.idUser)

    def getId(self):
        return self.idUser

    def addAccount(self, idAccount):
        if not self.accounts.accountExist(idAccount):
            myAccount = Account(idAccount, self)
            self.accounts.insertAccount(myAccount)

    def removeAccount(self, idAccount):
        if self.accounts.accountExist(idAccount):
            self.accounts.removeAccount(myAccount)

    def useAccount(self, idAccount):
        if self.accounts.accountExist(idAccount):
            self.accounts.increaseKey(idAccount)


class Account:
    def __init__(self, idAccount, user, frequency = 0):
        self.idAccount = idAccount
        self.idUser = user
        self.frequency = frequency
        self.edges = EdgesMinHeap()

    def __str__(self):
        return str(self.idAccount)

    def __hash__(self):
        return hash(self.idAccount)

    def getId(self):
        return self.idAccount

    def addEdge(self, dest, quantity):
        if self.edges.getTotalEdges() == 15:
            self.edges.removeOldest()
        myEdge = self.edges.getEdge(dest)
        if myEdge is not None:
            myEdge.uses + 1
            myEdge.add(quantity)
        else:
            newEdge = Edge(dest, 1)
            newEdge.add(quantity)
            self.edges.insertEdge(newEdge)

##    def removeEdge():
        #will see

class Edge:
    def __init__(self, dest, uses):
        self.dest = dest
        self.uses = uses
        self.quses = Queue()
        self.money = Queue()
        self.size = 0

    def __str__(self):
         return str(self.dest)

    def getDest(self):
         return self.dest

    def add(self, quantity):
        self.quses.enqueue(time.time())
        self.money.enqueue(quantity)
        self.size += 1

    def removeO(self):
        self.quses.dequeue()
        self.money.dequeue()
        self.size -= 1

    def sizeEmpty(self):
        return self.size == 0

class Queue:
    def __init__(self,queue):
        self.queue = []
    def dequeue(self):
        return self.queue.pop(0)
    def enqueue(self,element):
        self.queue.append(element)

if __name__ == "__main__":
    while True:
        print (time.time())
