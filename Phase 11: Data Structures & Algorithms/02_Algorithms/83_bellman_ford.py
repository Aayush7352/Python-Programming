from typing import Dict, List, Tuple, Optional


def bellman_ford(
    vertices: List[str],
    edges: List[Tuple[str, str, float]],
    start: str
) -> Tuple[Dict[str, float], Dict[str, Optional[str]], bool]:
    """Bellman-Ford algorithm for shortest paths.

    Handles negative edge weights and detects negative cycles.
    Returns: (distances, predecessors, has_negative_cycle)
    """
    distances = {v: float("inf") for v in vertices}
    distances[start] = 0
    predecessors = {v: None for v in vertices}

    # Relax edges |V| - 1 times
    for _ in range(len(vertices) - 1):
        relaxed = False
        for u, v, weight in edges:
            if distances[u] != float("inf") and \
               distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                predecessors[v] = u
                relaxed = True
        if not relaxed:
            break

    # Check for negative cycles
    for u, v, weight in edges:
        if distances[u] != float("inf") and \
           distances[u] + weight < distances[v]:
            return distances, predecessors, True  # negative cycle found

    return distances, predecessors, False


def shortest_path(predecessors: Dict[str, Optional[str]],
                  target: str) -> List[str]:
    """Reconstruct shortest path."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    return list(reversed(path))


def main():
    print("=== Bellman-Ford Algorithm ===")
    print("  Handles negative edge weights\n")

    vertices = ["A", "B", "C", "D", "E"]
    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 3),
        ("B", "D", 2),
        ("B", "E", 3),
        ("C", "B", 1),
        ("C", "D", 4),
        ("D", "E", 1),
    ]

    distances, predecessors, has_cycle = bellman_ford(vertices, edges, "A")
    print("  Graph with positive weights:")
    print(f"  Negative cycle: {has_cycle}")
    for v in vertices:
        if distances[v] != float("inf"):
            path = shortest_path(predecessors, v)
            print(f"    A -> {v}: dist={distances[v]}, path={' -> '.join(path)}")

    print("\n=== Graph with Negative Edges ===")
    neg_edges = [
        ("A", "B", 1),
        ("A", "C", 4),
        ("B", "C", -3),  # negative edge
        ("B", "D", 2),
        ("C", "D", 1),
    ]

    distances, predecessors, has_cycle = bellman_ford(vertices, neg_edges, "A")
    print(f"  Negative cycle: {has_cycle}")
    for v in vertices:
        if distances[v] != float("inf"):
            path = shortest_path(predecessors, v)
            print(f"    A -> {v}: dist={distances[v]}, path={' -> '.join(path)}")
        else:
            print(f"    A -> {v}: unreachable")

    print("\n=== Graph with Negative Cycle ===")
    cycle_edges = [
        ("A", "B", 1),
        ("B", "C", -1),
        ("C", "A", -1),  # creates negative cycle
        ("B", "D", 2),
    ]

    distances, predecessors, has_cycle = bellman_ford(vertices, cycle_edges, "A")
    print(f"  Negative cycle detected: {has_cycle}")

    if has_cycle:
        print("  (Bellman-Ford correctly detects negative cycles)")
        print("  Shortest paths are undefined with negative cycles")

    print("\n=== Edge Relaxation Steps ===")
    print("  Step 1: Initialize distances[start] = 0")
    print("  Step 2: Relax all edges |V| - 1 times")
    print("  Step 3: Check for negative cycles")

    # Real-world analogy: currency arbitrage
    print("\n=== Currency Arbitrage Example ===")
    currencies = ["USD", "EUR", "GBP", "JPY"]
    rates = [
        ("USD", "EUR", 0.85),  # 1 USD = 0.85 EUR
        ("EUR", "USD", 1.18),
        ("EUR", "GBP", 0.88),
        ("GBP", "EUR", 1.14),
        ("GBP", "JPY", 150.0),
        ("JPY", "GBP", 0.0067),
        ("USD", "JPY", 110.0),
        ("JPY", "USD", 0.0091),
    ]

    # Use negative log to find arbitrage opportunities
    import math
    log_edges = [(u, v, -math.log(rate)) for u, v, rate in rates]

    distances, _, has_cycle = bellman_ford(currencies, log_edges, "USD")
    print(f"  Arbitrage opportunity: {has_cycle}")

    print("\n=== Bellman-Ford Properties ===")
    print("  - Handles negative edge weights")
    print("  - Detects negative cycles")
    print("  - Time: O(V * E)")
    print("  - Space: O(V)")
    print("  - Slower than Dijkstra but more general")


if __name__ == "__main__":
    main()
