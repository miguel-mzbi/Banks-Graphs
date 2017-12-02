'''
Utility operations for the graph operations
'''

from collections import defaultdict

def DephtFS(start):
    '''
    Does a DFS.
    Complexity: O(A + T)
    '''
    visited = []
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            print(vertex)
            visited.append(vertex)
            edges = vertex.getEdgesList()
            stack.extend([item for item in edges if item not in visited])
    return visited

def BreadthFS(start):
    '''
    Does a BFS.
    Complexity: O(A + T)
    '''
    visited = []
    queue = [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            print(vertex)
            visited.append(vertex)
            edges = vertex.getEdgesList()
            queue.extend([item for item in edges if item not in visited])
    return visited

def edmonds(arcs, sink):
    '''
    Does a MST of a directed graph using Edmond's algorithm.
    Complexity: O(A^2 + T)
    '''
    goodArcs = []
    quotientMap = {arc.tail: arc.tail for arc in arcs}
    quotientMap[sink] = sink

    while True:
        minArcByTailRep = {}
        successorRep = {}

        for arc in arcs:
            if arc.tail == sink:
                continue
            tailRep = quotientMap[arc.tail]
            headRep = quotientMap[arc.head]
            if tailRep == headRep:
                continue
            if tailRep not in minArcByTailRep or minArcByTailRep[tailRep].weight > arc.weight:
                minArcByTailRep[tailRep] = arc
                successorRep[tailRep] = headRep

        cycleReps = findCycle(successorRep, sink)

        if cycleReps is None:
            goodArcs.extend(minArcByTailRep.values())
            return spanningArborescence(goodArcs, sink)

        goodArcs.extend(minArcByTailRep[cycle_rep] for cycle_rep in cycleReps)
        cycleRepSet = set(cycleReps)
        cycle_rep = cycleRepSet.pop()
        quotientMap = {node: cycle_rep if node_rep in cycleRepSet else node_rep for node, node_rep in quotientMap.items()}


def findCycle(successor, sink):
    '''
    Finds cycles
    '''
    visited = {sink}
    for node in successor:
        cycle = []
        while node not in visited:
            visited.add(node)
            cycle.append(node)
            node = successor[node]
        if node in cycle:
            return cycle[cycle.index(node):]

    return None


def spanningArborescence(arcs, sink):
    '''
    Arborescence
    '''
    arcsByHead = defaultdict(list)

    for arc in arcs:
        if arc.tail == sink:
            continue
        arcsByHead[arc.head].append(arc)

    solutionArcByTail = {}
    stack = arcsByHead[sink]

    while stack:
        arc = stack.pop()
        if arc.tail in solutionArcByTail:
            continue
        solutionArcByTail[arc.tail] = arc
        stack.extend(arcsByHead[arc.tail])

    return solutionArcByTail
