import numpy as np

from windactionsAU.utils import str_to_float

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


def ext_pressure_coeff_roof_shallow(h: float, d: float, alpha: float):
    """
    Calculates the roof external pressure coefficients for a rectangular 
    enclosed building with a roof slope of less than 10 degrees, per AS/NZS 
    1170.2:2021 Table 5.3(A).

    Args:
        h: average roof height (m).
        d: building depth, parallel with the wind direction (m).
        alpha: roof pitch (degrees).

    Returns:
        Roof external pressure coefficients, C_pe
    """
    height_depth_ratio = str_to_float(h) / str_to_float(d)

    if alpha < 10:
        if height_depth_ratio <= 0.5:
            C_pe = {
                "0 to 0.5h": [-0.9, -0.4],
                "0.5h to 1h": [-0.9, -0.4],
                "1h to 2h": [-0.5, 0.0],
                "2h to 3h": [-0.3, 0.1],
                "> 3h": [-0.2, 0.2]
            }
        elif height_depth_ratio >= 1.0:
            C_pe = {
                "0 to 0.5h": [-1.3, 0.6],
                "0.5h to 1h": [-0.7, -0.3],
                "1h to 2h": [-0.7, -0.3],
                "2h to 3h": [0.0, 0.0],
                "> 3h": [0.0, 0.0]
            }
        else:
            C_pe = {
                "0 to 0.5h": [
                    np.interp(height_depth_ratio, [0.5, 1.0], [-0.9, -1.3]),
                    np.interp(height_depth_ratio, [0.5, 1.0], [-0.4, -0.6])
                ],
                "0.5h to 1h": [
                    np.interp(height_depth_ratio, [0.5, 1.0], [-0.9, -0.7]),
                    np.interp(height_depth_ratio, [0.5, 1.0], [-0.4, -0.3])
                ],
                "1h to 2h": [
                    np.interp(height_depth_ratio, [0.5, 1.0], [-0.5, -0.7]),
                    np.interp(height_depth_ratio, [0.5, 1.0], [0.0, -0.3])
                ],
                "2h to 3h": [
                    np.interp(height_depth_ratio, [0.5, 1.0], [-0.3, 0.0]),
                    np.interp(height_depth_ratio, [0.5, 1.0], [0.1, 0.0])
                ],
                "> 3h": [
                    np.interp(height_depth_ratio, [0.5, 1.0], [-0.2, 0.0]),
                    np.interp(height_depth_ratio, [0.5, 1.0], [0.2, 0.0])
                ]
            }
    else:
        raise ValueError(f"The roof pitch should be less than 10 degrees, not '{alpha}' degrees.")
    return C_pe


def ext_pressure_coeff_roof_steep(h: float, d: float, b: float, alpha: float):
    """
    Calculates the roof external pressure coefficients for a rectangular 
    enclosed building with a roof slope of greater than 10 degrees, per AS/NZS 
    1170.2:2021 Table 5.3(B) and Table 5.3(C).

    Args:
        h: average roof height (m).
        d: building depth, parallel with the wind direction (m).
        b: building width, perpendicular to the wind direction (m).
        alpha: roof pitch (degrees).

    Returns:
        Roof external pressure coefficients, C_pe in the format of an 
    """
    height_depth_ratio = str_to_float(h) / str_to_float(d)
    width_depth_ratio = str_to_float(b) / str_to_float(d)

    if alpha >= 10:
        # Pressure coefficients for the upwind slope

        # Cpe values for h/d <= 0.25
        C_pe_U1a = np.interp(
            alpha,
            [10, 15, 20, 25, 30, 35, 45],
            [-0.7, -0.5, -0.3, -0.2, -0.2, 0.0, 0.0]
        )
        C_pe_U1b = np.interp(
            alpha,
            [10, 15, 20, 25, 30, 35, 45, 50, 60],
            [-0.3, 0.0, 0.2, 0.3, 0.4, 0.5, 0.57, 0.61, 0.69]
        )
        # Cpe values for h/d == 0.5
        C_pe_U2a = np.interp(
            alpha,
            [10, 15, 20, 25, 30, 35, 45],
            [-0.9, -0.7, -0.4, -0.3, -0.2, -0.2, 0.0]
        )
        C_pe_U2b = np.interp(
            alpha,
            [10, 15, 20, 25, 30, 35, 45, 50, 60],
            [-0.4, -0.3, 0.0, 0.2, 0.3, 0.4, 0.57, 0.61, 0.69]
        )
        # Cpe values for h/d >= 1.0
        C_pe_U3a = np.interp(
            alpha,
            [10, 15, 20, 25, 30, 35, 45],
            [-1.3, -1.0, -0.7, -0.5, -0.3, -0.2, 0.0]
        )
        C_pe_U3b = np.interp(
            alpha,
            [10, 15, 20, 25, 30, 35, 45, 50, 60],
            [-0.6, -0.5, -0.3, 0.0, 0.2, 0.3, 0.57, 0.61, 0.69]
        )

        C_pe_U = [
            np.interp(height_depth_ratio, [0.25, 0.5, 1.0], [C_pe_U1a, C_pe_U2a, C_pe_U3a]),
            np.interp(height_depth_ratio, [0.25, 0.5, 1.0], [C_pe_U1b, C_pe_U2b, C_pe_U3b]),
        ]

        # Pressure coefficients for the downwind slope
        if width_depth_ratio <= 3:
            val_1 = -0.6
        elif width_depth_ratio < 8:
            val_1 = -0.06 * (7 + width_depth_ratio)
        else:
            val_1 = -0.9

        # Cpe values for h/d <= 0.25
        C_pe_D1 = np.interp(
            alpha,
            [10, 15, 20, 25, 60],
            [-0.3, -0.5, -0.6, val_1, val_1]
        )
        # Cpe values for h/d == 0.5
        C_pe_D2 = np.interp(
            alpha,
            [10, 15, 20, 25, 60],
            [-0.5, -0.5, -0.6, val_1, val_1]
        )
        # Cpe values for h/d >= 1.0
        C_pe_D3 = np.interp(
            alpha,
            [10, 15, 20, 25, 60],
            [-0.7, -0.6, -0.6, val_1, val_1]
        )
        C_pe_D = [
            np.interp(height_depth_ratio, [0.25, 0.5, 1.0], [C_pe_D1, C_pe_D2, C_pe_D3]),
            np.interp(height_depth_ratio, [0.25, 0.5, 1.0], [C_pe_D1, C_pe_D2, C_pe_D3])
        ]

        C_pe = [C_pe_U, C_pe_D]  

    else:
        raise ValueError(f"The roof pitch should be greater than 10 degrees, not '{alpha}' degrees.")

    return C_pe


