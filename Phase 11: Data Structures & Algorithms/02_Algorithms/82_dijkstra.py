import heapq
import math
from typing import Dict, List, Tuple, Optional


def dijkstra(graph: Dict[str, List[Tuple[str, float]]],
             start: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """Dijkstra's algorithm for shortest paths from start."""
    distances = {vertex: float("inf") for vertex in graph}
    distances[start] = 0
    predecessors = {vertex: None for vertex in graph}
    pq = [(0, start)]
    visited = set()

    while pq:
        current_dist, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)

        for neighbor, weight in graph[current]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))

    return distances, predecessors


def shortest_path(predecessors: Dict[str, Optional[str]],
                  target: str) -> List[str]:
    """Reconstruct shortest path from predecessors."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    return list(reversed(path))


def dijkstra_grid(grid: List[List[int]], start: Tuple[int, int],
                  end: Tuple[int, int]) -> Tuple[float, List[Tuple[int, int]]]:
    """Dijkstra on a grid (0=open, positive=weight/cost)."""
    rows, cols = len(grid), len(grid[0])
    distances = {(r, c): float("inf") for r in range(rows) for c in range(cols)}
    distances[start] = 0
    predecessors = {}
    pq = [(0, start[0], start[1])]
    visited = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while pq:
        dist, r, c = heapq.heappop(pq)
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if (r, c) == end:
            break

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] < float("inf"):
                cost = grid[nr][nc]
                new_dist = dist + cost
                if new_dist < distances[(nr, nc)]:
                    distances[(nr, nc)] = new_dist
                    predecessors[(nr, nc)] = (r, c)
                    heapq.heappush(pq, (new_dist, nr, nc))

    # Reconstruct path
    path = []
    if distances[end] < float("inf"):
        current = end
        while current in predecessors:
            path.append(current)
            current = predecessors[current]
        path.append(start)
        path.reverse()

    return distances[end], path


def main():
    print("=== Dijkstra's Algorithm ===")
    graph = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 1), ("D", 5)],
        "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
        "D": [("B", 5), ("C", 8), ("E", 2), ("F", 6)],
        "E": [("C", 10), ("D", 2), ("F", 3)],
        "F": [("D", 6), ("E", 3)],
    }

    distances, predecessors = dijkstra(graph, "A")
    print("  Shortest distances from A:")
    for v, d in sorted(distances.items()):
        path = shortest_path(predecessors, v)
        print(f"    A -> {v}: distance={d}, path={' -> '.join(path)}")

    print("\n=== Dijkstra on Grid ===")
    grid = [
        [1, 1, 5, 1, 1],
        [1, 9, 9, 1, 1],
        [1, 1, 1, 5, 1],
        [9, 9, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]
    dist, path = dijkstra_grid(grid, (0, 0), (4, 4))
    print(f"  Shortest distance: {dist}")
    print(f"  Path: {path}")

    # Negative edge demonstration
    print("\n=== Dijkstra Limitation: Negative Edges ===")
    neg_graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", -3), ("D", 2)],  # Negative edge!
        "C": [("D", 1)],
        "D": [],
    }
    distances, _ = dijkstra(neg_graph, "A")
    print(f"  From A (may be incorrect with negative edges): {distances}")
    print("  Bellman-Ford handles negative edges instead")

    # Performance comparison
    print("\n=== Performance ===")
    import time, random
    big_graph = {}
    for i in range(1000):
        big_graph[str(i)] = []
    for i in range(1000):
        for _ in range(5):
            j = random.randint(0, 999)
            if j != i:
                big_graph[str(i)].append((str(j), random.random() * 10))

    start = time.perf_counter()
    distances, _ = dijkstra(big_graph, "0")
    elapsed = time.perf_counter() - start
    print(f"  Dijkstra on 1000-node graph: {elapsed:.4f}s")

    print("\n=== Dijkstra Properties ===")
    print("  - Finds shortest paths in weighted graphs")
    print("  - Time: O((V+E) log V) with binary heap")
    print("  - Works only with non-negative weights")
    print("  - Greedy algorithm")
    print("  - Used in GPS, network routing")


if __name__ == "__main__":
    main()
