class Flyable:
    """Mixin for flying behavior."""

    def fly(self) -> str:
        return f"{self.name} is flying"

    def land(self) -> str:
        return f"{self.name} lands gracefully"

    def can_fly(self) -> bool:
        return True


class Swimmable:
    """Mixin for swimming behavior."""

    def swim(self) -> str:
        return f"{self.name} is swimming"

    def dive(self, depth: int) -> str:
        return f"{self.name} dives to {depth} meters"

    def can_swim(self) -> bool:
        return True


class Walkable:
    """Mixin for walking behavior."""

    def walk(self) -> str:
        return f"{self.name} is walking"

    def run(self, speed: str = "fast") -> str:
        return f"{self.name} runs {speed}"


class Animal:
    """Base class."""

    def __init__(self, name: str):
        self.name = name

    def eat(self) -> str:
        return f"{self.name} is eating"

    def sleep(self) -> str:
        return f"{self.name} is sleeping"


class Duck(Animal, Flyable, Swimmable, Walkable):
    """Duck inherits from Animal and multiple mixins."""

    def __init__(self, name: str):
        super().__init__(name)

    def make_sound(self) -> str:
        return f"{self.name} quacks: Quack!"


class Penguin(Animal, Swimmable, Walkable):
    """Penguin inherits from Animal, Swimmable, and Walkable."""

    def __init__(self, name: str):
        super().__init__(name)

    def can_fly(self) -> bool:
        return False  # override

    def make_sound(self) -> str:
        return f"{self.name} honks!"


class Bat(Animal, Flyable):
    """Bat inherits from Animal and Flyable."""

    def __init__(self, name: str):
        super().__init__(name)

    def make_sound(self) -> str:
        return f"{self.name} screeches"


class FlyingFish(Animal, Flyable, Swimmable):
    """Flying fish: multiple inheritance with two mixins."""

    def __init__(self, name: str):
        super().__init__(name)

    def make_sound(self) -> str:
        return f"{self.name} makes bubble sounds"


def main():
    print("=== Duck (Fly + Swim + Walk) ===")
    duck = Duck("Donald")
    print(f"  {duck.make_sound()}")
    print(f"  {duck.fly()}")
    print(f"  {duck.swim()}")
    print(f"  {duck.walk()}")
    print(f"  {duck.eat()}")

    print("\n=== Penguin (Swim + Walk, no Fly) ===")
    penguin = Penguin("Happy")
    print(f"  {penguin.make_sound()}")
    print(f"  {penguin.swim()}")
    print(f"  {penguin.walk()}")
    print(f"  {penguin.dive(50)}")
    print(f"  Can fly? {penguin.can_fly()}")

    print("\n=== Bat (Fly only) ===")
    bat = Bat("Bruce")
    print(f"  {bat.make_sound()}")
    print(f"  {bat.fly()}")
    print(f"  {bat.land()}")

    print("\n=== Flying Fish ===")
    ff = FlyingFish("Fin")
    print(f"  {ff.make_sound()}")
    print(f"  {ff.fly()}")
    print(f"  {ff.swim()}")

    # MRO demonstration
    print(f"\n=== Method Resolution Order ===")
    print(f"Duck MRO: {[c.__name__ for c in Duck.__mro__]}")
    print(f"Penguin MRO: {[c.__name__ for c in Penguin.__mro__]}")


if __name__ == "__main__":
    main()
