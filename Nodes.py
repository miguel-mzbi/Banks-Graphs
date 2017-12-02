'''
Module that contains the basic classes
'''
import time
import MaxHeap
import MinHeap

class User:
    '''
    User class is an object of user which will be call by the main module
    Users are stored in a hash table
    '''
    def __init__(self, idUser, name):
        self.idUser = idUser
        self.name = name
        # Stores all the accounts of the user in a MaxHeap.
        # The order criteria is how many times an account is used.
        self.accounts = MaxHeap.AccountsMaxHeap()

    def __str__(self):
        return '{:<10s} {:<15s} {:<20}'.format(self.idUser, self.name, "No. of accounts: " + str(len(self.accounts)))

    def __hash__(self):
        return hash(self.idUser)

    def getId(self):
        '''
        Returns the id of the user.
        Complexity: O(1)
        '''
        return self.idUser

    def addAccount(self, account):
        '''
        Adds an account into the accounts MaxHeap.
        Complexity: O(log(A))
        '''
        self.accounts.insertAccount(account)
        return

    def removeAccount(self, idAccount):
        '''
        Remove an account that is in the MaxHeap.
        Complexity: O(log(A))
        '''
        self.accounts.removeAccount(idAccount)
        return

    def useAccount(self, idAccount):
        '''
        Increase the number of how many times the account is used.
        Complexity: O(log(A))
        '''
        self.accounts.increaseKey(idAccount)
        return

    def makeTransaction(self, accountO, accountD, qty):
        '''
        To make a transaction between one of this user's accounts with another.
        Complexity: O(log(A))
        '''
        result = accountO.addEdge(accountD, qty)
        if result:
            self.useAccount(accountO.getId())
        return result
    
    def getOrderedAccounts(self):
        '''
        Returns an ordered list with all the user's accounts
        Complexity: O(A)
        '''
        accs = self.accounts.getHeapList()
        accs = [x.getId() for x in accs if x is not None]
        accs = sorted(accs, key=lambda x: int(x[1:]))
        return accs

    def printAccounts(self):
        '''
        To print al accounts.
        Complexity: O(A)
        '''
        print('{:<10s} {:<5s} {:<1s} {:>11s} {:<15}'.format("Account ID", "Type", " ", "Amount" , "\tOwner"))
        print(self.accounts)
        return

    def printTransactions(self):
        '''
        To print al transactions.
        Complexity: O(T)
        '''
        print(self)
        accs = iter(self.accounts.getHeapList())
        next(accs)
        for a in accs:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print('{:<12s} {:<30s}\n'.format("From " + a.idAccount, "Total No. of transactions " + str(a.edges.getTotalEdges())))
            edgs = iter(a.edges.getHeapList())
            next(edgs)
            for e in edgs:
                print(e)
        return

class Account:
    '''
    Account class creates objects of user which will be call by the main module.
    Accounts are stored in a hash table and inside each users maxheap.
    '''
    def __init__(self, idAccount, userID, accType, balance = 0):
        self.idAccount = idAccount
        self.userID = userID
        self.frequency = 0
        self.balance = balance
        self.accType = accType
        self.edges = MinHeap.EdgesMinHeap()

    def __str__(self):
        return '{:<10s} {:<5c} {:<1s} {:>11s} {:<15} {:<15}'.format(self.idAccount, self.accType, "$", str(self.balance) , "\tOwner: " + self.userID, "Frequency: " + str(self.frequency))

    def __hash__(self):
        return hash(self.idAccount)

    def getId(self):
        '''
        Returns the id of the user.
        Complexity: O(1)
        '''
        return self.idAccount

    def addEdge(self, dest, quantity):
        '''
        Add a transaction between the origin and destination.
        Complexity: O(log(T))
        '''
        myEdge = self.edges.getEdge(dest)

        # If operation can't be made because of debit with innuficient funds
        if self.accType == 'D' and self.balance-quantity < 0:
            print("Not enough funds in account " + self.idAccount + " to transfer " + str(quantity) + " to " + dest.idAccount)
            return False
        elif dest.accType == 'C' and dest.userID != self.userID:
            print("Can't transfer to a 3rd's credit account from " + self.idAccount + " to " + dest.idAccount + " the quantity " + str(quantity))
            return False
        else:
            # If max transaction in this edge has occurred
            if self.edges.getTotalEdges() == 15:
                self.edges.removeOldest()

            print("Transfering $" + str(quantity) + " from " + self.idAccount + " to " + dest.idAccount)
            self.balance -= quantity
            dest.balance += quantity

            # Add to edge is exists
            if myEdge is not None:
                myEdge.add(quantity)
            # Create new edge
            else:
                newEdge = Edge(dest, 0)
                newEdge.add(quantity)
                self.edges.insertEdge(newEdge)

            return True

    def getEdgesList(self):
        '''
        Returns the list of all transactions destinations.
        Complexity: O(T)
        '''
        return [edge.dest for edge in self.edges.getHeapList() if edge is not None]

    def getEdgesListFull(self):
        '''
        Returns the list of all transactions objects.
        Complexity: O(T)
        '''
        return [edge for edge in self.edges.getHeapList() if edge is not None]

