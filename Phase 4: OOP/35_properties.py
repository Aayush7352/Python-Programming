class Temperature:
    """Temperature conversion with property validation."""

    def __init__(self, celsius: float = 0):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """Getter for celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Setter with validation."""
        if value < -273.15:
            raise ValueError(f"Temperature {value}°C is below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Computed property: convert to Fahrenheit."""
        return (self._celsius * 9 / 5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """Set temperature via Fahrenheit."""
        self.celsius = (value - 32) * 5 / 9

    @property
    def kelvin(self) -> float:
        """Computed property: convert to Kelvin."""
        return self._celsius + 273.15

    def __repr__(self) -> str:
        return f"Temperature({self._celsius:.1f}°C)"


class Person:
    """Person with property-based attribute management."""

    def __init__(self, name: str, age: int):
        self.name = name
        self._age = age
        self._full_name_parts = name.split()

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if value < 0 or value > 150:
            raise ValueError(f"Age must be between 0 and 150, got {value}")
        self._age = value

    @property
    def first_name(self) -> str:
        return self._full_name_parts[0] if self._full_name_parts else ""

    @property
    def last_name(self) -> str:
        return self._full_name_parts[-1] if len(self._full_name_parts) > 1 else ""

    @property
    def is_adult(self) -> bool:
        return self._age >= 18

    # Read-only property (no setter)
    @property
    def age_in_days(self) -> int:
        return self._age * 365


class Circle:
    """Circle with lazy-loaded computed property."""

    def __init__(self, radius: float):
        self.radius = radius
        self._area: float | None = None

    @property
    def area(self) -> float:
        """Lazy-loaded area computation with caching."""
        if self._area is None:
            import math
            self._area = math.pi * self.radius ** 2
            print(f"  (Computed area: {self._area:.2f})")
        return self._area


def main():
    print("=== Temperature with Properties ===")
    t = Temperature(25)
    print(f"  Celsius: {t.celsius}°C")
    print(f"  Fahrenheit: {t.fahrenheit}°F")
    print(f"  Kelvin: {t.kelvin}K")

    t.celsius = 100
    print(f"\n  After set to 100°C: {t.fahrenheit}°F")

    t.fahrenheit = 32
    print(f"  Set via Fahrenheit: {t}")

    try:
        t.celsius = -300
    except ValueError as e:
        print(f"\n  Validation error: {e}")

    print("\n=== Person with Properties ===")
    p = Person("John Smith", 30)
    print(f"  Full name: {p.name}")
    print(f"  First: {p.first_name}, Last: {p.last_name}")
    print(f"  Age: {p.age}")
    print(f"  Is adult? {p.is_adult}")
    print(f"  Age in days: {p.age_in_days}")

    try:
        p.age = 200
    except ValueError as e:
        print(f"  Validation error: {e}")

    print("\n=== Lazy Property (Circle) ===")
    c = Circle(5)
    print(f"  Radius: {c.radius}")
    print(f"  Area: {c.area:.2f}")
    print(f"  Area (cached): {c.area:.2f}")


if __name__ == "__main__":
    main()
