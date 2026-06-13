class ListNode:
    """Node in a singly linked list."""
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    """Singly linked list implementation."""

    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, value):
        """Add a node to the end."""
        node = ListNode(value)
        if not self.head:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        self._size += 1

    def prepend(self, value):
        """Add a node to the beginning."""
        node = ListNode(value)
        node.next = self.head
        self.head = node
        self._size += 1

    def delete(self, value):
        """Delete first occurrence of value."""
        if not self.head:
            return False
        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1
            return True
        current = self.head
        while current.next and current.next.value != value:
            current = current.next
        if current.next:
            current.next = current.next.next
            self._size -= 1
            return True
        return False

    def find(self, value):
        """Find value in list."""
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def reverse(self):
        """Reverse the linked list in-place."""
        prev, current = None, self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def to_list(self):
        """Convert to Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    @property
    def size(self):
        return self._size

    def __repr__(self):
        return f"LinkedList({self.to_list()})"


class DoublyListNode:
    """Node in a doubly linked list."""
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """Doubly linked list implementation."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, value):
        node = DoublyListNode(value)
        if not self.head:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    def prepend(self, value):
        node = DoublyListNode(value)
        if not self.head:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1

    def delete(self, value):
        current = self.head
        while current:
            if current.value == value:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self._size -= 1
                return True
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    def to_reverse_list(self):
        result = []
        current = self.tail
        while current:
            result.append(current.value)
            current = current.prev
        return result


def main():
    print("=== Singly Linked List ===")
    ll = LinkedList()
    for v in [1, 2, 3, 4, 5]:
        ll.append(v)
    print(f"  After appends: {ll} (size={ll.size})")

    ll.prepend(0)
    print(f"  After prepend(0): {ll}")

    ll.delete(3)
    print(f"  After delete(3): {ll}")

    print(f"  Find 4: {ll.find(4)}, Find 10: {ll.find(10)}")

    ll.reverse()
    print(f"  After reverse: {ll}")

    print("\n=== Doubly Linked List ===")
    dll = DoublyLinkedList()
    for v in [10, 20, 30, 40, 50]:
        dll.append(v)
    print(f"  Forward: {dll.to_list()}")
    print(f"  Reverse: {dll.to_reverse_list()}")

    dll.prepend(5)
    print(f"  After prepend(5): {dll.to_list()}")

    dll.delete(30)
    print(f"  After delete(30): {dll.to_list()}")

    # Performance comparison
    print("\n=== Performance ===")
    import time
    big_ll = LinkedList()
    start = time.perf_counter()
    for i in range(10000):
        big_ll.append(i)
    print(f"  Append 10000 items: {time.perf_counter() - start:.4f}s")


if __name__ == "__main__":
    main()
