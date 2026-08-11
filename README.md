# ATM Management System (Python)

A console-based ATM simulation built in Python with an OOP design. All
account data is stored in memory while the program runs — originally
started as a C++ concept and rebuilt from the ground up in Python.

## Features

- **Multi-account support** — create as many accounts as you like, each with
  its own account number, PIN, balance, and phone number.
- **Two account types** — Savings (enforces a minimum balance) and Current
  (allows overdraft up to a limit), implemented via inheritance and
  polymorphism.
- **PIN security** — accounts automatically lock after 3 failed PIN attempts.
- **Change PIN** — users can update their own PIN after verifying the old one.
- **Minimum balance protection** — savings accounts can't be withdrawn below
  a configurable minimum balance.
- **Phone number update**, **cash withdrawal**, **cash deposit**, and
  **balance/details lookup**.

## Tech Stack

- Python 3 (standard library only — no external dependencies)

## Project Structure

```
ATM-Python-Project/
├── atm.py     # Main program: ATM classes, menu, business logic
└── README.md
```

## Setup

1. Make sure Python 3 is installed.
2. Run the program:
   ```bash
   python atm.py
   ```
3. A demo account is preloaded (Account No: `1234567`, PIN: `4321`) so you
   can log in right away, or create a new account from the main menu.

**Note:** data is stored in memory only — it resets every time the program
is restarted (except the built-in demo account).

## Design Notes

- `Atm` is the base class holding shared account behavior (getters, PIN
  checks, deposits, phone updates).
- `SavingsAccount` and `CurrentAccount` inherit from `Atm` and override
  `cash_withdraw()` with their own withdrawal rules — a practical example of
  inheritance and polymorphism.
- All accounts live in a single in-memory dictionary (`accounts`) for the
  duration of the program's run.

## Background

This project began as a study of a simpler C++ console ATM concept and was
rebuilt independently in Python with a different architecture (multi-account
support, account-type polymorphism, and PIN lockout security) that the
original did not have.
