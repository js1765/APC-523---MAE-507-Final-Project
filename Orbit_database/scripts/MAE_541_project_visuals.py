from support.orbit_data import gather_analytic_resonant_with_specified_p_and_x_value, gather_dataset, gather_analytic_resonant, merge_datasets
from support.plot import plot_given_boxes, plot_Poincare_2D_with_boxes, plot_Poincare_2D_with_balls, plot_Poincare_2D, plot_Poincare_3D, plot_Poincare_analytic, plot_cross_section_x_vy, plot_cross_section_x_vy_individual
import numpy as np
from support.rectangle_calculations import Rect_Poincare_2D_get_boxes, calculate_mega_box


# data = gather_dataset(
#     plot_second_crossings = True,
#     load_lunar                   = True,
#     load_prograde_resonant    = True,
#     load_prograde_resonant_x1    = True,
#     load_retrograde_resonant     = True,
#     load_retrograde_resonant_x1  = True,
#     load_crash                   = True,
#     load_circular                = True,
# )

data = gather_dataset(
    plot_second_crossings = True,
    load_lunar                   = True,
    load_prograde_resonant    = True,
    load_prograde_resonant_x1    = True,
    load_retrograde_resonant     = True,
    load_retrograde_resonant_x1  = True,
    load_crash                   = False,
    load_circular                = True,
)


orbits      = data["orbits"]
crossings   = data["crossings"]
families_id = data["families_str"]
earth_crash_x0 = data["earth_crash_x0"]
earth_crash_vx0 = data["earth_crash_vx0"]
earth_crash_vy0 = data["earth_crash_vy0"]
moon_crash_x0  = data["moon_crash_x0"]
moon_crash_vx0  = data["moon_crash_vx0"]
moon_crash_vy0  = data["moon_crash_vy0"]


# ###Change max_p to get more orbits (up to max_p : 1), change step_dx to get higher resolution (but beware of long runtimes for small step_dx)
# data_analytic = gather_analytic_resonant(max_p = 12, step_dx = 0.1)

# orbits_analytic      = data_analytic["orbits"]
# crossings_analytic   = data_analytic["crossings"]
# families_id_analytic = data_analytic["families_str"]


# print(orbits)

plot_Poincare_2D(orbits, crossings, families_id, 
                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                 plot_second_crossings = True, which="vy")

# plot_Poincare_2D(orbits_analytic, crossings_analytic, families_id_analytic, 
#                  earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
#                  plot_second_crossings = True, which="vy")

plot_Poincare_3D(orbits, crossings, families_id, 
                earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                plot_second_crossings = True)

# plot_Poincare_3D(orbits_analytic, crossings_analytic, families_id_analytic, 
#                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
#                 plot_second_crossings = True)
