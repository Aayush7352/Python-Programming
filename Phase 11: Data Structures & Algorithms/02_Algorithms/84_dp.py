import time


def fib_recursive(n: int) -> int:
    """Fibonacci: naive recursion (O(2^n))."""
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_memoization(n: int, memo: dict = None) -> int:
    """Fibonacci: top-down DP with memoization."""
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memoization(n - 1, memo) + fib_memoization(n - 2, memo)
    return memo[n]


def fib_tabulation(n: int) -> int:
    """Fibonacci: bottom-up DP with tabulation."""
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def fib_optimized(n: int) -> int:
    """Fibonacci: optimized O(1) space."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def knapSack(weights: list, values: list, capacity: int) -> int:
    """0/1 KnapSack: maximize value within weight capacity."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


def longest_common_subsequence(text1: str, text2: str) -> int:
    """LCS: longest common subsequence."""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def longest_increasing_subsequence(nums: list) -> int:
    """LIS: longest increasing subsequence."""
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def edit_distance(word1: str, word2: str) -> int:
    """Levenshtein distance (edit distance)."""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # delete
                    dp[i][j - 1],    # insert
                    dp[i - 1][j - 1]  # replace
                )

    return dp[m][n]


def coin_change(coins: list, amount: int) -> int:
    """Minimum coins needed to make amount."""
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float("inf") else -1


def main():
    print("=== Fibonacci (DP vs Naive) ===")
    n = 35
    start = time.time()
    result1 = fib_recursive(n)
    print(f"  fib_recursive({n}): {result1} ({time.time() - start:.4f}s)")

    start = time.time()
    result2 = fib_memoization(n)
    print(f"  fib_memoization({n}): {result2} ({time.time() - start:.4f}s)")

    start = time.time()
    result3 = fib_tabulation(n)
    print(f"  fib_tabulation({n}): {result3} ({time.time() - start:.4f}s)")

    print("\n=== 0/1 KnapSack ===")
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5
    result = knapSack(weights, values, capacity)
    print(f"  Max value (capacity={capacity}): {result}")

    print("\n=== Longest Common Subsequence ===")
    text1, text2 = "abcdef", "acdf"
    lcs_length = longest_common_subsequence(text1, text2)
    print(f"  LCS of '{text1}' and '{text2}': {lcs_length}")

    print("\n=== Longest Increasing Subsequence ===")
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    lis_length = longest_increasing_subsequence(nums)
    print(f"  LIS of {nums}: {lis_length}")

    print("\n=== Edit Distance ===")
    w1, w2 = "kitten", "sitting"
    dist = edit_distance(w1, w2)
    print(f"  Edit distance '{w1}' -> '{w2}': {dist}")

    print("\n=== Coin Change ===")
    coins = [1, 2, 5]
    amount = 11
    min_coins = coin_change(coins, amount)
    print(f"  Minimum coins for ${amount} with {coins}: {min_coins}")

    print("\n=== DP Problem Patterns ===")
    print("  1. Fibonacci-style (1D DP)")
    print("  2. KnapSack (2D DP)")
    print("  3. LCS (2D DP with strings)")
    print("  4. LIS (1D DP with nested loop)")
    print("  5. Edit Distance (2D DP)")
    print("  6. Coin Change (1D DP)")
    print("\n  DP Approaches:")
    print("  - Top-down: recursion + memoization")
    print("  - Bottom-up: tabulation")


if __name__ == "__main__":
    main()
