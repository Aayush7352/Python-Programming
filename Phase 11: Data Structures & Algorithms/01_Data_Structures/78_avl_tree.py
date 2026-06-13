class AVLNode:
    """Node in an AVL Tree."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """Self-balancing AVL Tree implementation."""

    def __init__(self):
        self.root = None
        self._size = 0

    def _height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node, value):
        balance = self._balance_factor(node)

        # Left Left
        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)

        # Right Right
        if balance < -1 and value > node.right.value:
            return self._rotate_left(node)

        # Left Right
        if balance > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Left
        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, value):
        """Insert a value and rebalance."""
        self.root = self._insert(self.root, value)
        self._size += 1

    def _insert(self, node, value):
        if node is None:
            return AVLNode(value)

        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            self._size -= 1  # duplicate
            return node

        self._update_height(node)
        return self._rebalance(node, value)

    def inorder(self) -> list:
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def is_balanced(self) -> bool:
        """Check if tree is balanced."""
        def _check(node):
            if node is None:
                return True
            balance = abs(self._balance_factor(node))
            return balance <= 1 and _check(node.left) and _check(node.right)

        return _check(self.root)

    @property
    def size(self):
        return self._size

    def height(self):
        return self._height(self.root)


def main():
    print("=== AVL Tree ===")
    avl = AVLTree()

    # Insert values that would cause imbalance in BST
    values = [10, 20, 30, 40, 50, 25]
    for v in values:
        avl.insert(v)
        print(f"  Insert {v}: inorder={avl.inorder()}, height={avl.height()}, "
              f"balanced={avl.is_balanced()}")

    print(f"\n  Final size: {avl.size}")
    print(f"  Final height: {avl.height()}")
    print(f"  Is balanced: {avl.is_balanced()}")

    # Comparison with BST
    print("\n=== BST vs AVL Comparison ===")
    import time, random

    nums = list(range(1, 10001))

    # BST
    from bst import BST
    bst = BST()
    start = time.perf_counter()
    for n in nums:
        bst.insert(n)
    bst_time = time.perf_counter() - start
    print(f"  BST (sorted insert): height={bst.height()}, time={bst_time:.4f}s")

    # AVL
    avl2 = AVLTree()
    start = time.perf_counter()
    for n in nums:
        avl2.insert(n)
    avl_time = time.perf_counter() - start
    print(f"  AVL (sorted insert): height={avl2.height()}, time={avl_time:.4f}s")
    print(f"  AVL is balanced: {avl2.is_balanced()}")

    # Random insert
    random.shuffle(nums)
    bst3 = BST()
    avl3 = AVLTree()
    for n in nums[:1000]:
        bst3.insert(n)
        avl3.insert(n)
    print(f"\n  Random 1000 inserts:")
    print(f"  BST height: {bst3.height()}")
    print(f"  AVL height: {avl3.height()}, balanced: {avl3.is_balanced()}")

    print("\n=== AVL Properties ===")
    print("  - Self-balancing BST (height difference <= 1)")
    print("  - All operations O(log n)")
    print("  - Rotations maintain balance")
    print("  - Used in databases and file systems")


if __name__ == "__main__":
    main()
