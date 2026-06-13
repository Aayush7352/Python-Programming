def main():
    # Creating lists
    empty = []
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, "hello", 3.14, True]
    nested = [[1, 2], [3, 4], [5, 6]]
    constructed = list("python")
    comprehension = [x ** 2 for x in range(10)]

    print("=== Creating Lists ===")
    print(f"Empty: {empty}")
    print(f"Numbers: {numbers}")
    print(f"Mixed: {mixed}")
    print(f"Nested: {nested}")
    print(f"From string: {constructed}")
    print(f"Comprehension: {comprehension}")

    # List indexing and slicing
    print("\n=== Indexing and Slicing ===")
    print(f"First: {numbers[0]}, Last: {numbers[-1]}")
    print(f"Slice [1:3]: {numbers[1:3]}")
    print(f"Slice [::2]: {numbers[::2]}")
    print(f"Reverse: {numbers[::-1]}")

    # List operations
    print("\n=== List Operations ===")
    nums = [1, 2, 3]
    nums.append(4); print(f"After append(4): {nums}")
    nums.extend([5, 6]); print(f"After extend([5,6]): {nums}")
    nums.insert(0, 0); print(f"After insert(0, 0): {nums}")
    nums.remove(3); print(f"After remove(3): {nums}")
    popped = nums.pop(); print(f"After pop(): {nums}, popped: {popped}")
    popped_idx = nums.pop(0); print(f"After pop(0): {nums}, popped: {popped_idx}")
    nums.sort(reverse=True); print(f"After sort reverse: {nums}")
    nums.reverse(); print(f"After reverse: {nums}")

    # List methods
    print("\n=== List Methods ===")
    print(f"Index of 5: {nums.index(5)}")
    print(f"Count of 2: {nums.count(2)}")
    copy = nums.copy(); print(f"Shallow copy: {copy}")
    nums.clear(); print(f"After clear: {nums}")

    # List as stack/queue
    print("\n=== List as Stack/Queue ===")
    stack = []
    stack.append(1); stack.append(2); stack.append(3)
    print(f"Stack: {stack}, Pop: {stack.pop()}")
    from collections import deque
    queue = deque(["a", "b", "c"])
    queue.append("d")
    print(f"Queue: {list(queue)}, Popleft: {queue.popleft()}")


if __name__ == "__main__":
    main()
