import pandas as pd


# @dataclass
# class WindSpeed:
#     """
    
    
#     Args:

#     Returns:

#     """


# @dataclass
# class WindMultipliers:
#     """
    
#     """
#     # def __init__(self, )

def average_recurrence_interval(
        design_life: str='50 Years',
        importance_level: int=2,
        cyclonic: bool=False
) -> float:
    """
    Calculates the Average Recurrence Interval (ARI), which is the average time
    interval between exceedences of the design action, in accordance with
    AS/NZS 1170.0:2002(+A5) Appendix F. The Average Recurrence Interval is
    equal to the reciprocal of the Annual Probability of Exceedence (APE).

    Args:
        design_life: The design working life of a structure (in years). The 
            input shall be either: 'Construction Equipment', '5 Years', 
            '25 Years', '50 Years', or '100 Years'; default = '50 Years'.
        importance_level: The importance level of a structure as determined 
            by the National Construction Code of Australia or AS/NZS 
            1170.0:2002 Table F1. The input shall be either 1, 2, 3, or 4.
            Default is 2.
        cyclonic: Specifies whether the structure is in a cyclonic or
            non-cyclonic area; default is False (aka. non-cyclonic).
    Returns:
        Average Recurrence Interval (ARI) in years.
    """
    if cyclonic == False:
        ari_wind = 100
    else:
        ari_wind = 200

    ari_dict = {
        'Construction Equipment': 100,
        '5 Years': {1: 25, 2: 50, 3: 100, 4: 'NA'},
        '25 Years': {1: 100, 2: 500, 3: 500, 4: 1000},
        '50 Years': {1: ari_wind, 2: 500, 3: 1000, 4: 2500},
        '100 Years': {1: 500, 2: 1000, 3: 2500, 4: 'Risk Analysis'}
    }
    try:
        if design_life == 'Construction Equipment':
            ari = ari_dict[design_life]
        elif design_life == '5 Years' and importance_level == 4:
            raise ValueError(f"Importance Level 4 structures shall not be designed"
                            " for less than a 25 year design life.")
        elif design_life == '100 Years' and importance_level == 4:
            raise ValueError(f"Importance Level 4 structures with a design working"
                            " life of 100 years or more shall be determined by a"
                            " risk analysis, but shall have probabilities less"
                            " than or equal to those for Importance Level 3.")
        else:
            ari = ari_dict[design_life][importance_level]
    except:
        raise KeyError(f"The input Design Life and/or the Importance Level is an invalid option.")
    return ari


def regional_wind_speed(wind_region: str, R: float) -> float:
    """
    Calculates the regional wind speed.

    Args:
        wind_region: The wind region applicable to the site location as shown 
            in Figure 3.1(A) and Figure 3.1(B). The input shall be either: 
            'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'C', or 'D'.
        R: The Average Recurrence Interval (years).

    Returns:
        Regional Wind Speed (m/s).
    """
    if wind_region.startswith('A') == True:
        wind_speed = 67 - 41 * R ** (-0.1)
    elif wind_region.startswith('B') == True:
        wind_speed = 106 - 92 * R ** (-0.1)
    elif wind_region == 'C':
        wind_speed = 122 - 104 * R ** (-0.1)
    elif wind_region == 'D':
        wind_speed = 156 - 142 * R ** (-0.1)
    elif wind_region == 'NZ1' or wind_region == 'NZ2':
        wind_speed = 61 - 30 * R ** (-0.1)
    elif wind_region == 'NZ3':
        wind_speed = 71 - 34 * R ** (-0.1)
    elif wind_region == 'NZ4':
        wind_speed = 63 - 25 * R ** (-0.1)
    else:
        raise KeyError(f"The wind region '{wind_region}' is invalid. Please input a valid region.")
    return round(wind_speed)


