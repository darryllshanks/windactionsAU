import numpy as np


def ext_pressure_coeff_windward_wall(h: float, vary_with_height: bool=False) -> float:
    """
    
    """
    if h < 25 and vary_with_height == False:
        C_pe = 0.7
    else:
        C_pe = 0.8
    return C_pe


def ext_pressure_coeff_leeward_wall(d: float, b: float, roof_pitch: float):
    """
    
    Args:
        d:
        b:
        roof_pitch:
    """
    if roof_pitch < 10:
        C_pe = np.interp(d / b, [1, 2, 4], [-0.5, -0.3, -0.2])
    elif roof_pitch < 20:
        C_pe = np.interp(roof_pitch, [10, 15, 20], [-0.3, -0.3, -0.4])
    elif roof_pitch >= 25:
        C_pe = np.interp(roof_pitch, [0.1, 0.3], [-0.75, -0.5])
    return C_pe