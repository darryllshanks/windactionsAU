import math
import pandas as pd
from windactionsAU import wind_speed as WS


def test_average_recurrence_interval():
    assert WS.average_recurrence_interval('25 Years', 2, False) == 250
    assert WS.average_recurrence_interval('50 Years', 2, False) == 500
    assert WS.average_recurrence_interval('50 Years', 4, False) == 2500


def test_regional_wind_speed():
    assert WS.regional_wind_speed("A0", 500) == 45
    assert WS.regional_wind_speed("A2", 250) == 43
    assert WS.regional_wind_speed("B2", 250) == 53
    assert WS.regional_wind_speed("C", 500) == 66
    assert WS.regional_wind_speed("C", 2500) == 74
    assert WS.regional_wind_speed("C", 10000) == 81
    assert WS.regional_wind_speed("D", 500) == 80


def test_regional_wind_speed_SLS():
    assert WS.regional_wind_speed_SLS("A0") == 37
    assert WS.regional_wind_speed_SLS("A1") == 37
    assert WS.regional_wind_speed_SLS("B2") == 39
    assert WS.regional_wind_speed_SLS("C") == 47
    assert WS.regional_wind_speed_SLS("D") == 53


def test_site_wind_speed():
    data_1_M_d = {
        "N": 0.90,
        "NE": 0.90,
        "E": 0.90,
        "SE": 0.90,
        "S": 0.90,
        "SW": 0.90,
        "W": 0.90,
        "NW": 0.90
    }
    data_1 = {
        "N": 69.93,
        "NE": 69.93,
        "E": 69.93,
        "SE": 69.93,
        "S": 69.93,
        "SW": 69.93,
        "W": 69.93,
        "NW": 69.93
    }
    assert WS.regional_wind_speed(66, 1.05, data_1_M_d, 1.0, 1.0, 1.0) == pd.Series(
        data=data_1, 
        index=["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    )

    data_2_M_d = {
        "N": 0.90,
        "NE": 0.85,
        "E": 0.85,
        "SE": 0.90,
        "S": 0.90,
        "SW": 0.95,
        "W": 1.00,
        "NW": 0.95
    }
    data_2 = {
        "N": 45.36,
        "NE": 42.84,
        "E": 42.84,
        "SE": 45.36,
        "S": 45.36,
        "SW": 47.88,
        "W": 50.40,
        "NW": 47.88
    }
    assert WS.regional_wind_speed(48, 1.0, data_2_M_d, 1.05, 1.0, 1.0) == pd.Series(
        data=data_2, 
        index=["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    )


def test_design_wind_speed():
    angle_1 = 0
    angle_2 = 45
    angle_3 = 90
    V_sit_beta = pd.Series(
        data={
            "N": 45.36,
            "NE": 42.84,
            "E": 42.84,
            "SE": 45.36,
            "S": 45.36,
            "SW": 47.88,
            "W": 50.40,
            "NW": 47.88
        },
        index=["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    )
    assert WS.design_wind_speed(angle_1, V_sit_beta) == {'0 Deg': 47.88, '90 Deg': 45.36, '180 Deg': 47.88, '270 Deg': 50.4}
    assert WS.design_wind_speed(angle_2, V_sit_beta) == {'0 Deg': 45.36, '90 Deg': 45.36, '180 Deg': 50.4, '270 Deg': 50.4}
    assert WS.design_wind_speed(angle_3, V_sit_beta) == {'0 Deg': 45.36, '90 Deg': 47.88, '180 Deg': 50.4, '270 Deg': 47.88}


def test_wind_direction_multiplier():
    data_1 = {
        "N": 0.90,
        "NE": 0.90,
        "E": 0.90,
        "SE": 0.90,
        "S": 0.90,
        "SW": 0.90,
        "W": 0.90,
        "NW": 0.90
    }
    assert WS.wind_direction_multiplier(wind_region="C", modifer=False) == pd.Series(
        data=data_1, 
        index=["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    )

    data_2 = {
        "N": 0.90,
        "NE": 0.85,
        "E": 0.85,
        "SE": 0.90,
        "S": 0.90,
        "SW": 0.95,
        "W": 1.00,
        "NW": 0.95
    }
    assert WS.wind_direction_multiplier(wind_region="C", modifer=False) == pd.Series(
        data=data_2, 
        index=["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    )


def test_climate_change_multiplier():
    assert WS.climate_change_multiplier("A0") == 1.0
    assert WS.climate_change_multiplier("B1") == 1.0
    assert WS.climate_change_multiplier("B2") == 1.05
    assert WS.climate_change_multiplier("C") == 1.05
    assert WS.climate_change_multiplier("D") == 1.05
    assert WS.climate_change_multiplier("NZ1") == 1.0


def test_terrain_height_multiplier():
    assert WS.terrain_height_multiplier("TC1", "A0", 17.5) == 1.065
    assert WS.terrain_height_multiplier("TC1", "A0", 125) == 1.24
    assert WS.terrain_height_multiplier("TC1", "A1", 17.5) == 1.13
    assert WS.terrain_height_multiplier("TC2.5", "C", 25) == 1.035
    assert WS.terrain_height_multiplier("TC3", "C", 2.5) == 0.83
    assert WS.terrain_height_multiplier("TC3", "C", 200) == 1.24


def test_shielding_multiplier():
    assert WS.shielding_multiplier(height=10, h_s=4, b_s=10, n_s=2) == 1.0
    assert math.isclose(WS.shielding_multiplier(height=10, h_s=10, b_s=10, n_s=4), 0.996, abs_tol=1e-3)
    # assert math.isclose(WS.shielding_multiplier(height=10, h_s=4, b_s=10, n_s=4), 0.996, abs_tol=1e-3)