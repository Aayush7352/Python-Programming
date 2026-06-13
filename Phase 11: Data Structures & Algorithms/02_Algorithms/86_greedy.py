def activity_selection(start: list, finish: list) -> list:
    """Select maximum non-overlapping activities.

    Greedy: choose the activity that finishes earliest.
    """
    n = len(start)
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    selected = [activities[0]]
    last_finish = activities[0][1]

    for i in range(1, n):
        if activities[i][0] >= last_finish:
            selected.append(activities[i])
            last_finish = activities[i][1]

    return selected


def fractional_knapsack(weights: list, values: list, capacity: float) -> float:
    """Fractional knapsack: maximize value with weight constraint.

    Greedy: take items with highest value/weight ratio first.
    """
    items = sorted(
        zip(weights, values),
        key=lambda x: x[1] / x[0],
        reverse=True
    )
    total_value = 0.0

    for weight, value in items:
        if capacity >= weight:
            total_value += value
            capacity -= weight
        else:
            total_value += value * (capacity / weight)
            break

    return total_value


def coin_change_greedy(coins: list, amount: int) -> list:
    """Minimum coins using greedy approach.

    Works optimally for canonical coin systems (e.g., USD).
    """
    coins = sorted(coins, reverse=True)
    result = []

    for coin in coins:
        while amount >= coin:
            amount -= coin
            result.append(coin)

    return result


def huffman_coding(frequencies: dict) -> dict:
    """Huffman coding: optimal prefix codes.

    Greedy: merge two least frequent nodes.
    """
    import heapq

    heap = [[freq, [char, ""]] for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        low = heapq.heappop(heap)
        high = heapq.heappop(heap)

        for pair in low[1:]:
            pair[1] = "0" + pair[1]
        for pair in high[1:]:
            pair[1] = "1" + pair[1]

        heapq.heappush(heap, [low[0] + high[0]] + low[1:] + high[1:])

    return {char: code for char, code in heap[0][1:]}


def minimum_spanning_tree(graph: dict) -> list:
    """Prim's algorithm for Minimum Spanning Tree.

    Greedy: always add the cheapest edge to the current tree.
    """
    import heapq

    start = next(iter(graph))
    visited = {start}
    edges = []

    # Add all edges from start to heap
    heap = []
    for neighbor, weight in graph[start]:
        heapq.heappush(heap, (weight, start, neighbor))

    mst = []

    while heap and len(visited) < len(graph):
        weight, u, v = heapq.heappop(heap)
        if v not in visited:
            visited.add(v)
            mst.append((u, v, weight))
            for neighbor, w in graph[v]:
                if neighbor not in visited:
                    heapq.heappush(heap, (w, v, neighbor))

    return mst


def main():
    print("=== Activity Selection ===")
    start = [1, 3, 0, 5, 8, 5]
    finish = [2, 4, 6, 7, 9, 9]
    selected = activity_selection(start, finish)
    print(f"  Selected activities: {selected}")

    print("\n=== Fractional Knapsack ===")
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    max_value = fractional_knapsack(weights, values, capacity)
    print(f"  Max value (capacity={capacity}): {max_value:.2f}")

    print("\n=== Coin Change (Greedy) ===")
    coins = [1, 5, 10, 25]
    amount = 67
    change = coin_change_greedy(coins, amount)
    print(f"  ${amount} = {change}")
    print(f"  Count: {len(change)} coins")

    print("\n=== Huffman Coding ===")
    frequencies = {"A": 5, "B": 9, "C": 12, "D": 13, "E": 16, "F": 45}
    codes = huffman_coding(frequencies)
    print(f"  Huffman codes:")
    for char, code in sorted(codes.items()):
        print(f"    '{char}': {code}")

    print("\n=== Minimum Spanning Tree (Prim's) ===")
    graph = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 1), ("D", 5)],
        "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
        "D": [("B", 5), ("C", 8), ("E", 2)],
        "E": [("C", 10), ("D", 2)],
    }
    mst = minimum_spanning_tree(graph)
    total_weight = sum(w for _, _, w in mst)
    print(f"  MST edges: {mst}")
    print(f"  Total weight: {total_weight}")

    # Greedy vs DP: when greedy fails
    print("\n=== Greedy vs DP (Coin Change Counterexample) ===")
    coins = [1, 3, 4]
    amount = 6
    greedy = coin_change_greedy(coins, amount)
    print(f"  Coins: {coins}, Amount: ${amount}")
    print(f"  Greedy: {greedy} ({len(greedy)} coins)")

    from dp import coin_change as dp_coin
    min_coins = dp_coin(coins, amount)
    print(f"  DP optimal: {min_coins} coins")
    print(f"  Greedy fails because 4+1+1 > 3+3")

    print("\n=== Greedy Properties ===")
    print("  - Makes locally optimal choice at each step")
    print("  - Not always globally optimal")
    print("  - Works when problem has optimal substructure")
    print("  - Examples: MST, Huffman, Dijkstra")
    print("  - Faster than DP but may not find optimal")


if __name__ == "__main__":
    main()
