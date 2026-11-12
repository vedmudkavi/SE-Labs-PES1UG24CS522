"""Weather alert classifier hardened through Hypothesis fuzz testing.

All three functions accept strings and return None for invalid input.
Temperature must be finite; humidity must be an integer from 0 to 100.
Wind speed must be a nonnegative integer. Rainfall values must be finite
and nonnegative. Surrounding whitespace is allowed.
"""

import math


def parse_reading(text):
    """Return (temperature, humidity), or None for an invalid reading."""
    if not isinstance(text, str):
        return None
    parts = text.split("/")
    if len(parts) != 2:
        return None
    try:
        temperature = float(parts[0])
        humidity = int(parts[1])
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(temperature) or not 0 <= humidity <= 100:
        return None
    return temperature, humidity


def wind_category(speed_text):
    """Return the wind category, or None for an invalid speed.

    Original boundaries are preserved: 0-38 none, 39-88 advisory,
    and 89 or more warning, with speed measured in km/h.
    """
    if not isinstance(speed_text, str):
        return None
    try:
        speed = int(speed_text)
    except (ValueError, OverflowError):
        return None
    if speed < 0:
        return None
    if speed >= 89:
        return "warning"
    if speed >= 39:
        return "advisory"
    return "none"


def rainfall_spread(readings_csv):
    """Return the range of a nonempty rainfall CSV, or None if invalid."""
    if not isinstance(readings_csv, str):
        return None
    try:
        readings = [float(value) for value in readings_csv.split(",")]
    except (ValueError, OverflowError):
        return None
    if any(not math.isfinite(value) or value < 0 for value in readings):
        return None
    return max(readings) - min(readings)


def main():
    print("==== Running parse_reading ====")
    user_input = input("Enter temperature/humidity (e.g. 35.5/80): ")
    result = parse_reading(user_input)
    if result is None:
        print("Invalid reading: use a finite temperature / integer humidity (0-100).")
    else:
        print("Temperature and Humidity:", result)

    print("\n==== Running wind_category ====")
    user_input = input("Enter a wind speed in km/h (e.g. 45): ")
    result = wind_category(user_input)
    if result is None:
        print("Invalid wind speed: enter a nonnegative integer.")
    else:
        print("Wind Category:", result)

    print("\n==== Running rainfall_spread ====")
    user_input = input("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): ")
    result = rainfall_spread(user_input)
    if result is None:
        print("Invalid rainfall: enter finite, nonnegative numbers separated by commas.")
    else:
        print("Rainfall Spread:", result)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