def tributary_area(length: float, load_width: float) -> float:
    """
    Calculates the tributary area of applied loads to a structural member.

    Args:
        length: the length of the structural member.
        width: the load width for the structural member.

    Returns:
        Tributary Area
    """
    return str_to_float(length) * str_to_float(load_width)


def area_reduction_factor(trib_area: float, surface_parameter: str) -> float:
    """
    Calculates the area reduction factor for walls and roofs of enclosed
    buildings per AS/NZS 1170.2:2021 Table 5.4.

    Args:
        trib_area: the tributary area contributing to the force being
            considered (m**2).
        surface_parameter: the surface parameter for the structural element 
            being considered. The input shall be either 'Roof', 'Side Walls', 
            'Windward Walls', or 'Leeward Walls'.

    Returns:
        Area Reduction Factor, Ka    
    """
    surface_lowercase = str.lower(surface_parameter)
    if surface_lowercase == "roof" or surface_lowercase == "side walls":
        K_a = np.interp(trib_area, [10, 25, 100], [1.0, 0.9, 0.8])
    elif surface_lowercase == "windward walls":
        K_a = np.interp(trib_area, [10, 25, 100], [1.0, 0.95, 0.9])
    elif surface_lowercase == "leeward walls":
        K_a = np.interp(trib_area, [10, 25, 100], [1.0, 1.0, 0.95])
    return K_a


def action_combination_factor(C_pi: float, framing_type: str="Case z") -> float:
    """
    Calculates the action combination factor for walls and roofs of enclosed
    buildings per AS/NZS 1170.2:2021 Clause 5.4.3.

    Args:
        C_pi: the internal pressure coefficient.
        framing_type: The input shall be one of the following framing
            arrangement types (refer to AS/NZS 1170.2:2021 Table 5.5):
            {
                "Type 1": Portal frame with combination of wind pressures on 
                    the windward walls, leeward walls, and the roof.
                "Type 2": Portal frame with combination of wind pressures on
                    the side walls and the roof.
                "Type 3": Roof structure pinned at columns with roof wind
                    pressure.
                "Type 4": Lateral wind pressure on windward and leeward walls 
                    of braced structures.
                "Type 5": Lateral pressure on wall elements only.
            }
            If no framing_type is provided, the default value of 1.0  is 
            returned for the external and internal combination factors.

    Returns:
        Action Combination Factors, Kc   
    """
    action_combination_factors = {
        "Case a": {"External": 0.8, "Internal": 1.0},
        "Case b": {"External": 0.8, "Internal": 0.8},
        "Case c": {"External": 0.8, "Internal": 1.0},
        "Case d": {"External": 0.8, "Internal": 0.8},
        "Case e": {"External": 1.0, "Internal": 1.0},
        "Case f": {"External": 0.9, "Internal": 0.9},
        "Case g": {"External": 0.9, "Internal": 1.0},
        "Case h": {"External": 0.9, "Internal": 0.9},
        "Case z": {"External": 1.0, "Internal": 1.0},
    }

    if framing_type == "Type 1" and abs(C_pi) < 0.4:
        design_case = "Case a"
    elif design_case == "Type 1" and abs(C_pi) >= 0.4:
        design_case = "Case b"
    elif framing_type == "Type 2" and abs(C_pi) < 0.4:
        design_case = "Case c"
    elif design_case == "Type 2" and abs(C_pi) >= 0.4:
        design_case = "Case d"
    elif framing_type == "Type 3" and abs(C_pi) < 0.4:
        design_case = "Case e"
    elif design_case == "Type 3" and abs(C_pi) >= 0.4:
        design_case = "Case f"
    elif framing_type == "Type 4" and abs(C_pi) < 0.4:
        design_case = "Case g"
    elif framing_type == "Type 4" and abs(C_pi) >= 0.4:
        design_case = "Case h"
    elif design_case == "Type 5" and abs(C_pi) < 0.4:
        design_case = "Case h"
    elif design_case == "Type 5" and abs(C_pi) >= 0.4:
        design_case = "Case z"

    K_ce = action_combination_factors[design_case]["External"]
    K_ci = action_combination_factors[design_case]["Internal"]
    return K_ce, K_ci


