import windactionsAU.utils as utils


def test_str_to_int():
    test_str_1 = "43"
    test_str_2 = "-2000"
    test_str_3 = 'testint'

    assert utils.str_to_int(test_str_1) == 43
    assert utils.str_to_int(test_str_2) == -2000
    assert utils.str_to_int(test_str_3) == 'testint'


def test_str_to_float():
    test_str_1 = "43"
    test_str_2 = "-2000"
    test_str_3 = "324.625"
    test_str_4 = 'POINT:Fy'

    assert utils.str_to_float(test_str_1) == 43.0
    assert utils.str_to_float(test_str_2) == -2000.0
    assert utils.str_to_float(test_str_3) == 324.625
    assert utils.str_to_float(test_str_4) == 'POINT:Fy'


def test_round_down():
    test_val_1 = 43.168
    test_val_2 = 100.523
    test_val_3 = 89.954
    test_val_4 = 4
    test_val_5 = '43.168'

    assert utils.round_down(test_val_1, 2) == 43.16
    assert utils.round_down(test_val_1, 1) == 43.1
    assert utils.round_down(test_val_2, 2) == 100.52
    assert utils.round_down(test_val_2, 1) == 100.5
    assert utils.round_down(test_val_3, 2) == 89.95
    assert utils.round_down(test_val_3, 1) == 89.9
    assert utils.round_down(test_val_4, 1) == 4.0
    assert utils.round_down(test_val_5, 1) == '43.168'


def test_round_up():
    test_val_1 = 43.168
    test_val_2 = 100.523
    test_val_3 = 89.954
    test_val_4 = 4
    test_val_5 = '43.168'

    assert utils.round_up(test_val_1, 2) == 43.17
    assert utils.round_up(test_val_1, 1) == 43.2
    assert utils.round_up(test_val_2, 2) == 100.53
    assert utils.round_up(test_val_2, 1) == 100.6
    assert utils.round_up(test_val_3, 2) == 89.96
    assert utils.round_up(test_val_3, 1) == 90.0
    assert utils.round_up(test_val_4, 1) == 4.0
    assert utils.round_up(test_val_5, 1) == '43.168'