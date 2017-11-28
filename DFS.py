def DFS(source, start): # Source -> Accounts
    Adjacents = source.getEdgesList()
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(source[vertex] - visited)
    return visited
