import pytest
from mobile_data_plan import (
    overage_charge,
    recharge_allowed,
    validity_status
)

# 1. Overage Charge Tests

def test_within_included_data():
    assert overage_charge("standard", 3, False, False) == 0

def test_basic_plan_overage():
    assert overage_charge("basic", 4, False, False) == 30

def test_loyal_customer():
    assert overage_charge("basic", 3, False, True) == 0

def test_premium_loyal_customer():
    assert overage_charge("premium", 11, False, True) == 15

def test_roaming_charge():
    assert overage_charge("standard", 7, True, False) == 80

def test_high_data_usage():
    assert overage_charge("standard", 16, False, False) == 275

def test_high_roaming_charge():
    assert overage_charge("standard", 16, True, False) == 605

def test_unknown_plan():
    with pytest.raises(ValueError):
        overage_charge("gold", 5, False, False)

def test_negative_data_usage():
    with pytest.raises(ValueError):
        overage_charge("basic", -1, False, False)


# 2. Recharge Allowed Tests

def test_recharge_allowed():
    assert recharge_allowed(500, 1, False) is True

def test_kyc_pending_allowed():
    assert recharge_allowed(200, 5, True) is True

def test_kyc_pending_rejected():
    assert recharge_allowed(201, 1, True) is False

def test_recharge_above_limit():
    assert recharge_allowed(2001, 1, False) is False

def test_max_pending_recharges():
    assert recharge_allowed(2000, 2, False) is True

def test_too_many_pending_recharges():
    assert recharge_allowed(500, 3, False) is False


# 3. Validity Status Tests

def test_validity_active():
    assert validity_status(5, True, False) == "active"

def test_validity_grace():
    assert validity_status(-5, True, False) == "grace"

def test_validity_expired():
    assert validity_status(-16, True, False) == "expired"

def test_postpaid_active():
    assert validity_status(3, False, False) == "active"

def test_addon_active():
    assert validity_status(5, False, True) == "active"

def test_addon_grace():
    assert validity_status(4, False, True) == "grace"

def test_addon_expired():
    assert validity_status(-11, False, True) == "expired"
