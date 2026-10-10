from typing import Dict

def open_account(balances: Dict[str,int], name: str, amount: int) -> None:
    balances[name] = amount

def sum_balances(accounts: Dict[str,int]) -> int:
    total = 0
    for name, pence in accounts.items():
        print(f"{name} had balance {pence}")
        total += pence
    return total

def format_pence_as_string(total_pence: int) -> str:
    if total_pence < 100:
        return f"{total_pence}p"
    pounds = int(total_pence / 100)
    pence = total_pence % 100
    return f"£{pounds}.{pence:02d}"

balances = {
    "Sima": 700,
    "Linn": 545,
    "Georg": 831,
}

open_account(balances, "Tobi", 913)
open_account(balances, "Olya", 713)

total_pence = sum_balances(balances)
total_string = format_pence_as_string(total_pence)

print(f"The bank accounts total {total_string}")

# TASK 4
# This code contains bugs related to types. They are bugs mypy can catch.
# Read this code to understand what it's trying to do.
# Add type annotations to the method parameters and return types of this code.
# Run the code through mypy, and fix all of the bugs that show up.
# When you're confident all of the type annotations are correct, and the bugs are fixed, run the code and check it works.
