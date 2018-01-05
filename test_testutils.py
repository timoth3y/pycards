import pytest
import testutils
from datetime import datetime, timedelta

@pytest.fixture
def last_week():
    return datetime.now() - timedelta(days=-7)


def test_minutes_from_days():
    assert testutils.minutes_from_days(1) == 1440
    assert testutils.minutes_from_days(.5) == 720
    assert testutils.minutes_from_days(2) == 2880
    # Make sure rounding works
    assert testutils.minutes_from_days(.33) == 475


def test_next_test_interval_base_unkown_state(last_week):
    with pytest.raises(ValueError):
        testutils.next_test_interval_base('UNKOWN', -12, last_week)

def test_next_test_interval_base_dont_know(last_week):
    state = 'DONT_KNOW'
    # Test 10 min later if you don't know the first time
    assert testutils.next_test_interval_base(state, -12, last_week) == 10
    # Can't allow times less than one minute
    assert testutils.next_test_interval_base(state, 1, last_week) == 1
    assert testutils.next_test_interval_base(state, .5, last_week) == 1
    # Cuts the last schedule by 25%
    assert testutils.next_test_interval_base(state, 100, last_week) == 25
    assert testutils.next_test_interval_base(state, 75, last_week) == 19


def test_next_test_interval_base_so_so(last_week):
    state = 'SO_SO_KNOW'
    # 1.4 days if it's the first time
    assert testutils.next_test_interval_base(state, -1, last_week) == 2016
    # 90% of scedhuled if not first
    assert testutils.next_test_interval_base(state, 100, last_week) == 90
    assert testutils.next_test_interval_base(state, 56, last_week) == 50


def test_next_test_interval_base_know_it(last_week):
    state = 'KNOW_IT'
    # 1 week if it's the first time
    assert testutils.next_test_interval_base(state, -1, last_week) == 10080
    # 2.2 times longer than last test time if its been tested before regadless of schedule
    assert testutils.next_test_interval_base(state, 100, last_week) == 22176
    assert testutils.next_test_interval_base(state, 75, last_week) == 22176


def test_next_test_interval_base_know_it(last_week):
    pass
