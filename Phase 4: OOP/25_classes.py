class Car:
    """A simple Car class."""
    wheels = 4  # class attribute

    def __init__(self, make: str, model: str, year: int):
        self.make = make
        self.model = model
        self.year = year
        self._mileage = 0

    def drive(self, miles: int) -> None:
        if miles <= 0:
            raise ValueError("Miles must be positive")
        self._mileage += miles
        print(f"Driven {miles} miles. Total: {self._mileage}")

    def info(self) -> str:
        return f"{self.year} {self.make} {self.model} with {self._mileage} miles"

    @classmethod
    def from_string(cls, car_string: str):
        make, model, year = car_string.split(",")
        return cls(make.strip(), model.strip(), int(year.strip()))

    @staticmethod
    def is_vintage(year: int) -> bool:
        return year < 1990

    def __repr__(self) -> str:
        return f"Car(make='{self.make}', model='{self.model}', year={self.year})"


def main():
    # Creating instances
    car1 = Car("Toyota", "Camry", 2022)
    car2 = Car("Honda", "Accord", 2023)

    print("=== Class Attributes ===")
    print(f"All cars have {Car.wheels} wheels")
    print(f"car1 wheels: {car1.wheels}")

    print("\n=== Instance Methods ===")
    print(car1.info())
    car1.drive(50)
    print(car1.info())

    print("\n=== Class Method ===")
    car3 = Car.from_string("Ford, Mustang, 1965")
    print(car3.info())

    print("\n=== Static Method ===")
    print(f"Is 1965 vintage? {Car.is_vintage(1965)}")
    print(f"Is 2023 vintage? {Car.is_vintage(2023)}")

    print(f"\n=== repr ===")
    print(repr(car1))
    print(repr(car2))


if __name__ == "__main__":
    main()
