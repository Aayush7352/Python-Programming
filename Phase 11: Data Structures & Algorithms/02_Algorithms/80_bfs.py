from collections import deque


def bfs_shortest_path(graph: dict, start, target) -> list | None:
    """BFS to find shortest path in unweighted graph."""
    visited = {start}
    queue = deque([(start, [start])])

    while queue:
        vertex, path = queue.popleft()
        if vertex == target:
            return path

        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None


def bfs_level_order(root):
    """BFS on a tree: level-order traversal."""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)

    return result


def bfs_grid_shortest(grid: list[list], start: tuple, end: tuple) -> int:
    """BFS to find shortest path in a grid (0=open, 1=blocked)."""
    rows, cols = len(grid), len(grid[0])
    visited = {start}
    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == end:
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return -1


def bfs_word_ladder(begin_word: str, end_word: str, word_list: set) -> int:
    """BFS: Word Ladder - transform one word to another."""
    if end_word not in word_list:
        return 0

    queue = deque([(begin_word, 1)])
    visited = {begin_word}

    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length

        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                next_word = word[:i] + c + word[i + 1:]
                if next_word in word_list and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, length + 1))

    return 0


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def main():
    print("=== BFS: Shortest Path in Graph ===")
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }
    path = bfs_shortest_path(graph, "A", "F")
    print(f"  Shortest path A->F: {path}")

    print("\n=== BFS: Grid Shortest Path ===")
    grid = [
        [0, 0, 0, 0, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    dist = bfs_grid_shortest(grid, (0, 0), (4, 4))
    print(f"  Shortest path distance: {dist}")

    print("\n=== BFS: Level Order Traversal ===")
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(6)

    levels = bfs_level_order(root)
    print(f"  Level-order: {levels}")

    print("\n=== BFS: Word Ladder ===")
    word_list = {"hot", "dot", "dog", "lot", "log", "cog"}
    length = bfs_word_ladder("hit", "cog", word_list)
    print(f"  Word ladder 'hit' -> 'cog': {length} steps")

    print("\n=== BFS Properties ===")
    print("  - Finds shortest path in unweighted graphs")
    print("  - Uses queue (FIFO)")
    print("  - Time: O(V + E)")
    print("  - Space: O(V)")
    print("  - Complete: always finds solution if exists")


if __name__ == "__main__":
    main()