class Edge:
    '''
    Edge class creates objects of accounts which will be call by the main module.
    Edges are stored only inside each account's minheap.
    '''
    def __init__(self, dest, uses = 0):
        self.dest = dest
        self.quses = Queue()
        self.money = Queue()
        self.uses = uses

    def __str__(self):
        toReturn = '{:<13s} {:<25s}\n'.format("To: " + self.dest.idAccount, "No. of transactions: " + str(self.uses))
        usesList = self.quses.getArray()
        moneyList = self.money.getArray()
        toReturn += '{:<25s} {:<1s} {:<10s}\n'.format("Time of transaction", " ", "Value")
        for t, m in zip(usesList, moneyList):
            toReturn += '{:<25s} {:<1s} {:<10s}\n'.format(time.ctime(t), '$', str(m))
        return toReturn

    def getDest(self):
        '''
        Returns the edge's destination.
        Complexity: O(1)
        '''
        return self.dest

    def add(self, quantity):
        '''
        Add money and time into the transaction.
        Complexity: O(1)
        '''
        self.quses.enqueue(time.time())
        self.money.enqueue(quantity)
        self.uses += 1
        return

    def removeO(self):
        '''
        Remove money and time of the oldest transaction.
        Complexity: O(1)
        '''
        self.uses -= 1
        return self.quses.dequeue(), self.money.dequeue()

    def isEmpty(self):
        '''
        To know if the queues are empty.
        Complexity: O(1)
        '''
        return self.uses == 0
    
    def seeOldestTime(self):
        '''
        To see top of queue.
        Complexity: O(1)
        '''
        return self.quses.first()

class Queue:
    '''
    Utility class with queue methods
    '''
    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def dequeue(self):
        '''
        Complexity: O(1)
        '''
        return self.queue.pop(0)

    def enqueue(self, element):
        '''
        Complexity: O(1)
        '''
        self.queue.append(element)
        return

    def first(self):
        '''
        Complexity: O(1)
        '''
        return self.queue[0]

    def getArray(self):
        '''
        Returns the queue as an array.
        Complexity: O(1)
        '''
        return self.queue

if __name__ == "__main__":
    '''
    print("TESTING METHODS\n")
    print("\nTESTING USERCREATION\n--------------------------------------------------------------------------------------")
    U1 = User("U1", "Miguel")
    print(U1)
    U2 = User("U2", "Richie")

    print("\nTESTING ACCOUNT CREATION\n--------------------------------------------------------------------------------------")
    A1 = Account("A1", "U1", 'D', 1000)
    U1.addAccount(A1)
    A2 = Account("A2", "U1", 'C', 0)
    U1.addAccount(A2)
    print(U1)
    U1.printAccounts()
    A6 = Account("A6", "U1", 'C')
    U1.addAccount(A6)
    U1.printAccounts()
    U1.removeAccount("A6")
    U1.printAccounts()

    print("\nTESTING SIMPLE TRANSACTIONS\n--------------------------------------------------------------------------------------")
    U1.makeTransaction("A1", "A2",  10000)
    U1.makeTransaction("A2", "A1",  10000)
    U1.printAccounts()

    print("\nTESTING MULTIPLE TRANSACTIONS\n--------------------------------------------------------------------------------------")
    A3 = Account("A3", "U2", 'D', 1000000)
    U1.addAccount(A3)
    U1.printAccounts()
    U1.makeTransaction("A3", "A2",  1)
    U1.makeTransaction("A3", "A2",  2)
    U1.makeTransaction("A3", "A2",  3)
    U1.makeTransaction("A3", "A2",  4)
    U1.makeTransaction("A3", "A2",  5)
    U1.makeTransaction("A3", "A2",  6)
    U1.makeTransaction("A3", "A2",  7)
    U1.makeTransaction("A3", "A2",  8)
    U1.makeTransaction("A3", "A1",  9)
    U1.makeTransaction("A3", "A1",  10)
    U1.makeTransaction("A3", "A1",  11)
    U1.makeTransaction("A3", "A2",  12)
    U1.makeTransaction("A3", "A2",  13)
    U1.makeTransaction("A3", "A2",  14)
    U1.makeTransaction("A3", "A2",  15)
    print()
    U1.printAccounts()
    U1.printTransactions()

    U1.makeTransaction("A3", "A2",  16)
    print()
    U1.printAccounts()
    U1.printTransactions()
    '''
