


def basic_wind_pressure(V_des_theta: float):
    """
    Calculates the basic wind pressure (without aerodynamic shape factors
    applied) for wind in one of the four orthogonal directions.

    Args:
        V_des_theta: the building / structure design wind speeds in one of the 
            four orthogonal directions.
    Returns:
        Basic wind pressure (kPa).
    """
    return 0.5 * 1.2e-3 * (V_des_theta) ** 2


def design_wind_pressure(basic_wind_pressure: float, C_shp: float, C_dyn: float=1.0) -> float:
    """
    Calculates the design wind pressure (kPa) for structures and parts of
    structures.

    Args:
        basic_wind_pressure: the basic wind pressure in one of the four
            orthogonal directions (kPa).
        C_shp: aerodynamic shape factor
        C_dyn: dynamic response factor; default=1.0 except where the structure 
            is dynamically wind sensitive. Refer to AS/NZS 1170.2:2021 Section 
            6 for further details.
    Returns:
        Design wind pressure, p (kPa).
    """
    return basic_wind_pressure * C_shp * C_dyn