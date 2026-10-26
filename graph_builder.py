import random

"""
graph_builder.py

    -build edge list
    -convert edge list to adj list
    -convert edge list to adj matrix

"""

INF = float('inf')

"""
builds directed positively weighted graph as an edge list

params
    (1) n: int
            -number of vertices, 0 to n-1.
    
    (2) family: string
            -random or local
    
    (3) edge_density: float
            -density between 1 and 0
                random: prob for edge u->v existing
                local:  prob of edges to nearby vertices
    
    (4,5) w_min,w_max: int
            -inclusive range of pos edge weights
    
    (6) strongly_connected: bool
            -if true, adds backbone cycle through all vertices first

    (7) seed: int||None
            -random seed for reproducing

returns
    edges: list[tuple[int, int, int]]
        -list of (u, v, w) weighted directed edges

"""
def build_edge_list(
    n,
    w_min=1,
    w_max=20,
    seed=None,
    family="random",
    edge_density=0.1,
    strongly_connected=False,
    ):

    rand = random.Random(seed)
    edge_map = {}#(u, v)-> w

    def add_edge(u, v):
        if u == v: return
        if (u, v) not in edge_map:
            edge_map[(u, v)] = rand.randint(w_min, w_max)

    #backbone cycle, makes the graph more connected
    if strongly_connected and n >= 2:
        for u in range(n):
            v = (u + 1) % n
            add_edge(u, v)

    if family == "random":
        #every possible directed edge appears with probability edge_density
        for u in range(n):
            for v in range(n):
                if u != v and rand.random() < edge_density: add_edge(u, v)

    elif family == "local":
        #each vertex mostly connects to nearby indices
        #window size from n
        local_window = max(1, n // 8)

        for u in range(n):
            left = max(0, u - local_window)
            right = min(n - 1, u + local_window)

            for v in range(left, right + 1):
                if u != v and rand.random() < edge_density: add_edge(u, v)

    else: raise ValueError("family must = random or local")

    edges = [(u, v, w) for (u, v), w in edge_map.items()]
    return edges

###############################################
def edge_list_to_adj_list(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges: adj[u].append((v, w))
    return adj

def print_adj_list(adj, cell_width=8):
    print("\nadj list:")
    left_margin = "     "
    print()

    print(f"{left_margin}{'vertex':<{cell_width}} outgoing edges")
    print(f"{left_margin}{'-' * (cell_width-1)}  {'-' * 15}")

    for row_idx, neighbors in enumerate(adj):
        if not neighbors: neighbor_text = "[]"
        else:
            parts = []
            for v, w in neighbors: parts.append(f"({v}, {w})")
            neighbor_text = "  ".join(parts)

        print(f"{left_margin}{row_idx:<{cell_width}}  {neighbor_text}")

##############################################
def edge_list_to_matrix(n, edges, inf=INF):
    mat = [[inf] * n for _ in range(n)]
    for i in range(n): mat[i][i] = 0

    for u, v, w in edges:
        if w < mat[u][v]: mat[u][v] = w

    return mat

def print_matrix(mat, cell_width=6):
    print("\nadj matrix:")
    print()
    n = len(mat)
    top_border=""

    for i in range(cell_width*n): top_border+="-"
    header = " " * cell_width
    for col in range(n):
        header += f" {col:<{cell_width-1}}"
    
    print(header+"\n      *"+top_border)
    for row_idx, row in enumerate(mat):
        line = f"{row_idx:>{cell_width}}|"

        for x in row:
            if x == INF: cell = "INF"
            else: cell = str(x)
            line += f"{cell:<{cell_width}}"

        print(line)


