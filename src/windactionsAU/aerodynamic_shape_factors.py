import numpy as np


def ext_pressure_coeff_windward_wall(h: float, vary_with_height: bool=False) -> float:
    """
    Calculates the windward wall external pressure coefficient for a rectangular 
    enclosed building per AS/NZS 1170.2:2021 Table 5.2(A).

    Args:
        h: the average roof height (m).
        vary_with_height: applies only to buildings with an average roof height 
            less than 25 m, the wind speed may be set as constant (False) or 
            may vary with height (True): default=False.

    Returns:
        Windward wall external pressure coefficient, C_pe
    """
    if h < 25 and vary_with_height == False:
        C_pe = 0.7
    else:
        C_pe = 0.8
    return C_pe


def ext_pressure_coeff_leeward_wall(d: float, b: float, roof_pitch: float):
    """
    Calculates the leeward wall external pressure coefficient for a rectangular 
    enclosed building per AS/NZS 1170.2:2021 Table 5.2(B).

    Args:
        d: building depth, parallel with the wind direction (m).
        b: building width, perpendicular to the wind direction (m).
        roof_pitch: angle of the roof pitch (degrees).
    
    Returns:
        Leeward wall external pressure coefficient, C_pe
    """
    if roof_pitch < 10:
        C_pe = np.interp(d / b, [1, 2, 4], [-0.5, -0.3, -0.2])
    elif roof_pitch < 20:
        C_pe = np.interp(roof_pitch, [10, 15, 20], [-0.3, -0.3, -0.4])
    elif roof_pitch < 25:
        C_pe_25 = np.interp(d / b, [0.1, 0.3], [-0.75, -0.5])
        C_pe = np.interp(roof_pitch, [20, 25], [-0.4, C_pe_25])
    elif roof_pitch >= 25:
        C_pe = np.interp(d / b, [0.1, 0.3], [-0.75, -0.5])
    return C_pe


def ext_pressure_coeff_side_walls(h: float, d: float) -> dict:
    """
    Calculates the side wall external pressure coefficients for a rectangular 
    enclosed building per AS/NZS 1170.2:2021 Table 5.2(C).

    Args:
        h: average roof height (m).
        d: building depth, parallel with the wind direction (m).

    Returns:
        Side wall external pressure coefficients, C_pe
    """
    C_pe = {
        "0 to 1h": [0, 1 * h, -0.65],
        "1h to 2h": [1 * h, 2 * h, -0.5],
        "2h to 3h": [2 * h, 3 * h, -0.3],
        "> 3h": [3 * h, max(3 * h, d), -0.2]
    }
    return C_pe
