"""Compound interest calculator.

Shows how much you would have if you invest the same amount every month.
Run it with:  python calculator.py
"""

import webbrowser
from pathlib import Path


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


def save_chart(rows, filename="chart.html"):
    """Draw a bar chart of the balance each year and save it as a web page."""
    width, height, pad = 720, 360, 60
    top = max(balance for _, _, balance in rows)
    slot = (width - 2 * pad) / len(rows)
    bars = []
    for i, (year, invested, balance) in enumerate(rows):
        x = pad + i * slot + slot * 0.15
        w = slot * 0.7
        h_bal = balance / top * (height - 2 * pad)
        h_inv = invested / top * (height - 2 * pad)
        base = height - pad
        bars.append(
            f'<rect x="{x:.1f}" y="{base - h_bal:.1f}" width="{w:.1f}" height="{h_bal:.1f}" fill="#2e9e6b">'
            f'<title>Year {year}: ${balance:,.0f}</title></rect>'
            f'<rect x="{x:.1f}" y="{base - h_inv:.1f}" width="{w:.1f}" height="{h_inv:.1f}" fill="#3b6fd8">'
            f'<title>Year {year}: you put in ${invested:,.0f}</title></rect>'
            f'<text x="{x + w / 2:.1f}" y="{base + 18}" text-anchor="middle" font-size="12">{year}</text>'
        )
    page = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Investment growth</title></head>
<body style="font-family: sans-serif; max-width: 760px; margin: 40px auto;">
<h2>Your money over {rows[-1][0]} years</h2>
<p><span style="color:#3b6fd8">&#9632;</span> What you put in &nbsp;
<span style="color:#2e9e6b">&#9632;</span> Growth on top</p>
<svg width="{width}" height="{height}" style="max-width:100%">
<line x1="{pad}" y1="{height - pad}" x2="{width - pad}" y2="{height - pad}" stroke="#888"/>
<text x="{pad}" y="{pad - 10}" font-size="12">${top:,.0f}</text>
{''.join(bars)}
<text x="{width / 2}" y="{height - 15}" text-anchor="middle" font-size="12">Year</text>
</svg>
<p>Hover over a bar to see the exact amount.</p>
</body></html>"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(page)
    return Path(filename).resolve()


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

        path = save_chart(rows)
        print(f"\nChart saved to {path} - opening it in your browser...")
        webbrowser.open(path.as_uri())
    print("\n(Real returns go up and down each year - this assumes a steady rate.)")


if __name__ == "__main__":
    main()
