def dfs_paths(graph: dict, start, target, path=None) -> list:
    """DFS to find all paths from start to target."""
    if path is None:
        path = [start]

    if start == target:
        return [path.copy()]

    paths = []
    for neighbor in graph.get(start, []):
        if neighbor not in path:
            path.append(neighbor)
            paths.extend(dfs_paths(graph, neighbor, target, path))
            path.pop()

    return paths


def has_path_dfs(graph: dict, start, target, visited=None) -> bool:
    """DFS to check if path exists."""
    if visited is None:
        visited = set()
    if start == target:
        return True
    visited.add(start)

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            if has_path_dfs(graph, neighbor, target, visited):
                return True
    return False


def dfs_islands(grid: list[list]) -> int:
    """DFS to count islands in a grid."""
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def dfs(r, c):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 0:
            return
        visited.add((r, c))
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                dfs(r, c)
                islands += 1
    return islands


def dfs_permutations(nums: list) -> list:
    """DFS to generate all permutations."""
    result = []

    def backtrack(current, remaining):
        if not remaining:
            result.append(current.copy())
            return
        for i, val in enumerate(remaining):
            current.append(val)
            backtrack(current, remaining[:i] + remaining[i + 1:])
            current.pop()

    backtrack([], nums)
    return result


def dfs_combinations(n: int, k: int) -> list:
    """DFS to generate all combinations of size k."""
    result = []

    def backtrack(start, current):
        if len(current) == k:
            result.append(current.copy())
            return
        for i in range(start, n + 1):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()

    backtrack(1, [])
    return result


def main():
    print("=== DFS: Find Path ===")
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": [],
        "E": ["F"],
        "F": [],
    }
    print(f"  Path A->F exists: {has_path_dfs(graph, 'A', 'F')}")
    print(f"  Path A->Z exists: {has_path_dfs(graph, 'A', 'Z')}")

    print("\n=== DFS: All Paths ===")
    paths = dfs_paths(graph, "A", "F")
    print(f"  All paths A->F: {paths}")

    print("\n=== DFS: Count Islands ===")
    grid = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1],
    ]
    islands = dfs_islands(grid)
    print(f"  Number of islands: {islands}")

    print("\n=== DFS: Permutations ===")
    perms = dfs_permutations([1, 2, 3])
    print(f"  Permutations of [1,2,3]: {perms}")

    print("\n=== DFS: Combinations ===")
    combos = dfs_combinations(4, 2)
    print(f"  Combinations of C(4,2): {combos}")

    print("\n=== DFS: Maze Solving ===")
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]

    def solve_maze(maze, start, end):
        rows, cols = len(maze), len(maze[0])
        path = []

        def dfs(r, c):
            if (r, c) == end:
                path.append((r, c))
                return True
            if (r < 0 or r >= rows or c < 0 or c >= cols or
                maze[r][c] == 1 or (r, c) in path):
                return False

            path.append((r, c))
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                if dfs(r + dr, c + dc):
                    return True
            path.pop()
            return False

        dfs(start[0], start[1])
        return path

    maze_path = solve_maze(maze, (0, 0), (4, 4))
    print(f"  Maze path: {maze_path}")

    print("\n=== DFS Properties ===")
    print("  - Uses stack (recursion or explicit stack)")
    print("  - Time: O(V + E)")
    print("  - Space: O(V)")
    print("  - Not guaranteed shortest path")
    print("  - Good for: puzzles, permutations, connectivity")


if __name__ == "__main__":
    main()
