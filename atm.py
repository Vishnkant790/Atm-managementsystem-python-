import os

MIN_BALANCE = 500          # minimum balance that must always remain in the account
MAX_PIN_ATTEMPTS = 3       # account locks after this many wrong PIN attempts


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


class Atm:
    def __init__(self):
        # private-style attributes (Python convention: leading underscore)
        self._account_no = None
        self._name = None
        self._pin = None
        self._balance = 0.0
        self._phone_no = None
        self._failed_attempts = 0
        self._locked = False

    def setdata(self, account_no, name, pin, balance, phone_no,
                failed_attempts=0, locked=False):
        self._account_no = account_no
        self._name = name
        self._pin = pin
        self._balance = balance
        self._phone_no = phone_no
        self._failed_attempts = failed_attempts
        self._locked = locked

    def get_account_no(self):
        return self._account_no

    def get_name(self):
        return self._name

    def get_pin(self):
        return self._pin

    def get_balance(self):
        return self._balance

    def get_phone_no(self):
        return self._phone_no

    def is_locked(self):
        return self._locked

    def check_pin(self, entered_pin):
        """Verify PIN, tracking failed attempts and locking after too many."""
        if self._locked:
            return False

        if entered_pin == self._pin:
            self._failed_attempts = 0  # reset on success
            return True

        self._failed_attempts += 1
        if self._failed_attempts >= MAX_PIN_ATTEMPTS:
            self._locked = True
        return False

    def remaining_attempts(self):
        return MAX_PIN_ATTEMPTS - self._failed_attempts

    def set_phone(self, old_phone, new_phone):
        if old_phone == self._phone_no:
            self._phone_no = new_phone
            print("\nSuccessfully Updated")
        else:
            print("\nIncorrect Phone Number")
        pause()

    def change_pin(self, old_pin, new_pin):
        if old_pin != self._pin:
            print("\nIncorrect Current PIN")
        elif len(str(new_pin)) != 4:
            print("\nPIN must be exactly 4 digits")
        else:
            self._pin = new_pin
            print("\nPIN Changed Successfully")
        pause()

    def cash_withdraw(self, amount):
        if amount <= 0:
            print("\nInvalid Input")
        elif self._balance - amount < MIN_BALANCE:
            print(f"\nInsufficient Balance: A minimum balance of {MIN_BALANCE} must be maintained")
        else:
            self._balance -= amount
            print("\nPlease Collect Your Cash")
            print(f"Available Balance: {self._balance}")
        pause()

    def cash_deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\nDone!")
            print(f"Available Balance: {self._balance}")
        else:
            print("\nInvalid Input")
        pause()


# ---------- INHERITANCE + POLYMORPHISM ----------
class SavingsAccount(Atm):
    """A savings account must always keep at least MIN_BALANCE in it."""

    def cash_withdraw(self, amount):
        if amount <= 0:
            print("\nInvalid Input")
        elif self._balance - amount < MIN_BALANCE:
            print(f"\n[Savings Account] Denied: a minimum balance of {MIN_BALANCE} must be maintained")
        else:
            self._balance -= amount
            print("\n[Savings Account] Please Collect Your Cash")
            print(f"Available Balance: {self._balance}")
        pause()


class CurrentAccount(Atm):
    """A current (business) account is allowed to go into overdraft."""

    OVERDRAFT_LIMIT = -10000  # balance is allowed to go this low

    def cash_withdraw(self, amount):
        if amount <= 0:
            print("\nInvalid Input")
        elif self._balance - amount < self.OVERDRAFT_LIMIT:
            print(f"\n[Current Account] Denied: overdraft limit of {self.OVERDRAFT_LIMIT} exceeded")
        else:
            self._balance -= amount
            print("\n[Current Account] Please Collect Your Cash")
            print(f"Available Balance: {self._balance} (overdraft allowed up to {self.OVERDRAFT_LIMIT})")
        pause()


