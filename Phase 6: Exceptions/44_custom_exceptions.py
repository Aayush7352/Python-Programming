class BankAccountError(Exception):
    """Base exception for bank account errors."""
    pass


class InsufficientFundsError(BankAccountError):
    """Raised when withdrawal amount exceeds balance."""

    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        self.deficit = amount - balance
        super().__init__(
            f"Insufficient funds: balance=${balance:.2f}, "
            f"withdrawal=${amount:.2f}, deficit=${self.deficit:.2f}"
        )


class NegativeAmountError(BankAccountError):
    """Raised when a negative amount is used."""

    def __init__(self, amount: float, operation: str):
        self.amount = amount
        self.operation = operation
        super().__init__(
            f"Cannot {operation} negative amount: ${amount:.2f}"
        )


class AccountLockedError(BankAccountError):
    """Raised when trying to operate on a locked account."""

    def __init__(self, account_id: str):
        self.account_id = account_id
        super().__init__(f"Account {account_id} is locked")


class ValidationError(Exception):
    """Custom validation error with field-level details."""

    def __init__(self, message: str, field: str = None, value=None):
        self.field = field
        self.value = value
        super().__init__(message)

    def __repr__(self):
        return (
            f"ValidationError(field={self.field!r}, "
            f"value={self.value!r}, message={self.args[0]!r})"
        )


def validate_age(age: int) -> int:
    """Validate age with custom exception."""
    if not isinstance(age, int):
        raise ValidationError("Age must be an integer", field="age", value=age)
    if age < 0:
        raise ValidationError("Age cannot be negative", field="age", value=age)
    if age > 150:
        raise ValidationError("Age exceeds maximum", field="age", value=age)
    return age


def validate_email(email: str) -> str:
    """Basic email validation."""
    if "@" not in email:
        raise ValidationError("Email must contain @", field="email", value=email)
    if "." not in email.split("@")[-1]:
        raise ValidationError("Email domain must contain .", field="email", value=email)
    return email


class BankAccount:
    """Bank account using custom exceptions."""

    def __init__(self, account_id: str, owner: str, initial_balance: float = 0):
        if initial_balance < 0:
            raise NegativeAmountError(initial_balance, "create account with")
        self.account_id = account_id
        self.owner = owner
        self._balance = initial_balance
        self._locked = False

    def deposit(self, amount: float) -> float:
        if self._locked:
            raise AccountLockedError(self.account_id)
        if amount <= 0:
            raise NegativeAmountError(amount, "deposit")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        if self._locked:
            raise AccountLockedError(self.account_id)
        if amount <= 0:
            raise NegativeAmountError(amount, "withdraw")
        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)
        self._balance -= amount
        return self._balance

    def lock(self):
        self._locked = True

    @property
    def balance(self) -> float:
        return self._balance


def main():
    print("=== Custom Exceptions ===")

    # Basic custom exception
    print("\n1. BankAccount with custom exceptions:")
    account = BankAccount("ACC-001", "Alice", 1000)
    print(f"   Created: {account.owner}, ${account.balance}")

    try:
        account.withdraw(2000)
    except InsufficientFundsError as e:
        print(f"   Caught: {e}")

    try:
        account.deposit(-50)
    except NegativeAmountError as e:
        print(f"   Caught: {e}")

    # Account locked
    account.lock()
    try:
        account.withdraw(100)
    except AccountLockedError as e:
        print(f"   Caught: {e}")

    # Validation with custom exceptions
    print("\n2. Validation with custom exceptions:")
    try:
        validate_age(-5)
    except ValidationError as e:
        print(f"   Caught: {e}")
        print(f"   Field: {e.field}, Value: {e.value}")

    try:
        validate_email("invalid-email")
    except ValidationError as e:
        print(f"   Caught: {e}")

    # Exception hierarchy
    print("\n3. Exception hierarchy:")
    print(f"   InsufficientFundsError is BankAccountError: "
          f"{issubclass(InsufficientFundsError, BankAccountError)}")
    print(f"   BankAccountError is Exception: "
          f"{issubclass(BankAccountError, Exception)}")


if __name__ == "__main__":
    main()
