 # __Algorithms Project__ 

<p> Miguel Montoya </p>
<p> Luis Vargas </p>
<p> Ricardo Palma </p>

Nowadays, it is normal that people are connected between each other by any means possible. Social Networks such as Facebook and Twitter, between more, have proven that people are closer with others more than they know. But how do they keep track of how is a person connected with another? The purpose of this problem is to elaborate a time-efficient algorithm that can keep track of the relation between an user’s belongings and the ones from another user. This, with the objective of a user having a faster interaction with the quality enhanced interface. As an application of this algorithm, the project will simulate the interaction of a user and his accounts as a member of a certain bank. As a member of this bank, the user can use his accounts to withdraw, deposit or transfer any money. When a user does this, a relation is created. This is where the algorithm boosts the way this relationships are kept. In such way that an account is used more often than any other, it is prioritized in such way that the user can access to it faster than before. Then again, when a transfer is done by a user to another user, the algorithm creates and keeps track of this movement for future references. In this way, it can enhance the quality of the interface that banks such as Santander, Bancomer and Banamex offers to the user. So, that it makes this app work faster for the user and this influences him for a more positive feedback to the bank.

### __System functional requirements__
- The system needs to implement the insertion of different type of accounts (credit or debit) for a user.
- Insertion of new users that do not have an account.
- Insertion of cashiers inside an account in name of the Bank that counts as an user.
- Delete any kind of account such as a cashier or an user account.
- Search for a user's accounts and for a specific account.
- Insertion of relationships between accounts such as deposit, withdraw, transfer from a user account and deposit or withdraw from a cashier.
- Delete relationships between accounts.


### __The use of the algorithms__

Through the elaboration of the project, the following algorithms & Data Structures were implemented: 

- Breadth First Search (BFS) & Depth First Search (DFS)
>To traverse the nodes of the graph. If we are more interested in the closest first, we use BFS. If we are more interested in the furthest we can get, we use DFS.

- Edmond’s (Analog of Prim’s but for directed graphs)
>We can use Edmons’s algorithm to get the spanning arborescence (minimum spanning tree) of the graph. This would mean, to use a unique relation to traverse all the nodes.

- Hashing
> Simple for the clients’ id and the accounts’ id. Necessary for insertion in both hash tables.

- Heapsort
>To sort the accounts that belong to a client. Keeping the account that’s been used the most as heap.

- Queue
> In order to keep track of the 15 most recent relations an account had. When a movement happens from an account into another, that movement is enqueued, so that a relation between both accounts involved is stored. If the queue is already full, the oldest movement is dequeued in order to enqueue the most recent one. 

### __Complexities__

With the description of the algorithms implemented in the software, the following complexities are given when running it:

Action | Average Case | Worst Case
:---:|:----:|:----:
Create New User | θ(1) | O(U)
Search User | θ(1) | O(U)
Delete User | θ(1) | O(U)
Create New Account | θ(1) | O(U+A+log(A))
Search Account | θ(1) | O(A)
Delete Account | θ(1+log(A)) | O(U+A+log(A))
Make Transaction | θ(1) | O(U+2A+log(A))
Search Transaction(DFS) | θ(1+A+T) | O(2A+T)
Search Transaction(BFS) | θ(1+A+T) | O(2A+T)
Edmond's | θ(A+A^2+T) | O(A+A^2+T)

_NOTE:
A= Accounts     U= Users     T= Transactions (T has a constant value of 15 as maximum)_

### __Functionality__

First of all, a couple of assumptions were made in order to cover some functionalities of the software. One of them is that the Bank is an User, and Cashiers work as debit accounts of such Bank. In order to keep money flowing through the bank, the National Bank automatically gives more cash to the bank when it’s balance reaches $0. The cashiers are not related with other cashiers at all and they only receive relations; therefore, it will never be the origin of a relation, only the destiny. As mentioned before, only the 15 most recent relations between accounts are stored. The deposits and withdrawals from a Cashier are special. Deposit means that both the Account and the Cashier increase the balance amount. In addition, a Withdrawal means that the balance will decrease for both the Account and the Cashier. Finally,  The relations between Owners and the Accounts are not stored in the adjacency table instead they are stored in the Hash Table and their corresponding trees. 
