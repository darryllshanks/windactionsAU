from windactionsAU.wind_speed import average_recurrence_interval


def test_average_recurrence_interval():
    assert average_recurrence_interval('50 Years', 2, False) == 500