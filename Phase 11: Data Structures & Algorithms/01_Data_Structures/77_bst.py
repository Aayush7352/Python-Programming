class BSTNode:
    """Node in a Binary Search Tree."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    """Binary Search Tree implementation."""

    def __init__(self):
        self.root = None
        self._size = 0

    def insert(self, value):
        """Insert a value into BST."""
        self.root = self._insert(self.root, value)
        self._size += 1

    def _insert(self, node, value):
        if node is None:
            return BSTNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            self._size -= 1  # duplicate, not inserted
        return node

    def search(self, value) -> bool:
        """Search for a value."""
        return self._search(self.root, value)

    def _search(self, node, value) -> bool:
        if node is None:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    def delete(self, value) -> bool:
        """Delete a value from BST."""
        size_before = self._size
        self.root = self._delete(self.root, value)
        return self._size < size_before

    def _delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            self._size -= 1
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Two children: find in-order successor
            min_node = self._find_min(node.right)
            node.value = min_node.value
            node.right = self._delete(node.right, min_node.value)
            self._size += 1  # undo the decrement from the recursive delete
        return node

    def _find_min(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def find_min(self):
        if not self.root:
            raise ValueError("Tree is empty")
        return self._find_min(self.root).value

    def find_max(self):
        current = self.root
        while current and current.right:
            current = current.right
        return current.value if current else None

    # Traversals
    def inorder(self) -> list:
        """Left, Root, Right - gives sorted order."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def preorder(self) -> list:
        """Root, Left, Right."""
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self) -> list:
        """Left, Right, Root."""
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)

    def height(self) -> int:
        """Get the height of the tree."""
        return self._height(self.root)

    def _height(self, node) -> int:
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    @property
    def size(self):
        return self._size


def main():
    print("=== BST Insertion ===")
    bst = BST()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 55, 75]
    for v in values:
        bst.insert(v)
    print(f"  Size: {bst.size}")
    print(f"  Min: {bst.find_min()}")
    print(f"  Max: {bst.find_max()}")
    print(f"  Height: {bst.height()}")

    print("\n=== Traversals ===")
    print(f"  Inorder (sorted): {bst.inorder()}")
    print(f"  Preorder: {bst.preorder()}")
    print(f"  Postorder: {bst.postorder()}")

    print("\n=== Search ===")
    for v in [20, 55, 100]:
        print(f"  search({v}): {bst.search(v)}")

    print("\n=== Deletion ===")
    for v in [20, 50, 70]:
        bst.delete(v)
        print(f"  After delete({v}): {bst.inorder()} (size={bst.size})")

    print("\n=== Sorted Array from BST ===")
    sorted_vals = bst.inorder()
    print(f"  Sorted values: {sorted_vals}")

    # Duplicate handling
    print("\n=== Duplicates ===")
    bst2 = BST()
    for v in [5, 3, 7, 5, 3]:
        bst2.insert(v)
    print(f"  BST with duplicates: {bst2.inorder()} (size={bst2.size})")

    # Performance
    print("\n=== Performance ===")
    import time, random
    big_bst = BST()
    nums = list(range(10000))
    random.shuffle(nums)
    start = time.perf_counter()
    for n in nums:
        big_bst.insert(n)
    print(f"  Insert 10000 items: {time.perf_counter() - start:.4f}s")
    print(f"  Height: {big_bst.height()}")


if __name__ == "__main__":
    main()
