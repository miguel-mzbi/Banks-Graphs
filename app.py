import nodes
import bankhash

accountsHash = bankhash.BankHash()
usersHash = bankhash.BankHash()

def newUser(id, name):
    u = nodes.User(id, name)
    usersHash.put(u)
    return u

def deleteUser(id):
    u = usersHash.delete(id)
    return u

def getUser(id):
    u = usersHash.get(id)
    return u

def newAccount(id, userId, aType, balance):
    u = getUser(userId)
    a = nodes.Account(id, userId, aType, balance)
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

def makeTransaction(userID, accountID, destinationID, qty):
    u = getUser(userID)
    o = getAccount(accountID)
    d = getAccount(destinationID)
    result = u.makeTransaction(o, d, qty)
    return result

def printUsers():
    print(usersHash)
    return

def printAccounts():
    print(accountsHash)
    return



def main():
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

    print()
    printAccounts()
    U1.printAccounts()

    A2 = getAccount("A2")
    for o, m in A2.pointingAtMe:
        print(o.getId() + " " + str(m))

if __name__ == '__main__':
    main()

