import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert


@pytest.mark.parametrize("speed, expected", [
    (10, "none"),
    (39, "advisory"),
    (62, "watch"),
    (89, "warning"),
])
def test_wind_levels(speed, expected):
    assert wind_alert(speed) == expected


@pytest.mark.parametrize("rain, saturated, expected", [
    (5, False, "none"),
    (10, False, "advisory"),
    (10, True, "watch"),
    (50, False, "watch"),
    (50, True, "warning"),
])
def test_rain_levels(rain, saturated, expected):
    assert rain_alert(rain, saturated) == expected


@pytest.mark.parametrize("temperature, humidity, expected", [
    (30, 40, "none"),
    (34, 50, "advisory"),
    (39, 50, "watch"),
    (44, 50, "warning"),
])
def test_heat_levels(temperature, humidity, expected):
    assert heat_alert(temperature, humidity) == expected


def test_overall_highest_alert():
    assert overall_alert(["advisory", "watch", "warning"]) == "warning"


def test_overall_invalid_alert():
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["invalid"])
