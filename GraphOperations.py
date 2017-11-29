
def DephtFS(start):
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


from collections import defaultdict

def edmonds(arcs, sink):
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


#print(min_spanning_arborescence([Arc(1, 17, 0), Arc(2, 16, 0), Arc(3, 19, 0), Arc(4, 16, 0), Arc(5, 16, 0), Arc(6, 18, 0), Arc(2, 3, 1), Arc(3, 3, 1), Arc(4, 11, 1), Arc(5, 10, 1), Arc(6, 12, 1), Arc(1, 3, 2), Arc(3, 4, 2), Arc(4, 8, 2), Arc(5, 8, 2), Arc(6, 11, 2), Arc(1, 3, 3), Arc(2, 4, 3), Arc(4, 12, 3), Arc(5, 11, 3), Arc(6, 14, 3), Arc(1, 11, 4), Arc(2, 8, 4), Arc(3, 12, 4), Arc(5, 6, 4), Arc(6, 10, 4), Arc(1, 10, 5), Arc(2, 8, 5), Arc(3, 11, 5), Arc(4, 6, 5), Arc(6, 4, 5), Arc(1, 12, 6), Arc(2, 11, 6), Arc(3, 14, 6), Arc(4, 10, 6), Arc(5, 4, 6)], 0))