from collections import defaultdict, deque
from typing import List, Dict, Tuple, Set, Optional


class Graph:
    """Graph implementation using adjacency list."""

    def __init__(self, directed: bool = False):
        self.adjacency = defaultdict(list)
        self.directed = directed

    def add_edge(self, u, v, weight: float = 1.0):
        """Add an edge between u and v with optional weight."""
        self.adjacency[u].append((v, weight))
        if not self.directed:
            self.adjacency[v].append((u, weight))

    def add_vertex(self, vertex):
        """Add a vertex (ensures it exists)."""
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []

    def get_neighbors(self, vertex) -> List[Tuple]:
        return self.adjacency.get(vertex, [])

    @property
    def vertices(self) -> set:
        return set(self.adjacency.keys())

    @property
    def vertex_count(self) -> int:
        return len(self.adjacency)

    def bfs(self, start) -> List:
        """Breadth-first search traversal."""
        visited = set()
        queue = deque([start])
        result = []

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                for neighbor, _ in self.adjacency[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return result

    def dfs(self, start) -> List:
        """Depth-first search traversal."""
        visited = set()
        result = []

        def _dfs(vertex):
            visited.add(vertex)
            result.append(vertex)
            for neighbor, _ in self.adjacency[vertex]:
                if neighbor not in visited:
                    _dfs(neighbor)

        _dfs(start)
        return result

    def dijkstra(self, start) -> Dict:
        """Dijkstra's shortest path algorithm."""
        import heapq
        distances = {vertex: float("inf") for vertex in self.vertices}
        distances[start] = 0
        pq = [(0, start)]
        visited = set()

        while pq:
            current_dist, current = heapq.heappop(pq)
            if current in visited:
                continue
            visited.add(current)

            for neighbor, weight in self.adjacency[current]:
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances

    def has_cycle(self) -> bool:
        """Detect cycle in graph."""
        visited = set()
        rec_stack = set()

        def _dfs(vertex):
            visited.add(vertex)
            rec_stack.add(vertex)

            for neighbor, _ in self.adjacency[vertex]:
                if neighbor not in visited:
                    if _dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.discard(vertex)
            return False

        for vertex in self.vertices:
            if vertex not in visited:
                if _dfs(vertex):
                    return True
        return False

    def topological_sort(self) -> List:
        """Topological sort (for DAG)."""
        visited = set()
        result = []

        def _dfs(vertex):
            visited.add(vertex)
            for neighbor, _ in self.adjacency[vertex]:
                if neighbor not in visited:
                    _dfs(neighbor)
            result.insert(0, vertex)

        for vertex in self.vertices:
            if vertex not in visited:
                _dfs(vertex)
        return result

    def degree(self, vertex) -> int:
        """Degree of a vertex."""
        return len(self.adjacency[vertex])

    def adjacency_matrix(self) -> List[List[int]]:
        """Generate adjacency matrix."""
        vertices = sorted(self.vertices)
        index = {v: i for i, v in enumerate(vertices)}
        matrix = [[0] * len(vertices) for _ in range(len(vertices))]

        for v in vertices:
            for neighbor, _ in self.adjacency[v]:
                matrix[index[v]][index[neighbor]] = 1

        return matrix

    def __repr__(self):
        result = []
        for vertex, neighbors in self.adjacency.items():
            neighbor_str = ", ".join(f"{n}(w={w})" for n, w in neighbors)
            result.append(f"  {vertex}: [{neighbor_str}]")
        return "\n".join(result)


def main():
    print("=== Graph Creation ===")
    g = Graph(directed=False)
    edges = [
        ("A", "B"), ("A", "C"), ("B", "D"),
        ("C", "D"), ("D", "E"), ("C", "E"),
    ]
    for u, v in edges:
        g.add_edge(u, v)

    print("  Adjacency list:")
    print(g)
    print(f"  Vertices: {g.vertices}")
    print(f"  Vertex count: {g.vertex_count}")

    print("\n=== Traversals ===")
    print(f"  BFS from A: {g.bfs('A')}")
    print(f"  DFS from A: {g.dfs('A')}")

    print("\n=== Weighted Graph (Dijkstra) ===")
    wg = Graph(directed=True)
    wg.add_edge("A", "B", 4)
    wg.add_edge("A", "C", 2)
    wg.add_edge("B", "C", 1)
    wg.add_edge("B", "D", 5)
    wg.add_edge("C", "D", 8)
    wg.add_edge("C", "E", 10)
    wg.add_edge("D", "E", 2)

    distances = wg.dijkstra("A")
    print("  Shortest distances from A:")
    for v, d in sorted(distances.items()):
        print(f"    A -> {v}: {d}")

    print("\n=== Cycle Detection ===")
    print(f"  Undirected graph has cycle: {g.has_cycle()}")

    dag = Graph(directed=True)
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]:
        dag.add_edge(u, v)
    print(f"  DAG has cycle: {dag.has_cycle()}")

    cyclic = Graph(directed=True)
    for u, v in [("A", "B"), ("B", "C"), ("C", "A")]:
        cyclic.add_edge(u, v)
    print(f"  Directed cycle has cycle: {cyclic.has_cycle()}")

    print("\n=== Topological Sort ===")
    print(f"  DAG topological order: {dag.topological_sort()}")

    print("\n=== Degree ===")
    for v in sorted(g.vertices):
        print(f"  Degree of {v}: {g.degree(v)}")

    print("\n=== Adjacency Matrix ===")
    matrix = g.adjacency_matrix()
    vertices = sorted(g.vertices)
    print(f"  Vertices: {vertices}")
    for i, row in enumerate(matrix):
        print(f"  {vertices[i]}: {row}")

    print("\n=== Graph Applications ===")
    print("  - Social networks")
    print("  - Navigation/maps")
    print("  - Network routing")
    print("  - Dependency resolution")
    print("  - Recommendation systems")


if __name__ == "__main__":
    main()
