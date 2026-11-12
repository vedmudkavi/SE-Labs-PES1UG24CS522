"""Lab 7: run the same property tests before and after fixing weather_alert.py.

Contract: invalid inputs return None; valid inputs retain their original results.
Run: python -m pytest test_weather_alert.py
"""

import math

import pytest
from hypothesis import given, settings, strategies as st

from weather_alert import parse_reading, rainfall_spread, wind_category

# A repeatable volume of fuzzing; Hypothesis still generates and shrinks inputs.
settings.register_profile("lab7", max_examples=300, report_multiple_bugs=False)
settings.load_profile("lab7")

unexpected = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.booleans(),
    st.lists(st.integers(), max_size=10),
    st.dictionaries(st.text(max_size=10), st.integers(), max_size=5),
    st.binary(),
)


@given(unexpected)
def test_parse_reading_no_crash(value):
    result = parse_reading(value)
    if result is not None:
        temperature, humidity = result
        assert math.isfinite(temperature)
        assert isinstance(humidity, int)
        assert 0 <= humidity <= 100


@given(unexpected)
def test_wind_category_no_crash(value):
    assert wind_category(value) in (None, "none", "advisory", "warning")


@given(unexpected)
def test_rainfall_spread_no_crash(value):
    result = rainfall_spread(value)
    if result is not None:
        assert math.isfinite(result)
        assert result >= 0


@given(
    st.floats(allow_nan=False, allow_infinity=False),
    st.integers(min_value=0, max_value=100),
)
def test_parse_reading_valid(temperature, humidity):
    assert parse_reading(f"{temperature!r}/{humidity}") == (temperature, humidity)


@given(st.one_of(
    st.tuples(st.integers(0, 38), st.just("none")),
    st.tuples(st.integers(39, 88), st.just("advisory")),
    st.tuples(st.integers(89, 10**100), st.just("warning")),
))
def test_wind_category_valid(case):
    speed, expected = case
    assert wind_category(str(speed)) == expected


@given(st.lists(
    st.floats(min_value=0, allow_nan=False, allow_infinity=False),
    min_size=1, max_size=30,
))
def test_rainfall_spread_valid(readings):
    csv = ",".join(repr(value) for value in readings)
    ordered = sorted(readings)
    assert rainfall_spread(csv) == ordered[-1] - ordered[0]
    assert rainfall_spread(",".join(repr(value) for value in reversed(readings))) == rainfall_spread(csv)


@given(st.sampled_from([
    None, "", "35.5", "35/80/90", "/80", "35/", "hot/wet",
    "nan/50", "inf/50", "-inf/50", "1e309/50", "35/-1", "35/101",
    "35/80.5", 35, True, [], {},
]))
def test_parse_reading_rejects_invalid(value):
    assert parse_reading(value) is None


@given(st.sampled_from([
    None, "", "fast", "-1", "45.5", "nan", "inf", "1e309",
    45, 45.0, True, [], {},
]))
def test_wind_category_rejects_invalid(value):
    assert wind_category(value) is None


@given(st.sampled_from([
    None, "", " ", ",", "2,,5", "2,", ",2", "wet", "-1,2",
    "nan,2", "inf,2", "-inf,2", "1e309,2", 2, True, [], {},
]))
def test_rainfall_spread_rejects_invalid(value):
    assert rainfall_spread(value) is None


@pytest.mark.parametrize("speed, expected", [
    ("0", "none"), ("38", "none"), ("39", "advisory"),
    ("88", "advisory"), ("89", "warning"),
])
def test_wind_thresholds(speed, expected):
    assert wind_category(speed) == expected


def test_whitespace_and_negative_temperature():
    assert parse_reading(" -12.5 / 80 ") == (-12.5, 80)
    assert wind_category(" 45 ") == "advisory"
    assert rainfall_spread(" 2, 5.5, 10 ") == 8.0


def test_single_rainfall_value():
    assert rainfall_spread("5.5") == 0.0
