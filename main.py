import statistics
import random
import time
import csv

from graph_builder import *
from algorithms import *
"""
main.py
"""



"""
##########
SOURCE SET 
##########
"""
#k distinct source vertices from 0,1,...,n-1 
def choose_sources(n, k, seed=None):
    """choose distinct source vertices from 0,1,...,n-1"""
    if k > n: raise ValueError("k cannot be larger than n")
    rng = random.Random(seed)
    return rng.sample(range(n), k)


"""
##################
DJIKSTRA functions
##################
"""
#djikstra wrapper
#run djikstra for each sourcem fill result dict
def run_k_djikstras(adj, sources):
    results = {}
    for src in sources: #djikstra once for each source
        results[src] = djikstra(adj, src)#results{key=srcvertex, value=dist from src}

    return results


#k djikstra wrapper
def time_k_djikstras(adj, sources):
    """total elapsed time for running djikstra once per src v"""
    start   = time.perf_counter()
    results = run_k_djikstras(adj, sources)
    end     = time.perf_counter()
    elapsed = end - start

    return elapsed, results


def repeated_time_k_djikstras(adj, sources, repeats=7, warmups=1):
    """repeat k djikstra timings, returns (median_time, all_times, last_results)"""
    #warmup runs
    for _ in range(warmups): run_k_djikstras(adj, sources)

    times = []
    last_results = None

    for _ in range(repeats):
        elapsed, results = time_k_djikstras(adj, sources)
        times.append(elapsed)
        last_results = results

    return statistics.median(times), times, last_results


def print_djikstra_results(results):
    print("\ndjikstra results:")
    for src, dist in results.items():
        display_row = []
        for x in dist:
            if x == INF: display_row.append("INF")
            else: display_row.append(str(x))
        print(f"\tsource {src}: {display_row}")



"""
########################
FLOYD WARSHALL functions
########################
"""
#floyd warshall wrapper
def time_floyd_warshall(mat):
    """measure elapsed time for one floyd warshall run"""
    start   = time.perf_counter()
    dist    = floyd_warshall(mat)
    end     = time.perf_counter()
    elapsed = end - start

    return elapsed, dist


def repeated_time_floyd_warshall(mat, repeats=7, warmups=1):
    """repeat floyd warshall timing, returns (median_time, all_times, last_dist)"""
    #warmup runs
    for _ in range(warmups): floyd_warshall(mat)

    times = []
    last_dist = None

    for _ in range(repeats):
        elapsed, dist = time_floyd_warshall(mat)
        times.append(elapsed)
        last_dist = dist

    return statistics.median(times), times, last_dist


"""
################
HELPER functions
################
"""


def verify_results(sources, djikstra_results, fw_dist):
    """check if each djk result row matches corresponding row of fw output"""
    for src in sources:
        if djikstra_results[src] != fw_dist[src]:
            return False
    return True



def print_header():
    print("\nRESULTS")
    print("-" * 120)
    print(
        f"{'n':>6} {'family':>10} {'density':>10} {'k':>6} "
        f"{'g_seed':>8} {'edges':>8} {'act_dens':>10} "
        f"{'dji_med':>12} {'fw_med':>12} {'fw/dji':>10} "
        f"{'winner':>10} {'match':>8}"
    )
    print("-" * 120)



