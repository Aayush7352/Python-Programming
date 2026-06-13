class ValidatedAttribute:
    """Descriptor that validates attribute values."""

    def __init__(self, validator=None, min_val=None, max_val=None):
        self.validator = validator
        self.min_val = min_val
        self.max_val = max_val
        self.data = {}

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.data.get(obj, None)

    def __set__(self, obj, value):
        if self.validator and not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")
        self.data[obj] = value

    def __delete__(self, obj):
        raise AttributeError(f"Cannot delete {self.name}")


class PositiveNumber:
    """Descriptor that only allows positive numbers."""

    def __init__(self, default=0):
        self.default = default
        self.data = {}

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.data.get(obj, self.default)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number")
        if value <= 0:
            raise ValueError(f"{self.name} must be positive")
        self.data[obj] = value


class Product:
    """Using descriptors for attribute management."""

    name = ValidatedAttribute(validator=lambda x: isinstance(x, str) and len(x) > 0)
    price = ValidatedAttribute(min_val=0)
    quantity = PositiveNumber()

    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def total_value(self) -> float:
        return self.price * self.quantity

    def __repr__(self):
        return f"Product('{self.name}', ${self.price:.2f}, qty={self.quantity})"


class Person:
    """Another class using descriptors."""

    age = ValidatedAttribute(min_val=0, max_val=150)
    score = ValidatedAttribute(min_val=0, max_val=100)

    def __init__(self, name: str, age: int, score: float):
        self.name = name  # regular attribute
        self.age = age
        self.score = score


def main():
    print("=== Descriptor: ValidatedAttribute ===")
    p = Product("Laptop", 999.99, 10)
    print(f"  {p}")
    print(f"  Total value: ${p.total_value:.2f}")

    try:
        p.price = -100
    except ValueError as e:
        print(f"  Validation error: {e}")

    try:
        p.quantity = 0
    except ValueError as e:
        print(f"  Quantity error: {e}")

    print(f"\n  After valid update:")
    p.price = 899.99
    p.quantity = 5
    print(f"  {p}")

    print("\n=== Descriptor: Person ===")
    person = Person("Alice", 30, 85.5)
    print(f"  {person.name}: age={person.age}, score={person.score}")

    try:
        person.age = 200
    except ValueError as e:
        print(f"  Age validation: {e}")

    try:
        person.score = 105
    except ValueError as e:
        print(f"  Score validation: {e}")

    print("\n=== Descriptor with Multiple Instances ===")
    p1 = Product("Mouse", 25.99, 100)
    p2 = Product("Keyboard", 75.50, 50)
    print(f"  p1: {p1}")
    print(f"  p2: {p2}")
    p1.price = 19.99  # only affects p1
    print(f"  p1 after change: {p1}")
    print(f"  p2 unchanged: {p2}")

    print("\n=== Accessing Descriptor from Class ===")
    print(f"  Descriptor: {Product.price}")
    print(f"  Type: {type(Product.price)}")


if __name__ == "__main__":
    main()
