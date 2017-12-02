'''
App.py is the main module of the project. It contains all of the basic functions.
It also contains the demo and random generator to see the evolution.
In complexities: A = Accounts, T = Transactions, U = Users
'''

from collections import namedtuple

import matplotlib.pyplot as plt
import names
import networkx as nx
import numpy as np

import BankHash
import GraphOperations
import Nodes

Arc = namedtuple('Arc', ('tail', 'weight', 'head'))
accountsHash = BankHash.BankHash()
usersHash = BankHash.BankHash()

def newUser(uId, name):
    '''
    Creates a new user. It's added to the user's hashtable.
    Complexity: O(U)
    '''
    user = Nodes.User(uId, name)
    usersHash.put(user)
    return user

def deleteUser(uId):
    '''
    Deletes an user in the user's hashtable.
    Complexity: O(U)
    '''
    user = usersHash.delete(uId)
    return user

def getUser(uId):
    '''
    Searches an user in the user's hashtable.
    Complexity: O(U)
    '''
    return usersHash.get(uId)

def getUserRandom():
    '''
    Gets a random user from the hashtable.
    Complexity: O(U)
    '''
    return usersHash.getRandomItem()

def getUsersNum():
    '''
    Gets user's hashtable size
    Complexity: O(1)
    '''
    return usersHash.size

def printUsers():
    '''
    Prints all the existing users with data
    Complexity: O(U)
    '''
    print(usersHash)
    return

def newAccount(aId, userId, aType, balance):
    '''
    Creates a new account. It's added to the account's hashtable.
    First it searches the user object to assign this new account.
    Then the account is added to the user's maxheap.
    Complexity: O(U + A + log(A))
    '''
    user = getUser(userId)
    account = Nodes.Account(aId, userId, aType, balance)
    user.addAccount(account)
    accountsHash.put(account)
    return account

def deleteAccount(aId):
    '''
    Deletes an account. It's it's removed from account's hashtable.
    First it searches the user object to delete this account.
    Then the account is removed from the user's maxheap.
    Complexity: O(U + A + log(A))
    '''
    account = accountsHash.delete(aId)
    user = getUser(account.userID)
    user.removeAccount(account)
    return account

def getAccount(aId):
    '''
    Searches an account in the account's hashtable.
    Complexity: O(A)
    '''
    return accountsHash.get(aId)

def getAccountRandom():
    '''
    Gets a random account from the hashtable.
    Complexity: O(A)
    '''
    return accountsHash.getRandomItem()

def getAccsNum():
    '''
    Gets user's hashtable size
    Complexity: O(1)
    '''
    return accountsHash.size

def printAccounts():
    '''
    Prints all the existing accounts with data
    Complexity: O(A)
    '''
    print(accountsHash)
    return

def makeTransaction(userID, accountID, destinationID, qty):
    '''
    Makes a new transaction beetween accounts.
    First it searches the user that is making the transaction in the user's hashtable.
    Then it searches both the origin and destination account in the account's hashtable.
    Finally it makes the transaction (Increasing the keay in the heap).
    Complexity: O(U + 2A + log(A))
    '''
    user = getUser(userID)
    origin = getAccount(accountID)
    destiny = getAccount(destinationID)
    return user.makeTransaction(origin, destiny, qty)

def DFS(startID):
    '''
    Returns the DFS of the graph. It first searches the the account in the hashtable.
    Complexity: O(2A + T)
    '''
    return GraphOperations.DephtFS(getAccount(startID))

def BFS(startID):
    '''
    Returns the BFS of the graph. It first searches the the account in the hashtable.
    Complexity: O(2A + T)
    '''
    return GraphOperations.BreadthFS(getAccount(startID))

def edmonds():
    '''
    Returns the maximum spanning tree of the graph.
    It uses the minimum spanning tree's logic, but with the negated weights, to obtain the maximum.
    Complexity: O(A + A^2 + T)
    '''
    arcsResult = GraphOperations.edmonds(getEdgesAsArcs(), 'A1')
    arcsToReturn = []
    for i, arc in enumerate(arcsResult.values()):
        arcsToReturn.append(Arc(arc.tail, -arc.weight, arc.head))
    return arcsToReturn

def getEdgesAsArcs(trueValues=False):
    '''
    Function that obtains all of the edges in the graph
    It's used to draw the graph.
    Uses arcs tuplet
    Complexity: O(A + T)
    '''
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

def updateGraph():
    '''
    Plots the graph
    '''
    arcs = getEdgesAsArcs(True)
    plt.ion()
    plt.clf()
    g = nx.DiGraph((x, y, {'weight': w}) for (x, w, y) in arcs)
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, cmap=plt.get_cmap('jet'), node_size=500)
    nx.draw_networkx_labels(g, pos, font_size=8)
    nx.draw_networkx_edges(g, pos, arrows=True)
    plt.pause(.5)
    plt.show()
    return

def numberToType(n):
    '''
    Swich-type-dictionary
    Complexity: O(1)
    '''
    switcher = {
        0: 'C',
        1: 'D'
    }
    return switcher.get(n)

def getRandomUniformInt(end, start = 0):
    '''
    Generates a random int using a uniform distribution
    Complexity: O(1)
    '''
    return int(np.random.uniform(start, end))

def getRandomNormalAccount(user):
    '''
    Gets a random account of an user, using a normal distribution.
    Complexity: O(alpha)
    '''
    accs = user.getOrderedAccounts()
    mean = (len(accs)-1)//2
    stddev = len(accs) / 6
    while True:
        i = int(np.random.normal(mean, stddev))
        if 0 <= i < len(accs):
            return accs[i]
    return

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
        elif forced == 1: # Forced to create user
            tOperation = 13
        elif forced == 2: # Forced to create account
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
