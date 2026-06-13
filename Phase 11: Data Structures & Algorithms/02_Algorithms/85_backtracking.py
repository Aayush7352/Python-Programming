def solve_n_queens(n: int) -> list:
    """N-Queens: place N queens on NxN board without threats."""
    result = []

    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

    def backtrack(row, board):
        if row == n:
            result.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board.append(col)
                backtrack(row + 1, board)
                board.pop()

    backtrack(0, [])
    return result


def solve_sudoku(board: list) -> bool:
    """Solve a 9x9 Sudoku puzzle using backtracking."""
    def is_valid(board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def solve():
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            if solve():
                                return True
                            board[i][j] = 0
                    return False
        return True

    return solve()


def generate_subsets(nums: list) -> list:
    """Generate all subsets of a set."""
    result = []

    def backtrack(start, current):
        result.append(current[:])
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result


def generate_parentheses(n: int) -> list:
    """Generate all valid parentheses combinations."""
    result = []

    def backtrack(open_n, close_n, current):
        if len(current) == 2 * n:
            result.append("".join(current))
            return
        if open_n < n:
            current.append("(")
            backtrack(open_n + 1, close_n, current)
            current.pop()
        if close_n < open_n:
            current.append(")")
            backtrack(open_n, close_n + 1, current)
            current.pop()

    backtrack(0, 0, [])
    return result


def partition_palindrome(s: str) -> list:
    """Partition string into palindrome substrings."""
    result = []

    def is_palindrome(sub):
        return sub == sub[::-1]

    def backtrack(start, current):
        if start == len(s):
            result.append(current[:])
            return
        for end in range(start + 1, len(s) + 1):
            if is_palindrome(s[start:end]):
                current.append(s[start:end])
                backtrack(end, current)
                current.pop()

    backtrack(0, [])
    return result


def letter_combinations(digits: str) -> list:
    """Letter combinations of a phone number."""
    if not digits:
        return []

    mapping = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
    }
    result = []

    def backtrack(index, current):
        if index == len(digits):
            result.append("".join(current))
            return
        for letter in mapping[digits[index]]:
            current.append(letter)
            backtrack(index + 1, current)
            current.pop()

    backtrack(0, [])
    return result


def main():
    print("=== N-Queens (4x4) ===")
    solutions = solve_n_queens(4)
    print(f"  Number of solutions: {len(solutions)}")
    for sol in solutions:
        board = [["."] * 4 for _ in range(4)]
        for row, col in enumerate(sol):
            board[row][col] = "Q"
        print(f"  Solution:")
        for row in board:
            print(f"    {' '.join(row)}")
        print()

    print("=== Sudoku Solver ===")
    sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    solved = solve_sudoku(sudoku)
    print(f"  Solved: {solved}")
    for row in sudoku:
        print(f"    {row}")

    print("\n=== Subsets ===")
    subsets = generate_subsets([1, 2, 3])
    print(f"  Subsets of [1,2,3]: {subsets}")

    print("\n=== Generate Parentheses ===")
    parens = generate_parentheses(3)
    print(f"  n=3: {parens}")

    print("\n=== Palindrome Partitioning ===")
    partitions = partition_palindrome("aab")
    print(f"  'aab' partitions: {partitions}")

    print("\n=== Letter Combinations ===")
    combos = letter_combinations("23")
    print(f"  '23' combinations: {combos}")

    print("\n=== Backtracking Properties ===")
    print("  - Explores all possible solutions")
    print("  - Prunes invalid paths (constraint satisfaction)")
    print("  - Time: often exponential")
    print("  - Space: O(depth) for recursion stack")
    print("  - Used for: puzzles, constraints, optimization")


if __name__ == "__main__":
    main()
