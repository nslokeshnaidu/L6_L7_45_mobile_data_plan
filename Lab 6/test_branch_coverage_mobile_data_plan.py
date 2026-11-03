import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status


@pytest.mark.parametrize("plan,data,roaming,loyal,expected", [
    ("basic", 1, False, False, 0),
    ("basic", 4, False, False, 30),
    ("basic", 12, True, False, 400),
    ("basic", 13, True, False, 605),
    ("standard", 6, False, True, 0),
    ("premium", 12, False, True, 30),
])
def test_overage_branches(plan, data, roaming, loyal, expected):
    assert overage_charge(plan, data, roaming, loyal) == expected


def test_invalid_plan():
    with pytest.raises(ValueError):
        overage_charge("invalid", 1, False, False)


def test_invalid_usage():
    with pytest.raises(ValueError):
        overage_charge("basic", -1, False, False)


@pytest.mark.parametrize("amount,pending,kyc,expected", [
    (200, 0, True, True),
    (201, 0, True, False),
    (2000, 2, False, True),
    (2001, 2, False, False),
    (100, 3, False, False),
])
def test_recharge_branches(amount, pending, kyc, expected):
    assert recharge_allowed(amount, pending, kyc) == expected


@pytest.mark.parametrize("days,prepaid,addon,expected", [
    (0, True, False, "active"),
    (-1, True, False, "grace"),
    (-16, True, False, "expired"),
    (3, False, False, "active"),
    (-12, False, False, "grace"),
    (-13, False, False, "expired"),
    (2, True, True, "active"),
    (-10, False, True, "grace"),
    (-11, False, True, "expired"),
])
def test_validity_branches(days, prepaid, addon, expected):
    assert validity_status(days, prepaid, addon) == expected
