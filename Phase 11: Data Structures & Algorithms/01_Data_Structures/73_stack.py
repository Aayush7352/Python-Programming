class Stack:
    """Stack implementation using Python list."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty:
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty:
            raise IndexError("Peek from empty stack")
        return self._items[-1]

    @property
    def is_empty(self):
        return len(self._items) == 0

    @property
    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


class StackWithMax:
    """Stack that tracks maximum value in O(1)."""

    def __init__(self):
        self._stack = []
        self._max_stack = []

    def push(self, item):
        self._stack.append(item)
        if not self._max_stack or item >= self._max_stack[-1]:
            self._max_stack.append(item)

    def pop(self):
        if self.is_empty:
            raise IndexError("Pop from empty stack")
        item = self._stack.pop()
        if item == self._max_stack[-1]:
            self._max_stack.pop()
        return item

    def max(self):
        if self.is_empty:
            raise IndexError("Max from empty stack")
        return self._max_stack[-1]

    @property
    def is_empty(self):
        return len(self._stack) == 0


def is_balanced_parentheses(expr: str) -> bool:
    """Check if parentheses are balanced using stack."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = Stack()

    for char in expr:
        if char in "({[":
            stack.push(char)
        elif char in ")}]":
            if stack.is_empty or stack.pop() != pairs[char]:
                return False
    return stack.is_empty


def evaluate_postfix(expr: str) -> float:
    """Evaluate postfix expression using stack."""
    stack = Stack()
    operators = {"+": lambda a, b: a + b,
                 "-": lambda a, b: a - b,
                 "*": lambda a, b: a * b,
                 "/": lambda a, b: a / b}

    for token in expr.split():
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            stack.push(operators[token](a, b))
        else:
            stack.push(float(token))
    return stack.pop()


def decimal_to_binary(n: int) -> str:
    """Convert decimal to binary using stack."""
    stack = Stack()
    while n > 0:
        stack.push(n % 2)
        n //= 2
    return "".join(str(stack.pop()) for _ in range(stack.size))


def main():
    print("=== Stack Basics ===")
    stack = Stack()
    for v in [1, 2, 3, 4, 5]:
        stack.push(v)
    print(f"  Stack: {stack}")
    print(f"  Peek: {stack.peek()}")
    print(f"  Pop: {stack.pop()}")
    print(f"  Size: {stack.size}")
    print(f"  Empty: {stack.is_empty}")

    print("\n=== Balanced Parentheses ===")
    tests = ["()", "()[]{}", "([{}])", "(]", "([)]", "((("]
    for t in tests:
        print(f"  '{t}': {is_balanced_parentheses(t)}")

    print("\n=== Postfix Evaluation ===")
    expressions = ["3 4 +", "5 1 2 + 4 * + 3 -", "10 3 /"]
    for expr in expressions:
        print(f"  '{expr}' = {evaluate_postfix(expr)}")

    print("\n=== Decimal to Binary ===")
    for n in [10, 42, 255, 1024]:
        print(f"  {n} = {decimal_to_binary(n)}")

    print("\n=== Stack with Max ===")
    sm = StackWithMax()
    for v in [3, 1, 6, 2, 8]:
        sm.push(v)
        print(f"  push({v}), max={sm.max()}")
    sm.pop()
    print(f"  after pop, max={sm.max()}")
    sm.pop()
    print(f"  after pop, max={sm.max()}")

    print("\n=== Stack Applications ===")
    print("  - Undo/Redo in editors")
    print("  - Back/Forward in browsers")
    print("  - Expression evaluation")
    print("  - Syntax parsing")
    print("  - Call stack management")


if __name__ == "__main__":
    main()
