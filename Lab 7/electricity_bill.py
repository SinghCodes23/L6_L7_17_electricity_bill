RATES = {"DOM": 3, "COM": 6}
SLAB = {"A": 1, "B": 2}


def units_consumed(reading):
    """Return current - previous for a 'previous:current' string, or None if invalid."""
    if not isinstance(reading, str):
        return None
    parts = reading.split(':')
    if len(parts) != 2:
        return None
    try:
        previous, current = int(parts[0]), int(parts[1])
    except (ValueError, OverflowError):
        return None
    if previous < 0 or current < 0 or current < previous:
        return None
    return current - previous


def daily_average(units_csv):
    """Return the average of comma-separated daily units, or None if invalid."""
    if not isinstance(units_csv, str):
        return None
    try:
        units = [int(u) for u in units_csv.split(',')]
        if not units or any(u < 0 for u in units):
            return None
        return round(sum(units) / len(units), 2)
    except (ValueError, OverflowError, ZeroDivisionError):
        return None


def tariff_rate(code):
    """Return rate per unit for a 'CATEGORY-SLAB' code (e.g. DOM-A), or None if invalid."""
    if not isinstance(code, str):
        return None
    parts = code.split('-')
    if len(parts) != 2:
        return None
    category, slab = parts[0].strip().upper(), parts[1].strip().upper()
    if category not in RATES or slab not in SLAB:
        return None
    return RATES[category] * SLAB[slab]


def _show(label, value):
    print(label, value if value is not None else "Invalid input")


def main():
    print("==== Running units_consumed ====")
    user_input = input("Enter meter readings as previous:current (e.g. 1200:1350): ")
    _show("Units Consumed:", units_consumed(user_input))

    print("\n==== Running daily_average ====")
    user_input = input("Enter daily units as CSV (e.g. 5,7,6): ")
    _show("Daily Average:", daily_average(user_input))

    print("\n==== Running tariff_rate ====")
    user_input = input("Enter a tariff code (e.g. DOM-A): ")
    _show("Rate per Unit:", tariff_rate(user_input))


if __name__ == "__main__":
    main()
