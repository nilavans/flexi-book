import os
import re
from dataclasses import asdict
from tabulate import tabulate

CARD_PATTERNS = {
    "MasterCard": r"^5[1-5][0-9]{14}$|^(222[1-9]|22[3-9]\d|2[3-6]\d{2}|27[0-1]\d|2720)[0-9]{12}$",
    "Visa": r"^4[0-9]{12}(?:[0-9]{3})?$",
}


# To clear the terminal screen.
def clear() -> None:
    os.system("clr" if os.name == "nt" else "clear")


# Convert db rows to dataclass.
def map_rows_to_dataclass(cls, rows) -> list:
    return [asdict(cls(*row)) for row in rows]


def print_table(data: list[dict]) -> None:
    headers = data[0].keys()
    rows = [row.values() for row in data]
    print(tabulate(rows, headers, tablefmt="grid", maxcolwidths=[None, None, None, None, 30]))


# MasterCard (Starts with 51-55 / 2221-2720, 16 digits)
# Visa (Starts with 4, 16 digits)
def verify_card(cnum, ctype):
    card_type = "MasterCard" if ctype == 1 else "Visa" if ctype == 2 else None
    if not card_type or not re.match(CARD_PATTERNS[card_type], cnum):
        return False
    return True
