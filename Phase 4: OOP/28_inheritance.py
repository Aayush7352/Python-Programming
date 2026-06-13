class Animal:
    """Base class for all animals."""

    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species

    def make_sound(self) -> str:
        return f"{self.name} makes a sound"

    def move(self) -> str:
        return f"{self.name} moves around"

    def __repr__(self) -> str:
        return f"{self.species}: {self.name}"


class Mammal(Animal):
    """Inherits from Animal, adds mammal-specific behavior."""

    def __init__(self, name: str, species: str, fur_color: str):
        super().__init__(name, species)
        self.fur_color = fur_color

    def make_sound(self) -> str:
        return f"{self.name} makes a mammalian sound"

    def feed_babies(self) -> str:
        return f"{self.name} feeds its babies milk"


class Dog(Mammal):
    """Inherits from Mammal, overrides behaviors."""

    def __init__(self, name: str, breed: str, fur_color: str = "brown"):
        super().__init__(name, "Canis familiaris", fur_color)
        self.breed = breed

    def make_sound(self) -> str:
        return f"{self.name} barks: Woof! Woof!"

    def fetch(self, item: str) -> str:
        return f"{self.name} fetches the {item}"


class Cat(Mammal):
    """Another Mammal subclass."""

    def __init__(self, name: str, fur_color: str = "orange"):
        super().__init__(name, "Felis catus", fur_color)

    def make_sound(self) -> str:
        return f"{self.name} meows: Meow!"

    def purr(self) -> str:
        return f"{self.name} is purring"


def main():
    print("=== Base Animal ===")
    animal = Animal("Generic", "Unknown")
    print(f"  {animal}")
    print(f"  {animal.make_sound()}")
    print(f"  {animal.move()}")

    print("\n=== Mammal (Intermediate) ===")
    mammal = Mammal("GenericMammal", "Mammalia", "gray")
    print(f"  {mammal}")
    print(f"  {mammal.make_sound()}")
    print(f"  {mammal.feed_babies()}")
    print(f"  {mammal.move()}")

    print("\n=== Dog (Derived) ===")
    dog = Dog("Buddy", "Golden Retriever", "golden")
    print(f"  {dog}")
    print(f"  Species: {dog.species}")
    print(f"  Breed: {dog.breed}")
    print(f"  Fur: {dog.fur_color}")
    print(f"  {dog.make_sound()}")
    print(f"  {dog.fetch('ball')}")
    print(f"  {dog.feed_babies()}")
    print(f"  {dog.move()}")

    print("\n=== Cat (Derived) ===")
    cat = Cat("Whiskers")
    print(f"  {cat}")
    print(f"  {cat.make_sound()}")
    print(f"  {cat.purr()}")

    # isinstance and issubclass checks
    print("\n=== Type Checking ===")
    print(f"Dog is Animal: {isinstance(dog, Animal)}")
    print(f"Dog is Mammal: {isinstance(dog, Mammal)}")
    print(f"Animal is Dog: {isinstance(animal, Dog)}")
    print(f"Dog subclass of Animal: {issubclass(Dog, Animal)}")
    print(f"Dog subclass of Cat: {issubclass(Dog, Cat)}")

    # Method Resolution Order
    print(f"\n=== MRO ===")
    print(f"Dog MRO: {[c.__name__ for c in Dog.__mro__]}")


if __name__ == "__main__":
    main()
