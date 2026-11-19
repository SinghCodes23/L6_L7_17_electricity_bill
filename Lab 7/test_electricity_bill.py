from hypothesis import given, strategies as st
from electricity_bill import units_consumed, daily_average, tariff_rate


@given(st.text() | st.none())
def test_units_consumed_no_crash(s):
    try:
        units_consumed(s)
    except Exception as e:
        assert False, f"units_consumed crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_daily_average_no_crash(s):
    try:
        daily_average(s)
    except Exception as e:
        assert False, f"daily_average crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_tariff_rate_no_crash(s):
    try:
        tariff_rate(s)
    except Exception as e:
        assert False, f"tariff_rate crashed with: {e!r} for input {s!r}"


# Extra sanity checks: valid inputs still work, invalid ones return None
def test_valid_inputs():
    assert units_consumed("1200:1350") == 150
    assert daily_average("5,7,6") == 6.0
    assert tariff_rate("DOM-A") == 3
    assert tariff_rate("com-b") == 12


def test_invalid_inputs():
    assert units_consumed("1350:1200") is None
    assert units_consumed("abc") is None
    assert daily_average("") is None
    assert daily_average("1,,3") is None
    assert tariff_rate("XYZ-A") is None
    assert tariff_rate("DOM") is None
