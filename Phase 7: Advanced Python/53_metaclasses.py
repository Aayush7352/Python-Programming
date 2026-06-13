class SingletonMeta(type):
    """Metaclass that implements the Singleton pattern."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AutoPropertyMeta(type):
    """Metaclass that auto-creates properties for underscore attributes."""

    def __new__(mcs, name, bases, namespace):
        for key, value in list(namespace.items()):
            if key.startswith("_") and not key.startswith("__"):
                prop_name = key[1:]  # remove underscore prefix
                def make_getter(k):
                    return property(lambda self: getattr(self, k))
                namespace[prop_name] = make_getter(key)
        return super().__new__(mcs, name, bases, namespace)


class ValidateFieldsMeta(type):
    """Metaclass that validates field definitions."""

    def __new__(mcs, name, bases, namespace):
        fields = {}
        for key, value in namespace.items():
            if not key.startswith("_"):
                fields[key] = value

        def validate(self):
            for field_name, expected_type in fields.items():
                actual_value = getattr(self, field_name, None)
                if actual_value is not None and not isinstance(actual_value, expected_type):
                    raise TypeError(
                        f"Field '{field_name}' expected {expected_type.__name__}, "
                        f"got {type(actual_value).__name__}"
                    )
        namespace["validate"] = validate
        namespace["_fields"] = fields
        return super().__new__(mcs, name, bases, namespace)


# Classes using our metaclasses

class Config(metaclass=SingletonMeta):
    """Singleton configuration class."""
    def __init__(self):
        self.settings = {}

    def set(self, key, value):
        self.settings[key] = value

    def get(self, key, default=None):
        return self.settings.get(key, default)


class Person(metaclass=ValidateFieldsMeta):
    name: str
    age: int

    def __init__(self, name, age):
        self.name = name
        self.age = age


def demonstrate_type():
    """type() as a metaclass."""
    print("=== type() as Metaclass ===")
    DynamicClass = type("DynamicClass", (), {
        "greeting": "Hello",
        "greet": lambda self, name: f"{self.greeting}, {name}!"
    })

    obj = DynamicClass()
    print(f"  Class name: {DynamicClass.__name__}")
    print(f"  Bases: {DynamicClass.__bases__}")
    print(f"  {obj.greet('World')}")


def demonstrate_singleton():
    """Singleton via metaclass."""
    print("\n=== Singleton Metaclass ===")
    config1 = Config()
    config2 = Config()
    print(f"  config1 is config2: {config1 is config2}")

    config1.set("debug", True)
    print(f"  config2.get('debug'): {config2.get('debug')}")


def demonstrate_validation():
    """Field validation via metaclass."""
    print("\n=== Validation Metaclass ===")
    p = Person("Alice", 30)
    print(f"  Valid person: {p.name}, {p.age}")
    p.validate()
    print(f"  Validation passed")

    try:
        p.name = 123
        p.validate()
    except TypeError as e:
        print(f"  Validation failed: {e}")


def main():
    demonstrate_type()
    demonstrate_singleton()
    demonstrate_validation()

    # Metaclass internals
    print("\n=== Metaclass Internals ===")
    print(f"  Config class is instance of: {type(Config)}")
    print(f"  Person class is instance of: {type(Person)}")
    print(f"  Person fields: {Person._fields}")

    # Metaclass conflict (cannot inherit from classes with different metaclasses)
    print("\n=== Metaclass Resolution ===")
    class MetaA(type): pass
    class MetaB(type): pass
    class A(metaclass=MetaA): pass
    class B(metaclass=MetaB): pass

    try:
        class C(A, B): pass
    except TypeError as e:
        print(f"  Metaclass conflict error: {e}")

    # Solution: create a combined metaclass
    class MetaCombined(MetaA, MetaB): pass
    class C(A, B, metaclass=MetaCombined): pass
    print(f"  Combined metaclass works: {C.__name__}")


if __name__ == "__main__":
    main()
