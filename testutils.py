from enum import Enum, auto
from datetime import datetime

#TestResult = Enum('TestResult', 'DONT_KNOW SO_SO_KNOW KNOW_IT TOO_EASY)


def minutes_from_days(days):
    return round(days * 1440)


def next_test_interval_base(test_result, last_test_interval, last_test_datetime):
    '''Calcultes the number of minutes until the the test is shown again.'''

    is_first_test = last_test_interval <= 0

    if test_result == 'DONT_KNOW':
        if is_first_test:
            next_interval = 10
        else:
            next_interval = last_test_interval * .25
            # Don't allow values over one week
            next_interval = min(next_interval, minutes_from_days(7))

    elif test_result == 'SO_SO_KNOW':
        next_interval = minutes_from_days(1.4) if is_first_test else last_test_interval * 0.9

    elif test_result == 'KNOW_IT':
        next_interval = minutes_from_days(7) if is_first_test else minutes_passed(last_test_datetime) * 2.2

    elif test_result == 'TOO_EASY':
        next_interval = minutes_in_week * 4 if is_first_test else minutes_passed(last_test_date) * 3.5

    else:
        raise ValueError(f"Unkown test result: '{test_result}'")

    # Must be a positive integer greater or eqial to one
    return max(1, round(next_interval))

#      TODO   ' Add +- 7.5% to keep this from getting too predictable
#                Call Randomize
#                Dim RandMod As Single
#                RandMod = 1 + ((0.15 * Rnd()) - 0.075)

#                MinutesToNextTest = MinutesToNextTest * RandMod


def minutes_passed(start_datetime):
    '''The number of minutes since the specified date'''
    elaspedTime = datetime.now() - start_datetime
    return -1 * round(elaspedTime.total_seconds() / 60)
