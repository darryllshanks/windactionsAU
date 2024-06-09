import numpy as np
import pandas as pd

from math import sqrt
from windactionsAU.utils import str_to_int


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
            input shall be a string of either: 'Construction Equipment', 
            '5 Years', '25 Years', '50 Years', or '100 Years'; 
            default = '50 Years'.
        importance_level: The importance level of a structure as determined 
            by the National Construction Code of Australia or AS/NZS 
            1170.0:2002 Table F1. The input shall be either 1, 2, 3, or 4;
            default is 2.
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
        '25 Years': {1: 100, 2: 200, 3: 500, 4: 1000},
        '50 Years': {1: ari_wind, 2: 500, 3: 1000, 4: 2500},
        '100 Years': {1: 500, 2: 1000, 3: 2500, 4: 'Risk Analysis'}
    }
    importance_level = str_to_int(importance_level)

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
        Regional wind speed (m/s).
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


def regional_wind_speed_SLS(wind_region: str) -> float:
    """
    Calculates the serviceability limit state regional wind speed.

    Args:
        wind_region: The wind region applicable to the site location as shown 
            in Figure 3.1(A) and Figure 3.1(B). The input shall be either: 
            'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'C', or 'D'.
        R: The Average Recurrence Interval (years).

    Returns:
        Regional wind speed (m/s).
    """
    wind_speed = regional_wind_speed(wind_region, 25)
    return round(wind_speed)


