"""
A Python package to calculate wind loads on structures in accordance with
AS/NZS 1170.2:2021 Structural design actions Part 2: Wind actions.
"""

__version__ = "0.1.0"

from windactionsAU.wind_speed import(
    average_recurrence_interval,
    regional_wind_speed,
    site_wind_speed,
    design_wind_speed,
    wind_direction_multiplier,
    climate_change_multiplier,
    terrain_height_multiplier,
    shielding_multiplier,
    topographic_multiplier
)

from windactionsAU.wind_pressure import(
    basic_wind_pressure,
    design_wind_pressure,
)

from windactionsAU.aerodynamic_shape_factors import(
    ext_pressure_coeff_windward_wall,
    ext_pressure_coeff_leeward_wall,
    ext_pressure_coeff_side_walls,
    ext_pressure_coeff_roof_shallow,
    ext_pressure_coeff_roof_steep,
    area_reduction_factor,
    tributary_area
)