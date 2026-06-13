from datetime import datetime


class Person:
    """Person with multiple constructor patterns."""

    # Primary constructor
    def __init__(self, name: str, age: int, email: str = None):
        self.name = name
        self.age = age
        self.email = email
        self.created_at = datetime.now()

    # Alternative constructor: from year of birth
    @classmethod
    def from_birth_year(cls, name: str, birth_year: int, email: str = None):
        current_year = datetime.now().year
        age = current_year - birth_year
        return cls(name, age, email)

    # Alternative constructor: from full name (splits into first/last)
    @classmethod
    def from_full_name(cls, full_name: str, age: int):
        return cls(full_name, age)

    # Alternative constructor: from dictionary
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name", "Unknown"),
            age=data.get("age", 0),
            email=data.get("email"),
        )

    # Alternative constructor: parsing "Name, Age, Email"
    @classmethod
    def from_csv(cls, csv_string: str):
        parts = [p.strip() for p in csv_string.split(",")]
        name = parts[0]
        age = int(parts[1]) if len(parts) > 1 else 0
        email = parts[2] if len(parts) > 2 else None
        return cls(name, age, email)

    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age}, email='{self.email}')"


class Config:
    """Singleton-like constructor pattern."""

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, debug: bool = False):
        if not Config._initialized:
            self.debug = debug
            self.settings = {}
            Config._initialized = True


def demonstrate_constructors():
    print("=== Standard Constructor ===")
    p1 = Person("Alice", 30, "alice@example.com")
    print(f"  {p1}")

    print("\n=== Class Method: from_birth_year ===")
    p2 = Person.from_birth_year("Bob", 1990, "bob@example.com")
    print(f"  {p2}")

    print("\n=== Class Method: from_dict ===")
    data = {"name": "Charlie", "age": 25, "email": "charlie@example.com"}
    p3 = Person.from_dict(data)
    print(f"  {p3}")

    print("\n=== Class Method: from_csv ===")
    p4 = Person.from_csv("Diana, 28, diana@example.com")
    print(f"  {p4}")

    print("\n=== Singleton Pattern ===")
    c1 = Config(debug=True)
    c2 = Config(debug=False)
    print(f"  c1 is c2: {c1 is c2}")
    print(f"  c1.debug = {c1.debug} (only first init applies)")


def main():
    demonstrate_constructors()


if __name__ == "__main__":
    main()
