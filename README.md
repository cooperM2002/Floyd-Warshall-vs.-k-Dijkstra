# Floyd-Warshall-vs.-k-Dijkstra
A brief investigation into the $k$-source minimum cost path problem focused on comparing various performance metrics of Floyd-Warshall &amp; $k$-runs of Dijkstra.

### Problem:

Given an edge-weighted directed graph $G$ with no negative-cost edges and a set $S$ = { $\{s_1, s_2, \ldots, s_k\}$ } of $k$ starting vertices, construct minimum-cost path trees for each vertex in $S$.

### Investigated Conjecture:

Even for relatively small values of $k$, the Floyd-Warshall-Roy algorithm will provide better performance in practice for the $k$-source minimum-cost path problem than $k$ runs of Dijkstra’s algorithm (regardless of the asymptotic running times).

### Inlcuded in this repo:

- `algorithms.py` Floyd-Warshall and Dijkstra implementations
- `graph_builder.py` Graph generation and adjacency list/matrix conversion
- `main.py` Runtime benchmarking and correctness checks
- `results.csv` Raw experiment results
- `results.xlsx` Results spreadsheet
- `results.pdf` Results exported as a PDF
- `mcp_coopermartin.pdf` Written investigation and conclusions
