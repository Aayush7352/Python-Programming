class BankAccount:
    """Demonstrates encapsulation with public, protected, and private members."""

    def __init__(self, owner: str, initial_balance: float = 0):
        self.owner = owner                    # public
        self._branch_code = "XYZ-123"         # protected (convention: _prefix)
        self.__balance = initial_balance      # private (name mangling: __prefix)
        self.__transaction_history: list = [] # private

    # Public methods (API)
    def deposit(self, amount: float) -> str:
        if amount <= 0:
            return "Deposit amount must be positive"
        self.__balance += amount
        self.__add_transaction("deposit", amount)
        return f"Deposited ${amount:.2f}. New balance: ${self.__balance:.2f}"

    def withdraw(self, amount: float) -> str:
        if amount <= 0:
            return "Withdrawal amount must be positive"
        if amount > self.__balance:
            return f"Insufficient funds. Current balance: ${self.__balance:.2f}"
        self.__balance -= amount
        self.__add_transaction("withdraw", amount)
        return f"Withdrew ${amount:.2f}. New balance: ${self.__balance:.2f}"

    def get_balance(self) -> float:
        """Controlled access to private balance."""
        return self.__balance

    def get_transaction_history(self, count: int = 5) -> list:
        """Limited view of transaction history."""
        return self.__transaction_history[-count:]

    # Protected method
    def _apply_interest(self, rate: float) -> None:
        """Protected: meant for subclasses."""
        interest = self.__balance * rate
        self.__balance += interest
        self.__add_transaction("interest", interest)

    # Private method
    def __add_transaction(self, txn_type: str, amount: float) -> None:
        """Private: internal bookkeeping."""
        self.__transaction_history.append({
            "type": txn_type,
            "amount": amount,
            "balance_after": self.__balance,
        })

    def __repr__(self) -> str:
        return f"BankAccount(owner='{self.owner}', balance=${self.__balance:.2f})"


class SavingsAccount(BankAccount):
    """Subclass demonstrating access to protected members."""

    def __init__(self, owner: str, initial_balance: float = 0):
        super().__init__(owner, initial_balance)
        self._interest_rate = 0.02  # 2% annual interest

    def add_interest(self) -> str:
        """Uses protected method from parent."""
        self._apply_interest(self._interest_rate)
        return f"Interest applied at {self._interest_rate*100}%"


def main():
    print("=== Encapsulation Demo ===")
    account = BankAccount("Alice", 1000)
    print(f"Account: {account}")

    print("\n=== Public Interface ===")
    print(account.deposit(500))
    print(account.withdraw(200))
    print(account.withdraw(2000))  # Insufficient funds

    print(f"\n=== Controlled Access ===")
    print(f"Balance: ${account.get_balance():.2f}")
    print(f"Recent transactions: {account.get_transaction_history(3)}")

    print("\n=== Access Levels ===")
    print(f"Public (owner): {account.owner}")
    print(f"Protected (_branch_code): {account._branch_code}")  # Accessible but discouraged

    # Private member access via name mangling
    print(f"\nPrivate via name mangling: {account._BankAccount__balance}")

    # This would fail:
    # print(account.__balance)  # AttributeError

    print("\n=== Inheritance and Encapsulation ===")
    savings = SavingsAccount("Bob", 2000)
    print(f"Initial: ${savings.get_balance():.2f}")
    print(savings.add_interest())
    print(f"After interest: ${savings.get_balance():.2f}")

    # Name mangling for private members in subclasses
    print(f"\nPrivate member access from subclass:")
    print(f"  savings._BankAccount__balance: ${savings._BankAccount__balance:.2f}")


if __name__ == "__main__":
    main()