def site_wind_speed(V_R, M_c, M_d, M_zcat, M_s, M_t):
    """
    Calculates the site wind speed defined for the 8 cardinal directions for
    the specified reference height above ground.

    Args:
        V_R: regional wind speed (m/s).
        M_c: climate change multiplier.
        M_d: Pandas series containing wind direction multipliers for the 8 
            cardinal directions.
        M_zcat: terrain/height multiplier.
        M_s: shielding multiplier.
        M_t: topgraphic multiplier.

    Returns:
        Site wind speed (m/s).
    """
    acc = []
    for beta in M_d:
        # V_R * M_c * beta * (M_zcat * M_s * M_t)
        acc.append(V_R * M_c * beta * (M_zcat * M_s * M_t))

    V_sit_beta = pd.Series(
        data=acc,
        index=['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    )
    return V_sit_beta


def design_wind_speed(orientation_angle: float, V_sit_beta: pd.Series) -> dict:
    """
    Calculates the building / structure orthogonal design wind speeds.

    Args:
        orientation_angle: The orientation of the building/structure primary 
            orthogonal angle of 0 Degrees relative to the site true North. This 
            shall be selected from between 0 and 90 degrees, rounded to the
            nearest 5 degrees. Refer to AS/NZS 1170.2:2021 Figure 2.2.
        V_sit_beta: A Pandas series containing the site wind speeds in the 8
            cardinal directions (m/s).
    
    Returns:
        Dictionary containing the design wind speeds (m/s) for building / 
        structure in the 4 orthogonal directions.
    """
    # Generates a Pandas DataFrame for Wind Direction multipliers in 5 degree increments
    acc = []
    angles = np.arange(-45, 360, 5).tolist()
    for i in angles:
        if i < 0:
            M_d_interp = np.interp(i, [-45, 0], [V_sit_beta.iloc[7], V_sit_beta.iloc[0]])
        elif i >= 0 and i < 45:
            M_d_interp = np.interp(i, [0, 45], [V_sit_beta.iloc[0], V_sit_beta.iloc[1]])
        elif i >= 45 and i < 90:
            M_d_interp = np.interp(i, [45, 90], [V_sit_beta.iloc[1], V_sit_beta.iloc[2]])
        elif i >= 90 and i < 135:
            M_d_interp = np.interp(i, [90, 135], [V_sit_beta.iloc[2], V_sit_beta.iloc[3]])
        elif i >= 135 and i < 180:
            M_d_interp = np.interp(i, [135, 180], [V_sit_beta.iloc[3], V_sit_beta.iloc[4]])
        elif i >= 180 and i < 225:
            M_d_interp = np.interp(i, [180, 225], [V_sit_beta.iloc[4], V_sit_beta.iloc[5]])
        elif i >= 225 and i < 270:
            M_d_interp = np.interp(i, [225, 270], [V_sit_beta.iloc[5], V_sit_beta.iloc[6]])
        elif i >= 270 and i < 315:
            M_d_interp = np.interp(i, [270, 315], [V_sit_beta.iloc[6], V_sit_beta.iloc[7]])
        elif i >= 315 and i < 360:
            M_d_interp = np.interp(i, [315, 360], [V_sit_beta.iloc[7], V_sit_beta.iloc[0]])
        acc.append([i, round(M_d_interp, 2)])

    M_d_df = pd.DataFrame(
        data=acc,
        columns=["Angles", "V_sit_beta"]
    )

    V_des_theta = {}
    if orientation_angle >=0 and orientation_angle <=90:
        ortho_directions = [0, 90, 180, 270]
        for ortho_direction in ortho_directions:
            angle = orientation_angle + ortho_direction
            angle_lower = angle - 45
            angle_upper = angle + 45

            mask_1 = M_d_df['Angles'] >= angle_lower
            mask_2 = M_d_df['Angles'] <= angle_upper
            masked_df = M_d_df.loc[mask_1 & mask_2, ["V_sit_beta"]].values.tolist()
            V_sit_beta_max = max(max(masked_df)[0], 30)
            V_des_theta.update({str(ortho_direction) + " Deg": V_sit_beta_max})
    else:
        raise ValueError(f"The building orientation angle shall be between 0 and 90 degrees, not '{orientation_angle}' degrees.")
    return V_des_theta


def wind_direction_multiplier(wind_region: str, modifier: bool=False) -> pd.Series:
    """
    Calculates the wind direction multiplier (M_d) in each cardinal direction 
    for the site. Returns a Pandas series for wind on the primary structure 
    and a separate series for wind on the cladding and immediate support
    structure.

    Args:
        wind_region: The wind region applicable to the site location as shown 
            in Figure 3.1(A) and Figure 3.1(B). The input shall be either: 
            'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'C', or 'D'.
        modifier: A bool defining whether the structure is a chimney, tank, or
            pole with a circular or polygonal cross-section; default = False.
    
    Returns:
        Wind Direction Multiplier, M_d and M_d_cladding.
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
        if modifier == False:
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


def climate_change_multiplier(wind_region: str) -> float:
    """
    Calculates the climate change multiplier.

    Args:
        wind_region: The wind region applicable to the site location as shown 
            in Figure 3.1(A) and Figure 3.1(B). The input shall be either: 
            'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'C', or 'D'.

    Returns:
        Climate Change Multiplier, M_c.
    """
    if wind_region == 'B2' or wind_region == 'C' or wind_region == 'D':
        M_c = 1.05
    else:
        M_c = 1.0
    return M_c


def terrain_height_multiplier(
        terrain_category: str,
        wind_region: str,
        height: float,
) -> float:
    """
    Calculates the terrain/height multiplier per Clause 4.2.2.
    
    Args:
        terrain_category: The site terrain category. The input shall be one of 
            either: 'TC1', 'TC2', 'TC2.5', 'TC3', or 'TC4'.
        wind_region: The wind region applicable to the site location as shown 
            in Figure 3.1(A) and Figure 3.1(B). The input shall be either: 
            'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'C', or 'D'.
        height: Average roof height in metres.

    Returns:
        Returns a single value for the terrain height multiplier if the wind
            speed does not vary with height, otherwise returns a series of the 
            terrain height multipliers for various heights.
    """
    M_zcat_data = {
        'Height': [3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200],
        'TC1': [0.97, 1.01, 1.08, 1.12, 1.14, 1.18, 1.21, 1.23, 1.27, 1.31, 1.36, 1.39],
        'TC2': [0.91, 0.91, 1.00, 1.05, 1.08, 1.12, 1.16, 1.19, 1.22, 1.24, 1.27, 1.29],
        'TC2.5': [0.87, 0.87, 0.92, 0.97, 1.01, 1.06, 1.10, 1.13, 1.17, 1.20, 1.24, 1.27],
        'TC3': [0.83, 0.83, 0.83, 0.89, 0.94, 1.00, 1.04, 1.07, 1.12, 1.16, 1.21, 1.24],
        'TC4': [0.75, 0.75, 0.75, 0.75, 0.75, 0.80, 0.85, 0.90, 0.98, 1.03, 1.11, 1.16]
    }

    if wind_region == 'A0':
        M_zcat_series = pd.Series(
            data=[0.91, 0.91, 1.00, 1.05, 1.08, 1.12, 1.16, 1.18, 1.22, 1.24, 1.24, 1.24],
            index=M_zcat_data['Height']
        )
    else:
        M_zcat_series = pd.Series(
            data=M_zcat_data[terrain_category],
            index=M_zcat_data['Height']
        )

    # if vary_wind_speed == False:
    M_zcat = np.interp(height, list(M_zcat_series.index), list(M_zcat_series.values))
    return M_zcat
    # else:
    #     return M_zcat_series
    

def shielding_multiplier(height: float, h_s: float=3.0, b_s: float=3.0, n_s: float=0.001):
    """
    Calculates the shielding multiplier per Clause 4.3.

    Args:
        height: average roof height, above ground, of the structure being 
            shielded (m).
        h_s: average roof height of shielding buildings (m); default is 3m.
        b_s: average breadth of shielding buildings, normal to the wind stream
            (m); default is 3m.
        n_s: number of upwind shielding buildings within a 45 degree sector of 
            radius 20*h and with h_s >= h; default is 0, which is set at 0.001
            to not divide by zero.
    
    Returns:
        Shielding Multiplier, M_s.
    """
    try:
        if h_s < height:
            raise ValueError(f"The average roof height of shielding buildings shall be greater than the height of the building being shielded.")
        l_s = height * (10 / n_s + 5)
        s = l_s / sqrt(h_s * b_s)
    except:
        raise ZeroDivisionError(f"The parameters h_s, b_s, and n_s shall not be zero.")

    if s >= 12.0 or height > 25:
        M_s = 1.0
    elif s <= 1.5:
        M_s = 0.7
    else:
        s_data = [[1.5, 3.0, 6.0, 12.0], [0.7, 0.8, 0.9, 1.0]]
        M_s = np.interp(s, s_data[0], s_data[1])

    return M_s


def topographic_multiplier(wind_region: str, z: float, hill_height: float, L_u: float, x: float, escarpment: bool=False, E: float=0.0):
    """
    Calculates the topographic multiplier per Clause 4.4.

    Args:
        wind_region: The wind region applicable to the site location as shown 
            in Figure 3.1(A) and Figure 3.1(B). The input shall be either: 
            'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'C', or 'D'.
        z: reference height of the structure above average local ground
            level (m).
        hill_height: height of the hill, ridge or escarpment (m).
        L_u: horizontal distance upwind from the crest of the hill, ridge or 
            escarpment to a level half the height below the crest (m).
        x: horizontal distance upwind or downwind of the structure to the crest
            of the hill, ridge or escarpment (m).
        escarpment: boolean identifier whether an escarpment is present (false)
            or not (true); default is false
        E: site elevation about mean sea level (m).

    Returns:
        Topographic Multiplier, M_t.
    """
    upwind_slope = hill_height / (2 * L_u)
    L_1 = max(0.36 * L_u, 0.4 * hill_height)
    if escarpment == False:
        L_2 = 4 * L_1
    else:
        L_2 = 10 * L_1

    # if abs(x)

    if upwind_slope < 0.05:
        M_h = 1.0
    elif upwind_slope > 0.45 and x >=0 and x <= hill_height / 4:
        M_h = 1 + 0.71 * (1 - abs(x) / L_2)
    else:
        M_h = 1 + (hill_height / (3.5 * (z + L_1))) * (1 - abs(x) / L_2)

    M_lee = 1.0  # Does not deal with sites in New Zealand

    if wind_region == 'A0':
        M_t = 0.5 + 0.5 * M_h
    elif wind_region == 'A4' and E >= 500:
        M_t = M_h * M_lee * (1 + 0.00015 * E)
    else:
        M_t = max (M_h, M_lee)

    return M_t