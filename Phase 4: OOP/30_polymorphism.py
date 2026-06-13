from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """Abstract base class for shapes."""

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def description(self) -> str:
        return f"I am a {self.__class__.__name__}"


class Circle(Shape):
    """Circle implements Shape interface."""

    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius

    def __repr__(self) -> str:
        return f"Circle(r={self.radius})"


class Rectangle(Shape):
    """Rectangle implements Shape interface."""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def __repr__(self) -> str:
        return f"Rectangle({self.width}x{self.height})"


class Triangle(Shape):
    """Triangle implements Shape interface."""

    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c

    def __repr__(self) -> str:
        return f"Triangle({self.a}, {self.b}, {self.c})"


def print_shape_info(shape: Shape) -> None:
    """Polymorphic function: works with any Shape."""
    print(f"  {shape}")
    print(f"  {shape.description()}")
    print(f"  Area: {shape.area():.2f}")
    print(f"  Perimeter: {shape.perimeter():.2f}")
    print()


def main():
    print("=== Polymorphism with Shapes ===")
    shapes: list[Shape] = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 4, 5),
        Circle(2.5),
        Rectangle(3, 3),  # Square (special rectangle)
    ]

    # Polymorphic iteration
    for shape in shapes:
        print_shape_info(shape)

    # Duck typing example
    print("\n=== Duck Typing ===")

    class Dog:
        def speak(self):
            return "Woof!"

    class Cat:
        def speak(self):
            return "Meow!"

    class Duck:
        def speak(self):
            return "Quack!"

    def animal_sound(animal) -> str:
        return animal.speak()

    for animal in [Dog(), Cat(), Duck()]:
        print(f"  {animal.__class__.__name__}: {animal_sound(animal)}")

    # Operator overloading (polymorphism)
    print("\n=== Operator Overloading ===")
    print(f"  'Hello' + ' World' = {'Hello' + ' World'}")
    print(f"  [1, 2] + [3, 4] = {[1, 2] + [3, 4]}")
    print(f"  3 + 4 = {3 + 4}")
    print(f"  3.5 + 2.5 = {3.5 + 2.5}")


if __name__ == "__main__":
    main()
