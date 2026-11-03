  import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status


@pytest.mark.parametrize("plan,data,roaming,loyal,expected", [
    ("basic", 2, False, False, 0),
    ("basic", 3, False, False, 15),
    ("standard", 5, False, False, 0),
    ("standard", 7, False, True, 15),
    ("premium", 10, False, False, 0),
    ("basic", 15, True, False, 715),
    ("basic", 13, False, False, 275),
    ("basic", 14, True, False, 660),
])
def test_overage_charge(plan, data, roaming, loyal, expected):
    assert overage_charge(plan, data, roaming, loyal) == expected


@pytest.mark.parametrize("plan,data,roaming,loyal", [
    ("unknown", 1, False, False),
    ("basic", -1, False, False),
])
def test_overage_errors(plan, data, roaming, loyal):
    with pytest.raises(ValueError):
        overage_charge(plan, data, roaming, loyal)


@pytest.mark.parametrize("amount,pending,kyc,expected", [
    (100, 0, False, True),
    (2001, 0, False, False),
    (500, 3, False, False),
    (200, 10, True, True),
    (201, 0, True, False),
])
def test_recharge(amount, pending, kyc, expected):
    assert recharge_allowed(amount, pending, kyc) == expected


@pytest.mark.parametrize("days,prepaid,addon,expected", [
    (0, True, False, "active"),
    (-1, True, False, "grace"),
    (-15, True, False, "grace"),
    (-16, True, False, "expired"),
    (3, False, False, "active"),
    (-12, False, False, "grace"),
    (-13, False, False, "expired"),
    (5, False, True, "active"),
])
def test_validity(days, prepaid, addon, expected):
    assert validity_status(days, prepaid, addon) == expected