def wind_direction_mult(wind_region: str, polygon_xsec: bool=False) -> pd.Series:
    """
    Calculates the wind direction multiplier (M_d) in each cardinal direction 
    for the site. Returns a Pandas series for wind on the primary structure 
    and a serparate series for wind on the cladding.

    Args:
        wind_region: The wind region applicable to the site location as shown 
            in Figure 3.1(A) and Figure 3.1(B). The input shall be either: 
            'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'C', or 'D'.
        polygon_xsec: 
    
    Returns:
        Wind Direction Multiplier, M_d and M_d_cladding
    """
    wind_dir_data = {
        'Region': ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'C', 'D'],
        'N': [0.90, 0.90, 0.85, 0.90, 0.85, 0.95, 0.75, 0.90, 0.90, 0.90],
        'NE': [0.85, 0.85, 0.75, 0.75, 0.75, 0.80, 0.75, 0.90, 0.90, 0.90],
        'E': [0.85, 0.85, 0.85, 0.75, 0.75, 0.80, 0.85, 0.90, 0.90, 0.90],
        'SE': [0.90, 0.80, 0.95, 0.90, 0.80, 0.80, 0.90, 0.90, 0.90, 0.90],
        'S': [0.90, 0.80, 0.95, 0.90, 0.80, 0.80, 0.95, 0.90, 0.90, 0.90],
        'SW': [0.95, 0.95, 0.95, 0.95, 0.90, 0.95, 0.95, 0.90, 0.90, 0.90],
        'W': [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.95, 0.90, 0.90, 0.90],
        'NW': [0.95, 0.95, 0.95, 0.95, 1.00, 0.95, 0.90, 0.90, 0.90, 0.90]
    }
    df = pd.DataFrame(data = wind_dir_data).set_index('Region')

    try:
        if polygon_xsec == False:
            df_Md = df.loc[wind_region]
        else:
            df_Md = pd.Series(
                data=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                index=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
            )
        
        if wind_region == 'B2' or wind_region == 'C' or wind_region == 'D':
            df_Md_cladding = pd.Series(
                data=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                index=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
            )
        else:
            df_Md_cladding = df_Md.copy()
    except:
        raise KeyError(f"The wind region '{wind_region}' is invalid. Please input a valid region.")

    return df_Md, df_Md_cladding


def climate_change_mult(wind_region: str) -> float:
    """
    Calculates the climate change multiplier.

    Args:
        wind_region: The wind region applicable to the site location as shown 
            in Figure 3.1(A) and Figure 3.1(B). The input shall be either: 
            'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'C', or 'D'.

    Returns:
        Climate Change Multiplier, M_c
    """
    if wind_region == 'B2' or wind_region == 'C' or wind_region == 'D':
        M_c = 1.05
    else:
        M_c = 1.0
    return M_c


def terrain_height_mult(
        terrain_category: str,
        wind_region: str,
        height: float,
        vary_wind_speed: bool=False
) -> float:
    """
    Calculates the terrain/height multiplier per Clause 4.2.2.
    
    Args:
        terrain_category: The site terrain category. The input shall be one of 
            either: 'TC1', 'TC2', 'TC2.5', 'TC3', or 'TC4'.
        wind_region: The wind region applicable to the site location as shown 
            in Figure 3.1(A) and Figure 3.1(B). The input shall be either: 
            'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'C', or 'D'.
        height:

    Returns:

    """
    M_zcat_data = {
        'Terrain Category': ['TC1', 'TC2', 'TC2.5', 'TC3', 'TC4'],
        3: [0.97, 0.91, 0.87, 0.83, 0.75],
        5: [1.01, 0.91, 0.87, 0.83, 0.75],
        10: [1.08, 1.00, 0.92, 0.83, 0.75],
        15: [1.12, 1.05, 0.97, 0.89, 0.75],
        20: [1.14, 1.08, 1.01, 0.94, 0.75],
        30: [1.18, 1.12, 1.06, 1.00, 0.80],
        40: [1.21, 1.16, 1.10, 1.04, 0.85],
        50: [1.23, 1.19, 1.13, 1.07, 0.90],
        75: [1.27, 1.22, 1.17, 1.12, 0.98],
        100: [1.31, 1.24, 1.20, 1.16, 1.03],
        150: [1.36, 1.27, 1.24, 1.21, 1.11],
        200: [1.39, 1.29, 1.27, 1.24, 1.16]
    }
    df = pd.DataFrame(data = M_zcat_data).set_index('Terrain Category')

    if wind_region == 'A0':
        df_M_zcat = pd.Series(
            data=[0.91, 0.91, 1.00, 1.05, 1.08, 1.12, 1.16, 1.18, 1.22, 1.24, 1.24, 1.24],
            index=[3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200]
        )
    else:
        df_M_zcat = df.loc[terrain_category]

    return df_M_zcat