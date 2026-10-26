import heapq
"""
algorithms.py

"""

INF = float('inf')
"""
https://www.geeksforgeeks.org/dsa/floyd-warshall-algorithm-in-python/

floyd_warshall(graph)

# Solves the all-pairs shortest path
# problem using Floyd Warshall algorithm

params
    (1) graph: list[list[float || int]]
            adj/distance matrix:
            -graph[i][j] = edge weight  if edge i to j exist
            -graph[i][j] = info         if no edge exists
            -graph[i][i] = 0

returns
    dist: list[list[float || int]]
        -shortest path distance matrix

"""
def floyd_warshall(graph):

    V = len(graph)

    #copy of input matrix, g4g version modifies input matrix directly, this is a NONO
    dist = [row[:] for row in graph]

    # Add all vertices one by one to
    # the set of intermediate vertices.
    for k in range(V):
        
        # Pick all vertices as source one by one
        for i in range(V):
            

            # Pick all vertices as destination
            # for the above picked source
            for j in range(V):#pick each vertex as a source

                # If vertex k is on the shortest path from
                # i to j, then update the value of graph[i][j]

                #no edge = INF, g4g no edge = -1
                if dist[i][k] != INF and dist[k][j] != INF:

    
                    #g4g version:
                    #   if ((graph[i][j] == -1 or graph[i][j] > graph[i][k] + graph[k][j])
                    #       and (graph[k][j] != -1 and graph[i][k] != -1)):
                    if dist[i][j] > dist[i][k] + dist[k][j]:

                        dist[i][j] = dist[i][k] + dist[k][j]
    
    #finished distance matrix
    return dist


"""
https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/

params
    (1) adj:list[list[tuple[int, int]]]
            -adj list, adj[u] contains (v, w) pairs
    (2) src:int
            -source vertex

Returns
    dist:list[float || int]
        -dist[v] = shortest path dist from src to v
"""
def djikstra(adj, src):


    V = len(adj)
    # Min-heap (priority queue) storing pairs of (distance, node)   
    pq = []#priority queue

    # Distance from source to itself is 0
    dist = [INF] * V

    dist[src] = 0
    heapq.heappush(pq, (0, src))

    # Process the queue until all reachable vertices are finalized
    while pq:
        d, u = heapq.heappop(pq)
        # If this distance not the latest shortest one, skip it
        if d > dist[u]:
            continue
        # Explore all neighbors of the current vertex
        for v, w in adj[u]:
            # If we found a shorter path to v through u, update it
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    # Return the final shortest distances from the source

    return dist