import Nodes
import BankHash
import GraphOperations
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
import networkx as nx
import names

Arc = namedtuple('Arc', ('tail', 'weight', 'head'))
accountsHash = BankHash.BankHash()
usersHash = BankHash.BankHash()

def getEdgesAsArcs(trueValues = False):
    arcs = []
    accounts = accountsHash.getAll()
    for account in accounts:
        edges = account.getEdgesListFull()
        for edge in edges:
            if trueValues:
                arcs.append(Arc(account.idAccount, edge.uses, edge.dest.idAccount))
            else:
                arcs.append(Arc(account.idAccount, -edge.uses, edge.dest.idAccount))
    return arcs

def newUser(id, name):
    u = Nodes.User(id, name)
    usersHash.put(u)
    return u

def deleteUser(id):
    u = usersHash.delete(id)
    return u

def getUser(id):
    u = usersHash.get(id)
    return u

def getUserRandom():
    return usersHash.getRandomItem()

def newAccount(id, userId, aType, balance):
    u = getUser(userId)
    a = Nodes.Account(id, userId, aType, balance)
    u.addAccount(a)
    accountsHash.put(a)
    return a

def deleteAccount(id):
    a = accountsHash.delete(id)
    u = getUser(a.userID)
    u.removeAccount(a)
    return a

def getAccount(id):
    a = accountsHash.get(id)
    return a

def getAccountRandom():
    return accountsHash.getRandomItem()

def makeTransaction(userID, accountID, destinationID, qty):
    u = getUser(userID)
    o = getAccount(accountID)
    d = getAccount(destinationID)
    result = u.makeTransaction(o, d, qty)
    return result

def DFS(startID):
    return GraphOperations.DephtFS(getAccount(startID))

def BFS(startID):
    return GraphOperations.BreadthFS(getAccount(startID))

def edmonds():
    arcsResult = GraphOperations.edmonds(getEdgesAsArcs(), 'A1')
    arcsToReturn = []
    for i, arc in enumerate(arcsResult.values()):
        arcsToReturn.append(Arc(arc.tail, -arc.weight, arc.head))
    return arcsToReturn

def printUsers():
    print(usersHash)
    return

def printAccounts():
    print(accountsHash)
    return

def updateGraph():
    arcs = getEdgesAsArcs(True)
    plt.ion()
    plt.clf()
    g = nx.DiGraph((x, y, {'weight': w}) for (x, w, y) in arcs)
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, cmap=plt.get_cmap('jet'), node_size = 500)
    nx.draw_networkx_labels(g, pos, font_size=8)
    nx.draw_networkx_edges(g, pos, arrows=True)
    
    plt.pause(.1)    
    plt.show()

def numberToType(n):
    switcher = {
        0: 'C',
        1: 'D'
    }
    return switcher.get(n)

def getRandomUniformInt(end, start = 0):
    return int(np.random.uniform(start, end))

def getRandomNormalAccount(user):
    accs = user.getOrderedAccounts()
    mean = (len(accs)-1)//2
    stddev = len(accs) / 6
    while True:
        i = int(np.random.normal(mean, stddev))
        if 0 <= i < len(accs):
            return accs[i]

def getUsersNum():
    return usersHash.size

def getAccsNum():
    return accountsHash.size
    
def main():

    '''
    newUser("U1", "Miguel")
    U1 = getUser("U1")
    print(str(U1) + "\n")

    newUser("U2", "Luis")
    newUser("U3", "Richie")
    printUsers()

    newAccount("A1", "U1", 'D', 100)
    newAccount("A2", "U2", 'D', 1000)
    newAccount("A3", "U1", 'C', 0)
    newAccount("A4", "U1", 'D', 10)
    newAccount("A5", "U3", 'D', 10000)
    newAccount("A6", "U1", 'D', 100)
    printUsers()
    printAccounts()
    U1.printAccounts()

    makeTransaction("U1", "A1", "A2", 50)
    makeTransaction("U1", "A1", "A2", 50)
    makeTransaction("U1", "A1", "A2", 50)
    makeTransaction("U3", "A5", "A3", 100)
    makeTransaction("U1", "A6", "A2", 5)

    print()
    printAccounts()
    U1.printAccounts()

    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 1)
    makeTransaction("U1", "A3", "A2", 100)
    makeTransaction("U1", "A3", "A2", 200)
    makeTransaction("U1", "A3", "A2", 300)

    makeTransaction("U1", "A2", "A1", 1)

    print()
    printAccounts()
    U1.printAccounts()

    A2 = getAccount("A2")
    for o, m in A2.pointingAtMe:
        print(o.getId() + " " + str(m))

    print()
    print(DFS("A3"))
    print(BFS("A3"))
    print(edmonds())
    '''
    forced = 0
    while True:
        if forced == 0:
            tOperation = getRandomUniformInt(15)
        elif forced == 1:
            tOperation = 13
        elif forced == 2:
            tOperation = 8
            
        if tOperation >= 13: # Make new user
            forced = 0
            print("New User")
            uNum = getRandomUniformInt(1000000)
            while True:
                if getUser("U"+str(uNum)) is None:
                    newUser("U"+str(uNum), names.get_full_name())
                    break
                else:
                    uNum = getRandomUniformInt(1000000)
        elif tOperation >= 8: # Make new acount
            if getUsersNum() < 1:
                print("New Account Impossible. Users: " + str(getUsersNum()))
                forced = 1
                continue
            else:
                forced = 0
            
            print("New Account")
            aNum = getRandomUniformInt(1000000000)
            while True:
                if getAccount("A"+str(aNum)) is None:
                    aType = numberToType(getRandomUniformInt(2))
                    if aType == 'D':
                        aAmount = getRandomUniformInt(100000)
                    else:
                        aAmount = 0
                    newAccount("A"+str(aNum), getUserRandom().getId(), aType, aAmount)
                    break
                else:
                    aNum = getRandomUniformInt(1000000000)
        else: # Make new transaction
            if getUsersNum() < 2:
                print("New Transaction Impossible. Users: " + str(getUsersNum()))
                forced = 1
                continue
            elif getAccsNum() < 2:
                print("New Transaction Impossible. Accs: " + str(getAccsNum()))
                forced = 2
                continue
            else:
                forced = 0

            print("New Transaction")
            
            user = getUserRandom()
            while True:
                if len(user.accounts) > 0:
                    break
                else:
                    user = getUserRandom()
            accOrigin = getRandomNormalAccount(user)
            accDest = getAccountRandom().getId()
            while accOrigin == accDest:
                accDest = getAccountRandom().getId()
            amount = getRandomUniformInt(getAccount(accOrigin).balance, 1) if getAccount(accOrigin).accType == 'D' else getRandomUniformInt(10000, 1)
            makeTransaction(user.getId(), accOrigin, accDest, amount)
        
        updateGraph()

    while True:
        plt.pause(0.5)
    

if __name__ == '__main__':
    main()

