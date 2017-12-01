import time
import MaxHeap
import MinHeap

# User class is an object of user which will be call by the main module
# Users are stored in a hash table
class User:
    def __init__(self, idUser, name):
        self.idUser = idUser
        self.name = name
        self.accounts = MaxHeap.AccountsMaxHeap()
        # Stores all the accounts of the user in a MaxHeap, the order criteria is how many times an account is used

    def __str__(self):
        return '{:<10s} {:<15s} {:<20}'.format(self.idUser, self.name, "No. of accounts: " + str(len(self.accounts)))

    def __hash__(self):
        return hash(self.idUser)

    def getId(self):
        return self.idUser

    # Add an account into the accounts MaxHeap
    def addAccount(self, account):
        self.accounts.insertAccount(account)

    # Remove an account that is in the MaxHeap
    def removeAccount(self, idAccount):
        self.accounts.removeAccount(idAccount)

    # Increase the number of how many times the account is used
    def useAccount(self, idAccount):
        self.accounts.increaseKey(idAccount)
    
    # To make a transaction between one of this user's accounts with another
    def makeTransaction(self, accountO, accountD, qty):
        result = accountO.addEdge(accountD, qty)
        if result:
            self.accounts.increaseKey(accountO.getId())
        return result
    
    def getOrderedAccounts(self):
        accs = self.accounts.getHeapList()
        accs = [x.getId() for x in accs if x is not None]
        accs = sorted(accs, key = lambda x: int(x[1:]))
        return accs

    # To print al accounts
    def printAccounts(self):
        print('{:<10s} {:<5s} {:<1s} {:>11s} {:<15}'.format("Account ID", "Type", " ", "Amount" , "\tOwner"))
        print(self.accounts)
    
    # To print al transactions
    def printTransactions(self):
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
        

# Account class is an object of user which will be call by the main module
# Accounts are stored in a hash table
class Account:
    def __init__(self, idAccount, userID, accType, balance = 0):
        self.idAccount = idAccount
        self.userID = userID
        self.frequency = 0
        self.balance = balance
        self.accType = accType
        self.edges = MinHeap.EdgesMinHeap()
        self.pointingAtMe = []

    def __str__(self):
        return '{:<10s} {:<5c} {:<1s} {:>11s} {:<15} {:<15}'.format(self.idAccount, self.accType, "$", str(self.balance) , "\tOwner: " + self.userID, "Frequency: " + str(self.frequency))

    def __hash__(self):
        return hash(self.idAccount)

    def getId(self):
        return self.idAccount

    # Add a transaction between the origin and destination
    def addEdge(self, dest, quantity):

        myEdge = self.edges.getEdge(dest)

        if self.accType == 'D' and self.balance-quantity < 0: # If operation can't be made because of debit with innuficient funds
            print("Not enough funds in account " + self.idAccount + " to transfer " + str(quantity) + " to " + dest.idAccount)
            return False
        elif dest.accType == 'C' and dest.userID != self.userID:
            print("Can't transfer to a 3rd's credit account from " + self.idAccount + " to " + dest.idAccount + " the quantity " + str(quantity))
            return False
        else:
            removed = ()
            if self.edges.getTotalEdges() == 15:
                removed = self.edges.removeOldest()

            print("Transfering $" + str(quantity) + " from " + self.idAccount + " to " + dest.idAccount)
            self.balance -= quantity
            dest.balance += quantity

            if myEdge is not None: # Add to edge is exists
                myEdge.add(quantity)
            else: # Create new edge
                newEdge = Edge(dest, 0)
                newEdge.add(quantity)
                self.edges.insertEdge(newEdge)

            if removed:
                t, m = removed
                dest.pointingAtMe.remove([self, m])
            dest.pointingAtMe.append([self, quantity])

            return True
    
    def getEdgesList(self):
        return [edge.dest for edge in self.edges.getHeapList() if edge is not None]

    def getEdgesListFull(self):
        return [edge for edge in self.edges.getHeapList() if edge is not None]
            
class Edge:

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
        return self.dest

    # Add money and time into the transaction
    def add(self, quantity):
        self.quses.enqueue(time.time())
        self.money.enqueue(quantity)
        self.uses += 1

    # Remove money and time of the oldest transaction
    def removeO(self):
        self.uses -= 1
        return self.quses.dequeue(), self.money.dequeue()

    # To know if the size is empty
    def isEmpty(self):
        return self.uses == 0
    
    # To see top of queue
    def seeOldestTime(self):
        return self.quses.first()

class Queue:
    def __init__(self):
        self.queue = []
    
    def __len__(self):
        return len(self.queue)

    def dequeue(self):
        return self.queue.pop(0)

    def enqueue(self, element):
        self.queue.append(element)
        return

    def first(self):
        return self.queue[0]

    def getArray(self):
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