def run_test(
        n_vals, 
        f_vals, 
        ed_vals, 
        k_vals, 
        g_seeds, 
        w_min, 
        w_max, 
        strongly_connected,
        repeats,
        warmups
    ):

    total_cases = 0
    fw_wins = 0
    djikstra_wins = 0
    mismatch_count = 0
    ratio_values = []

    print_header()

    csv_filename = "results.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "n",
            "family",
            "edge_density",
            "k",
            "graph_seed",
            "source_seed",
            "num_edges",
            "actual_density",
            "djikstra_median",
            "fw_median",
            "fw_over_djikstra_ratio",
            "djikstra_per_source",
            "winner",
            "match"
        ])

        for n in n_vals:
            for f in f_vals:
                for ed in ed_vals:
                    for k in k_vals:
                        #skip impossible k
                        if k > n: continue
                        for g_seed in g_seeds:
                            #BUILD MAIN GRAPH
                            edges = build_edge_list(
                                n=n,
                                family=f,
                                edge_density=ed,
                                w_min=w_min,
                                w_max=w_max,
                                strongly_connected=strongly_connected,
                                seed=g_seed,
                            )

                            #BUILD ADJACENCY REPRESENTATIONS
                            adj = edge_list_to_adj_list(n, edges)
                            mat = edge_list_to_matrix(n, edges)

                            #use same source set
                            source_seed = 1000 + g_seed + k
                            sources = choose_sources(n, k, seed=source_seed)

                            #K djiKSTRA TIME
                            djikstra_median, djikstra_times, djikstra_results = repeated_time_k_djikstras(
                                adj, sources, repeats=repeats, warmups=warmups
                            )

                            #ONE FLOYD WARSHALL RUN
                            fw_median, fw_times, fw_dist = repeated_time_floyd_warshall(
                                mat, repeats=repeats, warmups=warmups
                            )

                            #VERIFY CORRECT
                            match = verify_results(sources, djikstra_results, fw_dist)

                            #EXTRA METRICS
                            num_edges = len(edges)
                            actual_density = num_edges / (n * (n - 1))
                            fw_over_djikstra_ratio = fw_median / djikstra_median
                            djikstra_per_source = djikstra_median / k
                            winner = "FW" if fw_median < djikstra_median else "djikstra"

                            #OVERALL COUNTS
                            total_cases += 1
                            ratio_values.append(fw_over_djikstra_ratio)

                            if winner == "FW":
                                fw_wins += 1
                            else:
                                djikstra_wins += 1

                            if not match:
                                mismatch_count += 1

                            #ONE SUMMARY ROW
                            print(
                                f"{n:>6} {f:>10} {ed:>10.2f} {k:>6} "
                                f"{g_seed:>8} {num_edges:>8} {actual_density:>10.3f} "
                                f"{djikstra_median:>12.6f} {fw_median:>12.6f} {fw_over_djikstra_ratio:>10.2f} "
                                f"{winner:>10} {str(match):>8}"
                            )

                            #WRITE ONE CSV ROW
                            writer.writerow([
                                n,
                                f,
                                ed,
                                k,
                                g_seed,
                                source_seed,
                                num_edges,
                                actual_density,
                                djikstra_median,
                                fw_median,
                                fw_over_djikstra_ratio,
                                djikstra_per_source,
                                winner,
                                match
                            ])
    print("-" * 120)
    print(f"total cases:      {total_cases}")
    print(f"FW wins:          {fw_wins}")
    print(f"djikstra wins:    {djikstra_wins}")
    print(f"mismatches:       {mismatch_count}")

    if ratio_values:
        print(f"min fw/dji ratio: {min(ratio_values):.2f}")
        print(f"med fw/dji ratio: {statistics.median(ratio_values):.2f}")
        print(f"max fw/dji ratio: {max(ratio_values):.2f}")
    
    print("-" * 120)
    print("DONE")

def main():
    """
    //////////////
    /// CONFIG ///
    //////////////
    """
    #graph settings
    n_vals  = [20, 40, 80, 120]
    f_vals  = ["random", "local"]
    ed_vals = [0.10, 0.25, 0.50]
    #number of sources
    k_values = [1, 2, 4, 8]
    #graph generation settings
    w_min = 1
    w_max = 10
    strongly_connected = True
    #graph seeds
    g_seeds = [10, 20, 30]
    #repeated timing settings
    repeats = 7
    warmups = 1

    """
    ////////////////
    /// RUN TEST ///
    ////////////////
    """
    run_test(
            n_vals, 
            f_vals, 
            ed_vals, 
            k_values, 
            g_seeds, 
            w_min, 
            w_max, 
            strongly_connected,
            repeats,
            warmups
        )

if __name__ == "__main__":
    main()