def read_int(prompt):
    """Safe integer input (handles bad input instead of crashing)."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def create_account(accounts):
    """Ask the user for details and register a brand new account in RAM."""
    clear_screen()
    print("\n******Create New Account******\n")

    account_no = read_int("Choose an Account Number: ")
    if account_no in accounts:
        print("\nAn account with this number already exists. Please try again.")
        pause()
        return

    name = input("Enter Your Name: ")
    pin = read_int("Set a 4-digit PIN: ")
    balance = read_int("Enter Initial Deposit Amount: ")
    phone_no = input("Enter Phone Number: ")

    print("\nSelect Account Type")
    print("1. Savings Account (minimum balance rule)")
    print("2. Current Account (overdraft allowed)")
    acc_type = read_int("Enter choice: ")

    # Polymorphism: which class we instantiate decides how cash_withdraw()
    # will behave later, even though the rest of the program treats every
    # account the exact same way.
    if acc_type == 2:
        new_user = CurrentAccount()
    else:
        new_user = SavingsAccount()

    new_user.setdata(account_no, name, pin, balance, phone_no)
    accounts[account_no] = new_user

    print(f"\nAccount created successfully! Your Account Number is {account_no}")
    pause()


def login(accounts):
    """Ask for account number + PIN and return the matching account object, or None."""
    clear_screen()
    print("\n******Welcome to ATM******\n")

    enter_account_no = read_int("Enter Account Number: ")
    user1 = accounts.get(enter_account_no)

    if user1 is None:
        print("\nUser Details are Invalid")
        pause()
        return None

    if user1.is_locked():
        print("\nThis account is LOCKED due to too many failed PIN attempts.")
        print("Please contact bank support.")
        pause()
        return None

    enter_pin = read_int("\nEnter ATM PIN: ")

    if not user1.check_pin(enter_pin):
        if user1.is_locked():
            print("\nIncorrect PIN. Account is now LOCKED due to too many failed attempts.")
        else:
            print(f"\nIncorrect PIN. Attempts remaining: {user1.remaining_attempts()}")
        pause()
        return None

    return user1


def main():
    # In-memory "database" of accounts: {account_no: Atm/SavingsAccount/CurrentAccount object}
    # NOTE: everything lives in RAM only — data resets every time the program restarts.
    accounts = {}

    # A ready-made demo account, so login still works out of the box.
    demo_user = SavingsAccount()
    demo_user.setdata(1234567, "ABC", 4321, 9999.90, "9638527410")
    accounts[1234567] = demo_user

    while True:  # outer loop: create account or login
        clear_screen()
        print("\n******Welcome to ATM******\n")
        print("1. Login")
        print("2. Create New Account")
        print("3. Exit\n")
        start_choice = read_int("Enter choice: ")

        if start_choice == 2:
            create_account(accounts)
            continue
        elif start_choice == 3:
            exit(0)

        user1 = login(accounts)
        if user1 is None:
            continue  # login failed, go back to the start menu

        # Successful login
        while True:  # menu loop (like C++ inner do-while)
            clear_screen()
            print("\n******Welcome to ATM******\n")
            print("Select Options")
            print("1. Check Balance")
            print("2. Cash Withdraw")
            print("3. Show User details")
            print("4. Update Phone Number")
            print("5. Deposit Cash")
            print("6. Exit")
            print("7. Change PIN\n")

            choice = read_int("Enter choice: ")

            if choice == 1:
                print(f"\nYour Balance is: {user1.get_balance()}")
                pause()

            elif choice == 2:
                amount = read_int("\nEnter Amount: ")
                user1.cash_withdraw(amount)

            elif choice == 3:
                print("\nUser Details:-")
                print(f"-> Account Number: {user1.get_account_no()}")
                print(f"-> Account Name: {user1.get_name()}")
                print(f"-> Balance: {user1.get_balance()}")
                print(f"-> Phone Number: {user1.get_phone_no()}")
                pause()

            elif choice == 4:
                old_phone = input("\nEnter Old Phone Number: ")
                new_phone = input("\nEnter New Phone Number: ")
                user1.set_phone(old_phone, new_phone)

            elif choice == 5:
                amount = read_int("\nEnter Amount: ")
                user1.cash_deposit(amount)

            elif choice == 6:
                print("\nLogging out...")
                pause()
                break  # go back to the start menu (Login / Create Account)

            elif choice == 7:
                old_pin = read_int("\nEnter Current PIN: ")
                new_pin = read_int("Enter New 4-digit PIN: ")
                user1.change_pin(old_pin, new_pin)

            else:
                print("Enter Valid Data")
                pause()


if __name__ == "__main__":
    main()