def local_pressure_factor_walls(h: float, d: float, b: float):
    """
    
    Args:
        h: average roof height (m).
        d: building depth, parallel with the wind direction (m).
        b: building width, perpendicular to the wind direction (m).

    Returns:
        Local Pressure Factor, Kl
    """
    a = min(0.2 * b, 0.2 * d, h)

    # Building aspect ratio
    ratio = h / min(d, b)

    # Generate dictionary
    local_pressure_factors = {
        "All": {"K_l": 1.0},
        "WA1": {"K_l": 1.5, "Area": 0.25 * a ** 2, "Edge Proximity": "Anywhere"}
    }
    if ratio <= 1.0:
        local_pressure_factors.update({"SA1": {"K_l": 1.5, "Area": a ** 2, "Edge Proximity": [0, a]}})
        local_pressure_factors.update({"SA2": {"K_l": 2.0, "Area": 0.25 * a ** 2, "Edge Proximity": [0, 0.5 * a]}})
    elif ratio > 1.0:
        local_pressure_factors.update({"SA3": {"K_l": 1.5, "Area": 0.25 * a ** 2, "Edge Proximity": [a, d]}})
        local_pressure_factors.update({"SA4": {"K_l": 2.0, "Area": a ** 2, "Edge Proximity": [0, a]}})
        local_pressure_factors.update({"SA5": {"K_l": 3.0, "Area": 0.25 * a ** 2, "Edge Proximity": [0, 0.5 * a]}})
    return local_pressure_factors



def local_pressure_factor_roof(h: float, d: float, b: float, alpha: float):
    """
    Calculates the local pressure factor (K_l) when determining the wind 
    actions applied to cladding, their fixings, the members that directly 
    support the cladding, and the immediate fixings of these members. 

    Args:
        h: average roof height (m).
        d: building depth, parallel with the wind direction (m).
        b: building width, perpendicular to the wind direction (m).
        alpha: roof pitch (degrees).

    Returns:
        Local Pressure Factor, Kl
    """
    if h / d >= 0.2 or h / b >= 0.2:
        a = min(0.2 * b, 0.2 * d)
    else:
        a = 2 * h

    # Generate dictionary
    local_pressure_factors = {
        "All": {"K_l": 1.0},
        "RA1": {"K_l": 1.5, "Area": a ** 2, "Edge Proximity": [0, a]},
        "RA2": {"K_l": 2.0, "Area": 0.25 * a ** 2, "Edge Proximity": [0, 0.5 * a]}
    }
    if alpha < 10.0:
        local_pressure_factors.update({"RC1": {"K_l": 3.0, "Area": 0.25 * a ** 2, "Edge Proximity": [0, a]}})
    elif alpha >= 10:
        local_pressure_factors.update({"RA3": {"K_l": 1.5, "Area": a ** 2, "Edge Proximity": [0, a]}})
        local_pressure_factors.update({"RA4": {"K_l": 2.0, "Area": 0.25 * a ** 2, "Edge Proximity": [0, 0.5 * a]}})
        local_pressure_factors.update({"RC2": {"K_l": 3.0, "Area": 0.25 * a ** 2, "Edge Proximity": [0, a]}}),
    return local_pressure_factors


def local_pressure_factor_negative_limit(K_l: float, C_pe: float) -> float:
    """
    Calculates the negative limit on the prodcuct of the Local Pressure Factor 
    and the External Pressure Coefficient for rectangular buildings per 
    AS/NZS 1170.2:2021 Clause 5.4.4.

    Args:
        K_l: the local pressure factor.
        C_pe: the external pressure coefficient.

    Returns:
        Negative limit on the product of K_l * C_pe.
    """
    limit = max(K_l * C_pe, -3.0)
    return limit