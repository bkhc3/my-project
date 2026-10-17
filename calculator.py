"""Compound interest calculator.

Shows how much you would have if you invest the same amount every month.
Run it with:  python calculator.py
"""


def ask_number(question, default):
    """Ask the user for a number. Pressing Enter uses the default."""
    while True:
        answer = input(f"{question} [{default}]: ").strip()
        if answer == "":
            return default
        try:
            return float(answer.replace(",", "").replace("$", ""))
        except ValueError:
            print("  Please type a number, e.g. 500")


def grow(monthly, yearly_rate, years):
    """Return a list of (year, total_invested, balance) for each year."""
    monthly_rate = yearly_rate / 100 / 12
    balance = 0.0
    rows = []
    for month in range(1, int(years * 12) + 1):
        balance = balance * (1 + monthly_rate) + monthly
        if month % 12 == 0:
            rows.append((month // 12, monthly * month, balance))
    return rows


def main():
    print("=== Compound Interest Calculator ===\n")
    monthly = ask_number("How much will you invest each month ($)?", 500)
    rate = ask_number("Expected yearly return (%)?", 7)
    years = ask_number("For how many years?", 10)

    rows = grow(monthly, rate, years)

    print(f"\n{'Year':>4}  {'You put in':>14}  {'Balance':>14}  {'Growth':>14}")
    print("-" * 52)
    for year, invested, balance in rows:
        print(f"{year:>4}  ${invested:>13,.0f}  ${balance:>13,.0f}  ${balance - invested:>13,.0f}")

    if rows:
        _, invested, balance = rows[-1]
        print(f"\nAfter {rows[-1][0]} years you put in ${invested:,.0f} "
              f"and end up with ${balance:,.0f}.")
        print(f"That's ${balance - invested:,.0f} from growth.")
    print("\n(Real returns go up and down each year - this assumes a steady rate.)")


if __name__ == "__main__":
    main()
