import pytest
from electricity_bill import energy_charge, late_fee, subsidy


# ---------- energy_charge ----------
def test_low_usage_domestic():
    assert energy_charge(50, "domestic") == 200

def test_mid_slab_domestic():
    # 300 + (200-100)*5 = 800, + 50 fixed
    assert energy_charge(200, "domestic") == 850

def test_high_slab_domestic():
    # 1300 + (400-300)*8 = 2100, + 50 fixed
    assert energy_charge(400, "domestic") == 2150

def test_commercial_doubles_charge():
    # 50*3 = 150, *2 = 300, + 150 fixed
    assert energy_charge(50, "commercial") == 450

def test_unknown_connection_raises():
    with pytest.raises(ValueError):
        energy_charge(50, "industrial")

def test_negative_units_raises():
    with pytest.raises(ValueError):
        energy_charge(-1, "domestic")


# ---------- late_fee ----------
def test_paid_on_time():
    assert late_fee(500, 0) == 0

def test_late_up_to_15_days():
    assert late_fee(500, 10) == 50

def test_late_over_15_days_large_bill():
    # 100 + 4000//20 = 300
    assert late_fee(4000, 20) == 300


# ---------- subsidy ----------
def test_senior_low_usage():
    assert subsidy(80, True, False) == 50

def test_solar_only():
    assert subsidy(200, False, True) == 100

def test_solar_high_usage_cancels_subsidy():
    assert subsidy(400, False, True) == 0
