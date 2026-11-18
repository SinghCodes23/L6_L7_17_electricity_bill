import pytest
from electricity_bill import energy_charge, late_fee, subsidy


# ---------- energy_charge ----------
def test_low_usage_domestic():
    assert energy_charge(50, "domestic") == 200

def test_zero_units():
    assert energy_charge(0, "domestic") == 50

def test_slab1_upper_boundary():
    assert energy_charge(100, "domestic") == 350

def test_slab2_lower_boundary():
    assert energy_charge(101, "domestic") == 355

def test_slab2_upper_boundary():
    assert energy_charge(300, "domestic") == 1350

def test_slab3_lower_boundary():
    assert energy_charge(301, "domestic") == 1358

def test_high_slab_domestic():
    assert energy_charge(400, "domestic") == 2150

def test_commercial_low_slab():
    assert energy_charge(50, "commercial") == 450

def test_commercial_high_slab():
    # 2100 * 2 = 4200, + 150 fixed
    assert energy_charge(400, "commercial") == 4350

def test_unknown_connection_raises():
    with pytest.raises(ValueError, match="unknown connection"):
        energy_charge(50, "industrial")

def test_negative_units_raises():
    with pytest.raises(ValueError, match="invalid units"):
        energy_charge(-1, "domestic")


# ---------- late_fee ----------
def test_paid_on_time():
    assert late_fee(500, 0) == 0

def test_negative_days_late():
    assert late_fee(500, -3) == 0

def test_one_day_late():
    assert late_fee(500, 1) == 50

def test_fifteen_days_late_boundary():
    assert late_fee(500, 15) == 50

def test_sixteen_days_late_small_bill():
    assert late_fee(500, 16) == 100

def test_bill_exactly_2000_no_extra():
    assert late_fee(2000, 16) == 100

def test_bill_above_2000_extra_fee():
    # 100 + 2001//20 = 200
    assert late_fee(2001, 16) == 200

def test_late_over_15_days_large_bill():
    assert late_fee(4000, 20) == 300


# ---------- subsidy ----------
def test_senior_low_usage():
    assert subsidy(100, True, False) == 50

def test_senior_just_over_100_units():
    assert subsidy(101, True, False) == 0

def test_not_senior_no_solar():
    assert subsidy(50, False, False) == 0

def test_solar_only():
    assert subsidy(50, False, True) == 100

def test_senior_and_solar_stack():
    assert subsidy(50, True, True) == 150

def test_solar_at_300_units_keeps_subsidy():
    assert subsidy(300, False, True) == 100

def test_solar_over_300_units_cancels():
    assert subsidy(301, False, True) == 0

def test_senior_over_300_no_solar():
    assert subsidy(301, True, False) == 0
