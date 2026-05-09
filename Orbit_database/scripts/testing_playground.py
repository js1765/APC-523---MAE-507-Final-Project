"""
CR3BP dataset loader & plotting driver
======================================

Purpose
-------


Honestly, this is doing the same thing that poincare_plot_generation.py was doing, but that file got too messy so I wanted to start here from scratch and keep it more organised this time.
"""




from support.orbit_data import gather_analytic_resonant_with_specified_p_and_x_value, gather_dataset, gather_analytic_resonant, merge_datasets, merge_lists
from support.plot import plot_Poincare_2D_without_printing, plot_given_boxes, plot_Poincare_2D_with_boxes, plot_Poincare_2D_with_balls, plot_Poincare_2D, plot_Poincare_3D, plot_Poincare_analytic, plot_cross_section_x_vy, plot_cross_section_x_vy_individual
from support.rectangle_calculations import Rect_Poincare_2D_get_boxes, calculate_mega_box, define_region
from support.constants import cr3bp, mu1, mu2, R_earth, R_moon, earth_collision_radius, E0, jacobimin, L2_info, L1_info, U_tilde, BASE_PATH  # type: ignore
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
# from bounding_box_calculations import BoundingBox
import bounding_box_calculations as bc





data = gather_dataset(
    plot_second_crossings = True,
    load_lunar                   = False,
    load_prograde_resonant    = False,
    load_prograde_resonant_x1    = False,
    load_retrograde_resonant     = False,
    load_retrograde_resonant_x1  = True,
    load_crash                   = False,
    load_circular                = False,
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



# data_analytic1 = gather_analytic_resonant(max_p = 14, step_dx = 0.01)
data_analytic1 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.1)
orbits_analytic1      = data_analytic1["orbits"]
crossings_analytic1   = data_analytic1["crossings"]
families_id_analytic1 = data_analytic1["families_str"]

data_analytic2 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 14, x_value = 0.05)
orbits_analytic2      = data_analytic2["orbits"]
crossings_analytic2   = data_analytic2["crossings"]
families_id_analytic2 = data_analytic2["families_str"]
    

data_analytic3 = gather_analytic_resonant(max_p = 12, step_dx = 0.1)
orbits_analytic3      = data_analytic3["orbits"]
crossings_analytic3   = data_analytic3["crossings"]
families_id_analytic3 = data_analytic3["families_str"]



    
    
def test_plot_Poincare_2D_with_balls():
    plot_Poincare_2D_with_balls(orbits_analytic1, crossings_analytic1, families_id_analytic1, 
                     earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                     plot_second_crossings = True, which="vy", radius=0.02)
    
    plot_Poincare_2D_with_balls(orbits_analytic1, crossings_analytic1, families_id_analytic1, 
                     earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                     plot_second_crossings = True, which="vy", radius=0.02, show_only_lower_quadrant=True)
    

def test_merge_datasets():
    """
    If the two plots look the same, then the merge_datasets function is working correctly. If they look different, then there is a problem with the merge_datasets function.
    """
    merged_data = merge_datasets(data_analytic1, data_analytic2)
    
    plot_Poincare_2D(merged_data["orbits"], merged_data["crossings"], merged_data["families_str"], 
                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                 plot_second_crossings = True, which="vy")
    

    #Compare this to the following, which merges in a different way. If these plots agree, then I know it's working.


    merged_orbits = merge_lists(orbits_analytic1, orbits_analytic2)
    merged_crossings = merge_lists(crossings_analytic1, crossings_analytic2)
    merged_families_id = merge_lists(families_id_analytic1, families_id_analytic2)
    
    # print(merged_crossings)

    plot_Poincare_2D(merged_orbits, merged_crossings, merged_families_id, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy")



def make_mega_dataset():
    
    merged_data_collection = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.02)
    
    x_arr = np.linspace(0.02, 1.15, 20)

    for p in range(8,14):
        for x_val in x_arr:
            data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
            merged_data_collection = merge_datasets(merged_data_collection, data_analytic)

    
    # plot_Poincare_2D_with_balls(merged_data_collection["orbits"], merged_data_collection["crossings"], merged_data_collection["families_str"], 
    #              earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    #              plot_second_crossings = True, which="vy")
    
    return merged_data_collection
    
        

# def test_merge_more():
    
#     merged_data = merge_datasets(data_analytic1, data_analytic2)
#     merged_data = merge_datasets(merged_data, data_analytic3)
    
#     # plot_Poincare_2D(merged_data["orbits"], merged_data["crossings"], merged_data["families_str"], 
#     #              earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
#     #              plot_second_crossings = True, which="vy", show_only_lower_quadrant=True)
    
    
#     # orbits_merged    = merged_data["orbits"]
#     # crossings_merged  = merged_data["crossings"]
#     # families_id_merged = merged_data["families_str"]
    
#     # # print(crossings_merged)
    
#     return merged_data
    
    
    
    
    
    

def test_plot_Poincare_2D_with_boxes():
    merged_orbits = merge_lists(orbits_analytic1, orbits_analytic2)
    merged_crossings = merge_lists(crossings_analytic1, crossings_analytic2)
    merged_families_id = merge_lists(families_id_analytic1, families_id_analytic2)
    
    merged_orbits = merge_lists(merged_orbits,orbits_analytic3)
    merged_crossings = merge_lists(merged_crossings, crossings_analytic3)
    merged_families_id = merge_lists(merged_families_id, families_id_analytic3)

    

    # boxes = Rect_Poincare_2D_get_boxes(orbits_analytic3, crossings_analytic3, plot_second_crossings = True, which="vy", square_length=0.04)
    
    
    boxes = Rect_Poincare_2D_get_boxes(merged_orbits, merged_crossings, plot_second_crossings = True, which="vy", square_length=0.1)
    plot_given_boxes(boxes, earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, which="vy")
    
    
    boxes = Rect_Poincare_2D_get_boxes(merged_orbits, merged_crossings, plot_second_crossings = True, which="vy", square_length=0.1)
    plot_given_boxes(boxes, earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, which="vy", show_only_lower_quadrant=True)


    calculate_mega_box(boxes)


def test_energy_lines():
    plot_Poincare_2D(orbits_analytic1, crossings_analytic1, families_id_analytic1, 
                     earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                     plot_second_crossings = True, which="vy", show_only_lower_quadrant=False, show_curves_of_constant_energy=True)
    
    # plot_Poincare_2D(orbits_analytic1, crossings_analytic1, families_id_analytic1, 
    #                  earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    #                  plot_second_crossings = True, which="vy", show_only_lower_quadrant=True, show_curves_of_constant_energy=False)









#######NOTE TO SELF: DOUBLE CHECK THIS, BUT I BELIEVE THAT ALL OF THE FOLLOWING FUNCTIONALITY WAS MOVED TO bounding_box_calculations.py. SO THE FOLLOWING INDICATED SECTION SHOULD PROBABLY BE DELETED:
####------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_region():
    import numpy as np
    import matplotlib.pyplot as plt
    # from support.constants import cr3bp, mu1, mu2, R_earth, R_moon, earth_collision_radius, E0, jacobimin, L2_info, L1_info, U_tilde, BASE_PATH 

    # # grid
    # x = np.linspace(-2, 2, 800)
    # y = np.linspace(0, 1, 800)
    # X, Y = np.meshgrid(x, y)
    # K1 = 1
    # y_upper = np.sqrt(2*(1.56*E0 - U_tilde(x, 0, mu1, mu2)))
    # y_lower = np.sqrt(2*(K1*E0 - U_tilde(x, 0, mu1, mu2)))
    # print(y_upper)
    # print(y_lower)
    
    # region = (
    # (Y < y_upper) &
    # (Y > y_lower) &
    # (Y > 0.4) &
    # (Y < 0.5)
    # )
    
    # plt.figure(figsize=(6,4))
    # plt.contourf(X, Y, region, levels=[0.5, 1], alpha=0.6)
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.title("Region defined by inequalities")
    # plt.colorbar(label="inside region")
    # plt.show()






    # X, Y = np.meshgrid(np.linspace(0.7, 1.1, 400),
    #                np.linspace(0, 3.2, 400))
    
    # def f1(x):
    #     return x**2

    # def f2(x):
    #     return -(x-1)**2 + 3

    # # region = (
    # #     (Y >= f1(X)) &
    # #     (Y <= f2(X)) &
    # #     (X >= 0.8) &
    # #     (X <= 1.0)
    # # )
    
    # region = (
    #     (Y >= 0.8) &
    #     (Y <= 1.0) &
    #     (X >= f1(X[0])) &
    #     (X <= f2(X[0]))
    # )

    # plt.contourf(X, Y, region, levels=[0.5,1], alpha=0.4)
    # plt.plot(X[0], f1(X[0]), 'k')
    # plt.plot(X[0], f2(X[0]), 'k')
    # plt.show()
    
    
    
    
    y = np.linspace(-np.sqrt(2), np.sqrt(2), 400)

    x_left = np.maximum(y**2, 0.5)
    x_right = np.minimum(y**2 + 1, 2)

    plt.plot(y**2, y, 'k', label=r"$x=y^2$")
    plt.plot(y**2 + 1, y, 'k', label=r"$x=y^2+1$")
    plt.axvline(0.5, color='k', linestyle='--')
    plt.axvline(2.0, color='k', linestyle='--')

    plt.fill_betweenx(y, x_left, x_right, alpha=0.4)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.title("Region")
    plt.show()
    
    
    
    # y = np.linspace(-6, 6, 400)

    # # x_left = np.maximum(y**2, 0.5)
    # # x_right = np.minimum(y**2 + 1, 2)
    
    # x_left = y**2
    # x_right = y**2 + 1

    # plt.plot(y**2, y, 'k', label=r"$x=y^2$")
    # plt.plot(y**2 + 1, y, 'k', label=r"$x=y^2+1$")
    # plt.axvline(0.5, color='k', linestyle='--')
    # plt.axvline(2.0, color='k', linestyle='--')

    # plt.fill_betweenx(y, x_left, x_right, alpha=0.4)

    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.legend()
    # plt.title("Region")
    # plt.show()
    
    
    x = np.linspace(0, 2.2, 600)
    y = np.linspace(-6, 6, 600)
    X, Y = np.meshgrid(x, y)

    x_left = np.maximum(Y**2, 0.5)
    x_right = np.minimum(Y**2 + 1, 2.0)

    region = (X >= x_left) & (X <= x_right)

    plt.contourf(X, Y, region, levels=[0.5,1], alpha=0.4)

    yy = np.linspace(-6,6,500)
    plt.plot(yy**2, yy, 'k')
    plt.plot(yy**2 + 1, yy, 'k')
    plt.axvline(0.5, color='k', linestyle='--')
    plt.axvline(2.0, color='k', linestyle='--')

    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    
    # y_upper = np.sqrt(2*(1.56*E0 - U_tilde(x, 0, mu1, mu2)))
    # y_lower = np.sqrt(2*(K1*E0 - U_tilde(x, 0, mu1, mu2)))
    
  
  
    # def U0(x):
    #     return -0.5*(x**2) - mu1/np.sqrt((x + mu2)**2) - mu2/np.sqrt((x - mu1)**2) - 0.5*mu1*mu2
    
    
    # y = np.linspace(-6, 6, 600)
    # x = np.linspace(0, 10, 600)  # make x big enough to cover parabolas
    # X, Y = np.meshgrid(x, y)

    # # compute left/right bounds
    # x_left = np.sqrt(2*(1.6*E0 - U_tilde(x, 0, mu1, mu2)))
    # x_right = np.sqrt(2*(1.56*E0 - U_tilde(x, 0, mu1, mu2)))

    # # mask: region exists only for 0.5 <= y <= 2
    # region = (Y >= 0.5) & (Y <= 2) & (X >= x_left) & (X <= x_right)

    # plt.contourf(X, Y, region, levels=[0.5,1], alpha=0.4)
    # plt.plot(np.sqrt(2*(1.56*E0 - U_tilde(x, 0, mu1, mu2))), x, 'k')
    # plt.plot(np.sqrt(2*(1.6*E0 - U_tilde(x, 0, mu1, mu2))), x, 'k')
    # plt.axhline(0.5, color='k', linestyle='--')
    # plt.axhline(2.0, color='k', linestyle='--')
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.show()
    
    
def test_shading1():
    
    
    
    from matplotlib.axes import Axes
    
    
    
    
    
    def U_0(x):
        return -0.5*(x**2) - mu1/np.sqrt((x + mu2)**2) - mu2/np.sqrt((x - mu1)**2) - 0.5*mu1*mu2
    
    x = np.linspace(-1.5, 1.5, 1200)  # x-grid

    # Compute left/right curves
    y_left = np.sqrt(np.maximum(0, 2*(1.6*E0 - U_0(x))))
    y_right = np.sqrt(np.maximum(0, 2*(1.56*E0 - U_0(x))))

    # Bottom and top bounds
    y_bottom = 0.4
    y_top = 0.5

    # Compute actual shaded region bounds
    y_min_fill = np.maximum(y_bottom, y_left)
    y_max_fill = np.minimum(y_top, y_right)


    valid = y_max_fill > y_min_fill
    y_min_plot = np.where(valid, y_min_fill, np.nan)
    y_max_plot = np.where(valid, y_max_fill, np.nan)

    # plt.fill_between(x, y_min_plot, y_max_plot, alpha=0.5, color='skyblue')


    # Mask where region exists
    mask = y_max_fill > y_min_fill


    x_min = -0.8
    x_max = L2_info[0][0]
    # Plot
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(111)
    # ax.set_xlim(x_min, x_max)
    # ax.set_ylim(-6, 6)
    ax.set_xlim(0.35, 0.4)
    ax.set_ylim(0.3, 0.55)
    plt.fill_between(x, y_min_plot, y_max_plot, alpha=0.5, color='skyblue')
    # plt.fill_between(x[mask], y_min_fill[mask], y_max_fill[mask], alpha=0.5, color='skyblue')
    
    #plot boundary curves
    plt.plot(x, y_left, 'k', label=r'$y_\mathrm{left}$')
    plt.plot(x, y_right, 'k', label=r'$y_\mathrm{right}$')
    plt.axhline(y_bottom, color='k', linestyle='--')
    plt.axhline(y_top, color='k', linestyle='--')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()
    
    
    
    # x = np.linspace(-1.5, 1.5, 1000)

    # # Compute raw curves
    # arg_left = 2*(1.6*E0 - U_0(x))
    # arg_right = 2*(1.56*E0 - U_0(x))

    # # Mask where both args are positive
    # valid = (arg_left > 0) & (arg_right > 0)

    # x_valid = x[valid]
    # y_left = np.sqrt(arg_left[valid])
    # y_right = np.sqrt(arg_right[valid])

    # # Clip to vertical bounds
    # y_bottom = 0.4
    # y_top = 0.5
    # y_lower_fill = np.maximum(y_left, y_bottom)
    # y_upper_fill = np.minimum(y_right, y_top)

    # # Only keep points where lower < upper
    # mask = y_upper_fill > y_lower_fill
    # x_final = x_valid[mask]
    # y_lower_final = y_lower_fill[mask]
    # y_upper_final = y_upper_fill[mask]


    # fig = plt.figure(figsize=(6,4))
    # ax = fig.add_subplot(111)
    # # ax.set_xlim(x_min, x_max)
    # # ax.set_ylim(-6, 6)
    # ax.set_xlim(0.35, 0.4)
    # ax.set_ylim(0.3, 0.55)
    
    # # Fill region
    # plt.fill_between(x_final, y_lower_final, y_upper_final, color='skyblue', alpha=0.5)

    # # Optional: plot curves
    # plt.plot(x_valid, y_left, 'k')
    # plt.plot(x_valid, y_right, 'k')
    # plt.axhline(y_bottom, color='k', linestyle='--')
    # plt.axhline(y_top, color='k', linestyle='--')

    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.title("Clean shaded region without offshoots")
    # plt.show()


    
def test_shading2():
    
    ###from matplotlib.axes import Axes
    
    def U_0(x):
        return -0.5*(x**2) - mu1/np.sqrt((x + mu2)**2) - mu2/np.sqrt((x - mu1)**2) - 0.5*mu1*mu2
    
    x = np.linspace(-1.5, 1.5, 64000)  # x-grid


    ##------------------------------------------------------------
    
    # # Compute left/right curves
    # y_left = np.sqrt(np.maximum(0, 2*(1.6*E0 - U_0(x))))
    # y_right = np.sqrt(np.maximum(0, 2*(1.2*E0 - U_0(x))))
    # Compute left/right curves
    y_left = np.sqrt(np.maximum(0, 2*(1.6*E0 - U_0(x))))
    y_right = np.sqrt(np.maximum(0, 2*(1.2*E0 - U_0(x))))


    h = 0.8 # height of regions
    y_min = 0
    y_max = 6
    y_heights = np.linspace(y_min, y_max, round((y_max - y_min) / h) + 1)

   
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    
    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    line_width = 1
    
    # Plot the bounding constant energy curves
    plt.plot(x, y_left, 'm', label=r'$y_\mathrm{left}$', lw=line_width)
    plt.plot(x, y_right, 'm', label=r'$y_\mathrm{right}$', lw=line_width)
    
    for i in range(len(y_heights)-1):
        
        # if i % 2 == 0:
        
        # if i == 5:
    
        # # Compute actual shaded region bounds
        y_min_fill = np.maximum(y_heights[i], y_left)
        y_max_fill = np.minimum(y_heights[i+1], y_right)
        
        valid = y_max_fill > y_min_fill
        y_min_plot = np.where(valid, y_min_fill, np.nan)
        y_max_plot = np.where(valid, y_max_fill, np.nan)
        
        plt.fill_between(x, y_min_plot, y_max_plot, alpha=0.5, color='skyblue')
        
        # Plot the horizontal bounding lines (the lines of constant height)
        plt.axhline(y_heights[i], color='tab:orange', linestyle='--', lw=line_width)
        plt.axhline(y_heights[i+1], color='tab:orange', linestyle='--', lw=line_width)
        
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()
    
    #------------------------------------------------------------
    


def test_bounding():
    
    def U_0(x):
            return -0.5*(x**2) - mu1/np.sqrt((x + mu2)**2) - mu2/np.sqrt((x - mu1)**2) - 0.5*mu1*mu2

    # x = np.linspace(-1.5, 1.5, 64000)  # x-grid



    class BoundingBox:

        def __init__(self, min_energy, max_energy, min_height, max_height):
            self.min_energy = min_energy  
            self.max_energy = max_energy
            self.min_height = min_height
            self.max_height = max_height
        
        
        def contains_point(self, x0, y0):
            
            # Boundary curves
            left_curve = np.sqrt(np.maximum(0, 2*(self.max_energy*E0 - U_0(x0))))
            right_curve = np.sqrt(np.maximum(0, 2*(self.min_energy*E0 - U_0(x0))))
            
            print("Left curve", left_curve)
            print("Right curve", right_curve)
            
            # # If the x0 value lies between the two energy curves, and the y0 value lies between the two horizontal heights
            # if ((left_curve <= x0 <= right_curve) and (self.min_height <= y0 <= self.max_height)):
            #     return True
            # else:
            #     return False
            
            print((left_curve >= x0 >= right_curve))
            
            
            # Check if bounded horizontally
            if ((left_curve <= x0 <= right_curve) or (left_curve >= x0 >= right_curve)):
                print("test1")
                
                # Check if bounded vertically
                if ((self.min_height <= y0 <= self.max_height) or (self.min_height >= y0 >= self.max_height)):
                    print("test2")
                    return True
                else:
                    return False
            else:
                return False
            
            
        
        
        def shade_box(self):
            """
            Visually plots the box.
            """    
            
            
            def const_energy_curve(k,x):
                return np.sqrt(np.maximum(0, 2*(k*E0 - U_0(x))))
            
            
            x = np.linspace(-1.5, 1.5, 64000)
            
            
            y_left = np.maximum(0, const_energy_curve(self.max_energy,x))
            y_right = np.maximum(0, const_energy_curve(self.min_energy,x))
            
            
            y_min_fill = np.maximum(self.min_height, y_left)
            y_max_fill = np.minimum(self.max_height, y_right)
            
            valid = y_max_fill > y_min_fill
            y_min_plot = np.where(valid, y_min_fill, np.nan)
            y_max_plot = np.where(valid, y_max_fill, np.nan)
            
            plt.plot(x, y_left, 'm', label={f"{self.min_energy:.1f}"}, lw=line_width)
            plt.plot(x, y_right, 'm', label={f"{self.max_energy:.1f}"}, lw=line_width)
            
            plt.fill_between(x, y_min_plot, y_max_plot, alpha=0.5, color='skyblue')
            
            # Plot the horizontal bounding lines (the lines of constant height)
            plt.axhline(self.min_height, color='tab:orange', linestyle='--', lw=line_width)
            plt.axhline(self.max_height, color='tab:orange', linestyle='--', lw=line_width)
            
            
        
    
    box1 = BoundingBox(1.2,1.6,0,1)
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    line_width = 1

    box1.shade_box()

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()
    
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    line_width = 1

    shade_vertical_slice(1,6,0)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()
        
    # print(box1.contains_point(-0.45, 0.1))



##### Fills in the boxes between the constant energy curve with energy k1*E0 and the constant energy curve with energy k2*E0 
# def shade_vertical_slice(k1,k2, chequerboard = False):
def shade_vertical_slice(k1,k2, chequerboard = 0):
    
    ###from matplotlib.axes import Axes
    
    def U_0(x):
        return -0.5*(x**2) - mu1/np.sqrt((x + mu2)**2) - mu2/np.sqrt((x - mu1)**2) - 0.5*mu1*mu2
    
    x = np.linspace(-1.5, 1.5, 64000)  # x-grid



    y_left = np.sqrt(np.maximum(0, 2*(k2*E0 - U_0(x))))
    y_right = np.sqrt(np.maximum(0, 2*(k1*E0 - U_0(x))))


    h = 0.2 # height of regions
    y_min = 0
    y_max = 6
    y_heights = np.linspace(y_min, y_max, round((y_max - y_min) / h) + 1)


    line_width = 1
    

    
    # for i in range(len(y_heights)-1):
        
    #     # if i % 2 == 0:
        
    #     # If we dont want a chequered pattern, then always do this. If we do want a chequered pattern, then only do this every other time:
    #     if (chequerboard and i % 2 == 0) or (not chequerboard):
            
    #         # Compute actual shaded region bounds
    #         y_min_fill = np.maximum(y_heights[i], y_left)
    #         y_max_fill = np.minimum(y_heights[i+1], y_right)
            
    #         valid = y_max_fill > y_min_fill
    #         y_min_plot = np.where(valid, y_min_fill, np.nan)
    #         y_max_plot = np.where(valid, y_max_fill, np.nan)
            
    #         plt.fill_between(x, y_min_plot, y_max_plot, alpha=0.5, color='skyblue')
            
    #         # Plot the horizontal bounding lines (the lines of constant height)
    #         plt.axhline(y_heights[i], color='tab:orange', linestyle='--', lw=line_width)
    #         plt.axhline(y_heights[i+1], color='tab:orange', linestyle='--', lw=line_width)
            


    for i in range(len(y_heights)-1):
        
        # if i % 2 == 0:
        
        # If we dont want a chequered pattern, then always do this. If we do want a chequered pattern, then only do this every other time:
        if (chequerboard == 1 and i % 2 == 0) or (chequerboard == 2 and i % 2 == 1) or (chequerboard == 0):
            
            # Compute actual shaded region bounds
            y_min_fill = np.maximum(y_heights[i], y_left)
            y_max_fill = np.minimum(y_heights[i+1], y_right)
            
            valid = y_max_fill > y_min_fill
            y_min_plot = np.where(valid, y_min_fill, np.nan)
            y_max_plot = np.where(valid, y_max_fill, np.nan)
            
            plt.fill_between(x, y_min_plot, y_max_plot, alpha=0.5, color='skyblue')
            
            # Plot the horizontal bounding lines (the lines of constant height)
            plt.axhline(y_heights[i], color='tab:orange', linestyle='--', lw=line_width)
            plt.axhline(y_heights[i+1], color='tab:orange', linestyle='--', lw=line_width)
            

 
def test_shading_fully_tiled():
    
    ###from matplotlib.axes import Axes
    
    def U_0(x):
        return -0.5*(x**2) - mu1/np.sqrt((x + mu2)**2) - mu2/np.sqrt((x - mu1)**2) - 0.5*mu1*mu2
    
    x = np.linspace(-1.5, 1.5, 64000)  # x-grid







    def const_energy_curve(k,x):
        return np.sqrt(np.maximum(0, 2*(k*E0 - U_0(x))))



    h1 = 1 # Difference between energy levels.
    energy_min = 1
    energy_max = 6
    energy_vals = np.linspace(energy_min, energy_max, round((energy_max - energy_min) / h1) + 1)
    
    print(energy_vals)
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    
    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    line_width = 1
    
    
    # for j in range(len(energy_vals)-1):
        
    #     # curve1 = const_energy_curve(energy_vals[j],x)
    #     # curve2 = const_energy_curve(energy_vals[j+1],x)
    #     plt.plot(x, const_energy_curve(energy_vals[j],x), 'm', label={f"{energy_vals[j]:.1f}"}, lw=line_width)
    #     # plot_vertical(curve1, curve2)
    #     shade_vertical_slice(energy_vals[j], energy_vals[j+1], chequerboard=True)
    
    
    for j in range(len(energy_vals)-1):
        
        # curve1 = const_energy_curve(energy_vals[j],x)
        # curve2 = const_energy_curve(energy_vals[j+1],x)
        plt.plot(x, const_energy_curve(energy_vals[j],x), 'm', label={f"{energy_vals[j]:.1f}"}, lw=line_width)
        # plot_vertical(curve1, curve2)
        
        # ####Uncomment for fully covered, no chequerboard pattern:
        # shade_vertical_slice(energy_vals[j], energy_vals[j+1])
        
        ####Uncomment for chequerboard pattern:
        if (j % 2 == 0):
            shade_vertical_slice(energy_vals[j], energy_vals[j+1], chequerboard=1)
        else:
            shade_vertical_slice(energy_vals[j], energy_vals[j+1], chequerboard=2)
            
            
        
        
    plt.plot(x, const_energy_curve(energy_vals[-1],x), 'm', label={f"{energy_vals[-1]:.1f}"}, lw=line_width)    #Print the last one too.
    
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()









    # def plot_vertical(y_left, y_right):
    #     #------------------------------------------------------------
    #     # # Compute left/right curves
    #     # y_left = np.sqrt(np.maximum(0, 2*(1.6*E0 - U_0(x))))
    #     # y_right = np.sqrt(np.maximum(0, 2*(1.2*E0 - U_0(x))))
        


    #     h = 0.2 # height of regions
    #     y_min = 0
    #     y_max = 6
    #     y_heights = np.linspace(y_min, y_max, round((y_max - y_min) / h) + 1)

    
        
    #     # fig = plt.figure(figsize=(12,8))
    #     # ax = fig.add_subplot(111)
        
    #     # ax.set_xlim(-0.5, 0)
    #     # ax.set_ylim(-0.1, 6)
    #     # line_width = 1
        
    #     # # Plot the bounding constant energy curves
    #     # plt.plot(x, y_left, 'm', label=r'$y_\mathrm{left}$', lw=line_width)
    #     # # plt.plot(x, y_right, 'm', label=r'$y_\mathrm{right}$', lw=line_width)
        
    #     for i in range(len(y_heights)-1):
            
    #         # if i % 2 == 0:
    #         # # Compute actual shaded region bounds
    #         y_min_fill = np.maximum(y_heights[i], y_left)
    #         y_max_fill = np.minimum(y_heights[i+1], y_right)
            
    #         valid = y_max_fill > y_min_fill
    #         y_min_plot = np.where(valid, y_min_fill, np.nan)
    #         y_max_plot = np.where(valid, y_max_fill, np.nan)
            
    #         plt.fill_between(x, y_min_plot, y_max_plot, alpha=0.5, color='skyblue')
            
            
    #         # Plot the horizontal bounding lines (the lines of constant height)
    #         plt.axhline(y_heights[i], color='tab:orange', linestyle='--', lw=line_width)
    #         plt.axhline(y_heights[i+1], color='tab:orange', linestyle='--', lw=line_width)
            
            
    #     # plt.xlabel("x")
    #     # plt.ylabel("y")
    #     # plt.legend()
    #     # plt.show()
    
    # #------------------------------------------------------------



    # def const_energy_curve(k,x):
    #     return np.sqrt(np.maximum(0, 2*(k*E0 - U_0(x))))



    # h1 = 1 # height of regions
    # energy_min = 1
    # energy_max = 6
    # energy_vals = np.linspace(energy_min, energy_max, round((energy_max - energy_min) / h1) + 1)
    
    # print(energy_vals)
    
    # fig = plt.figure(figsize=(12,8))
    # ax = fig.add_subplot(111)
    
    # ax.set_xlim(-0.5, 0)
    # ax.set_ylim(-0.1, 6)
    # line_width = 1
    
    # for j in range(len(energy_vals)-1):
        
    #     curve1 = const_energy_curve(energy_vals[j],x)
    #     curve2 = const_energy_curve(energy_vals[j+1],x)
    #     plt.plot(x, const_energy_curve(energy_vals[j],x), 'm', label={f"{energy_vals[j]:.1f}"}, lw=line_width)
    #     plot_vertical(curve1, curve2)
        
    # plt.plot(x, const_energy_curve(energy_vals[-1],x), 'm', label={f"{energy_vals[-1]:.1f}"}, lw=line_width)    #Print the last one too.
    
    
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.legend()
    # plt.show()
    


def test_shade_vertical_slice():
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    line_width = 1

    shade_vertical_slice(1,6,0)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()

####------------------------------------------------------------------------------------------------------------------------------------------------------------    














#####MOVED TO bounding_boxes.py, AND SIMPLIFIED
# def test_plot_points_in_boxes():
#     fig = plt.figure(figsize=(12,8))
#     ax = fig.add_subplot(111)

#     ax.set_xlim(-0.5, 0)
#     ax.set_ylim(-0.1, 6)
#     line_width = 1

#     boxes_arr = bc.generate_all_boxes(h1=1, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6)

    
#     # test_points_arr = [(-0.5, 0.2), (-0.5, 0.3), (-0.5, 0.4), (-0.6, 0.4), (-0.6, 0.2), (-0.6, 0), (1, 0.2), (0.5, 0.2), (-0.43, 0.2), (-0.41, 0.299)]
#     test_points_arr = [(-0.4, 0.15), (-0.3, 0.5), (-0.2, 2), (-0.15,3), (-0.059, 4.917), (-0.15, 0.1), (-0.45, 1.1)]
    
#     for point in test_points_arr:
#         for j in range(len(boxes_arr)):
#             for i in range(len(boxes_arr[0])):
#                 if boxes_arr[j][i].contains_point(point[0], point[1]):
#                     plt.plot(point[0], point[1], 'ro')  # Plot the point in red if it's in the box
#                     boxes_arr[j][i].plot_bounding_curves()
#                     boxes_arr[j][i].shade_box()
#                     break  # No need to check other boxes once we find one that contains the point
    
#     # plot_boxes(boxes_arr)

#     plt.xlabel("x")
#     plt.ylabel("y")
#     plt.legend()
#     plt.show()






def test_plot_crossings_in_boxes():
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)


    boxes_arr = bc.generate_all_boxes(h1=0.2, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6)

    
    bc.plot_crossings_in_boxes(crossings_analytic1, boxes_arr, colour='ro')
    
    bc.plot_crossings_in_boxes(crossings_analytic2, boxes_arr, colour='bo')
    
    bc.BoundingBox.plot_all_bounding_curves(h1=0.2, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6, line_width=1)
    
        
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()
    


def test_plot_merged_crossings_in_boxes():
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)


    boxes_arr = bc.generate_all_boxes(h1=0.2, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6)

    merged_data = merge_datasets(data_analytic1, data_analytic2)
    merged_data = merge_datasets(merged_data, data_analytic3)
    
    crossings_merged = merged_data["crossings"]
    
    # print(crossings_merged)
    
    # bc.plot_crossings_in_boxes(crossings_merged, boxes_arr, colour='ro')

    
        
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.legend()
    # plt.show()
    
    # print(crossings_merged)
    
    
    
    # for (x_vals, vx_vals, vy_vals, label) in crossings_merged:
    #     bc.plot_crossings_in_boxes([(x_vals, vx_vals, vy_vals, label)], boxes_arr, colour='ro')
        
    
    bc.plot_crossings_in_boxes(crossings_merged, boxes_arr, colour='ro')
    
    bc.BoundingBox.plot_all_bounding_curves(h1=0.2, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6, line_width=1)
        
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()
    
    

def test_plot_all_bounding_curves():
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    line_width = 1

    bc.BoundingBox.plot_all_bounding_curves(h1=0.2, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6, line_width=1)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()


def test_get_boxes_containing_crossings():
    
    boxes_arr = bc.generate_all_boxes(h1=0.2, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6)

    merged_data = merge_datasets(data_analytic1, data_analytic2)
    # merged_data = merge_datasets(merged_data, data_analytic3)
    
    crossings_merged = merged_data["crossings"]
    
    boxes_with_crossings = bc.get_boxes_containing_crossings(crossings_merged, boxes_arr)
    
    
    # print(boxes_with_crossings)
    
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)

    bc.plot_boxes(boxes_with_crossings)

    plt.xlabel("x")
    plt.ylabel("y")
    # plt.legend()
    plt.show()
    
    bc.find_percentage_covered(boxes_with_crossings, boxes_arr)
    





def test_finding_a_good_mega_dataset():
    
    merged_data_collection = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.01)
    
    # x_values = np.linspace(0.06, 1.15, 20)
    
    # x_values = np.linspace(0.02, 0.1, 20)
    
    
    # x_values = np.linspace(0.01, 0.1, 20)
    
    # x_values = np.linspace(0.01, 0.2, 20)
    
    # x_values = np.linspace(0.01, 0.4, 20)
    
    
    
    
    
    
    
    
    # x_values = np.linspace(0.01, 0.3, 60)
    
    
    # for p in range(8,15):
    #     for x_val in x_values:
    #         data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
    #         merged_data_collection = merge_datasets(data_analytic, merged_data_collection)
    #         print(f"Done p={p}, x={x_val}")
    
    
  
    
    
    
    
     # p_values = np.array([9,11,14])
    # p_values = np.array([9,11,14,20,30,40,50])
    # p_values = np.array([30,40,50])
    # p_values = np.array([8,9,10,11,12,13,14,15,16,17,18,19,20])
    
    # x_values = np.linspace(0.06, 1.15, 1200)
    x_values = np.linspace(0.06, 1.15, 150)
    p_values = np.array([8,10,11,13,16,20])
    
    
    for p in p_values:
        for x_val in x_values:
            data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
            merged_data_collection = merge_datasets(data_analytic, merged_data_collection)
    
    
    
    orbits_merged0     = merged_data_collection["orbits"]
    crossings_merged0   = merged_data_collection["crossings"]
    # families_id_merged0 = merged_data_collection["families_str"][0]
    families_id_merged0 = merged_data_collection["families_str"]
    
    
    
 
 
    h1=0.2
    energy_min=1
    energy_max=8
    h2=0.2
    y_min=0.8
    y_max=6
    
    boxes_arr = bc.generate_all_boxes(h1, energy_min, energy_max, h2, y_min, y_max)

    boxes_with_crossings = bc.get_boxes_containing_crossings(crossings_merged0, boxes_arr)
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    
    # # ax.set_xlim(-0.5, 1.5)
    # # ax.set_ylim(-6, 6)

    bc.plot_boxes(boxes_with_crossings)
    
    plot_Poincare_2D_without_printing(ax, orbits_merged0, crossings_merged0, families_id_merged0, 
                      earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0,
                      plot_second_crossings=True, which="vy", show_only_lower_quadrant=False, show_curves_of_constant_energy=False, print_legend=True)

    bc.BoundingBox.plot_all_bounding_curves(h1, energy_min, energy_max, h2, y_min, y_max, line_width=0.3)

    # plt.xlabel("x")
    # plt.ylabel("y")
    # # plt.legend()
    plt.show()
    
    bc.find_percentage_covered(boxes_with_crossings, boxes_arr)
    
    
    
    
    
    
    
    # merged_data0 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.01)

    # x_values = np.linspace(0.02, 0.1, 9)
    # # print("x_values:", x_values)

    # for x_val in x_values:
    #     data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = x_val)
    #     merged_data0 = merge_datasets(merged_data0, data_analytic)
        
    # orbits_merged0     = merged_data0["orbits"]
    # crossings_merged0   = merged_data0["crossings"]
    # families_id_merged0 = merged_data0["families_str"]

    # plot_Poincare_2D(orbits_merged0, crossings_merged0, families_id_merged0, 
    #                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    #                 plot_second_crossings = True, which="vy")



# # merged_data0 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.01)

# # x_values = np.linspace(0.02, 0.1, 9)
# # # print("x_values:", x_values)

# for x_val in x_values:
#     data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = x_val)
#     merged_data0 = merge_datasets(merged_data0, data_analytic)
    
# orbits_merged0     = merged_data0["orbits"]
# crossings_merged0   = merged_data0["crossings"]
# families_id_merged0 = merged_data0["families_str"]



# plot_Poincare_2D(orbits_merged0, crossings_merged0, families_id_merged0, 
#                  earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
#                  plot_second_crossings = True, which="vy")
    
    
    
    
    
    # fig = plt.figure(figsize=(12,8))
    # ax = fig.add_subplot(111)

    # ax.set_xlim(-0.5, 0)
    # ax.set_ylim(-0.1, 6)
    
    
    # h1=0.2
    # energy_min=1
    # energy_max=8
    # h2=0.2
    # y_min=0
    # y_max=6



    # boxes_arr = bc.generate_all_boxes(h1, energy_min, energy_max, h2, y_min, y_max)

    # # merged_data = merge_datasets(data_analytic1, data_analytic2)
    # # merged_data = merge_datasets(merged_data, data_analytic3)
    
    # # crossings_merged = merged_data["crossings"]
    
    # crossings_merged = merged_data_collection["crossings"]
    
    # bc.plot_crossings_in_boxes(crossings_merged, boxes_arr, colour='ro')
    
    # bc.BoundingBox.plot_all_bounding_curves(h1, energy_min, energy_max, h2, y_min, y_max, line_width=0.3)
        
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.legend()
    # plt.show()







# def plot_crossings_in_boxes(crossings_arr, boxes_arr):
    
#     x_vals = crossings_arr[0][0]
#     vy_vals = crossings_arr[0][2]

#     point_arr = []
#     for i in range(len(x_vals)): #Note that len(x_vals) = len(vy_vals) = number of crossings in this dataset.
#         point_arr.append((x_vals[i], vy_vals[i]))

#     bc.plot_points_in_boxes(point_arr, boxes_arr)
    
    
    
    
    
def finding_a_densish_collection_near_the_crash_region():
    
    merged_data0 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.008)

    # merged_data0 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.012)
    
    # merged_data0 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 12, x_value = 0.1)


    # orbits_merged0     = merged_data0["orbits"]
    # crossings_merged0   = merged_data0["crossings"]
    # families_id_merged0 = merged_data0["families_str"]






    # # x_values = np.linspace(0.02, 0.1, 9)
    # # p_values = np.array([8,9,10,11,14])
    
    
    # x_values = np.linspace(0.001, 0.02, 10)
    # p_values = np.array([8,9,10,11,12,13,14])
    
    # for p in p_values:
    #     for x_val in x_values:
    #         data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
    #         merged_data0 = merge_datasets(merged_data0, data_analytic)
        
        
    
    ###EXAMPLE OF THE X_VALUES JUST NOT GENERATING ANYTHING
    #####---------------------------------------
    # # x_values = np.linspace(0.1, 0.3, 9)
    # x_values = np.linspace(0.4, 0.5, 20)
    # # p_values = np.array([9,11,14])
    # p_values = np.array([9,11,14,20,30,40,50])
    
    # for p in p_values:
    #     for x_val in x_values:
    #         data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
    #         merged_data0 = merge_datasets(merged_data0, data_analytic)
    #####---------------------------------------
        
        
    
    
    # # x_values = np.linspace(0.1, 0.3, 9)
    # x_values = np.linspace(0.08, 0.32, 8)
    # # p_values = np.array([9,11,14])
    # p_values = np.array([9,11,14,20,30,40,50])
    # for p in p_values:
    #     for x_val in x_values:
    #         data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
    #         merged_data0 = merge_datasets(merged_data0, data_analytic)
    
    
    
    
    # # x_values = np.linspace(0.1, 0.3, 9)
    # x_values = np.linspace(0.08, 0.1, 20)
    # # p_values = np.array([9,11,14])
    # p_values = np.array([9,11,14,20,30,40,50])
    # for p in p_values:
    #     for x_val in x_values:
    #         data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
    #         merged_data0 = merge_datasets(merged_data0, data_analytic)
    
    
    
    
    #  # x_values = np.linspace(0.1, 0.3, 9)
    # x_values = np.linspace(0.08, 0.1, 20)
    # # p_values = np.array([9,11,14])
    # # p_values = np.array([9,11,14,20,30,40,50])
    # p_values = np.array([30,40,50])
    # for p in p_values:
    #     for x_val in x_values:
    #         data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
    #         merged_data0 = merge_datasets(merged_data0, data_analytic)
        
        
        
        
    

    x_values = np.linspace(0.06, 1.15, 150)
    # p_values = np.array([9,11,14])
    # p_values = np.array([9,11,14,20,30,40,50])
    # p_values = np.array([30,40,50])
    # p_values = np.array([8,9,10,11,12,13,14,15,16,17,18,19,20])
    p_values = np.array([8,10,11,13,16,20])
    for p in p_values:
        for x_val in x_values:
            data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
            merged_data0 = merge_datasets(merged_data0, data_analytic)
        
        
        
        
        
    orbits_merged0     = merged_data0["orbits"]
    crossings_merged0   = merged_data0["crossings"]
    families_id_merged0 = merged_data0["families_str"]


    


    plot_Poincare_2D(orbits_merged0, crossings_merged0, families_id_merged0, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy", show_only_lower_quadrant=True, print_legend=True)

        
    
    
# test_plot_Poincare_2D_with_balls()
# test_merge_datasets()
# test_plot_Poincare_2D_with_boxes()
# test_energy_lines()

# define_region()

# test_region()

# test_energy_lines()

# test_shading1()

# test_shading2()

# test_bounding()

# test_shading_fully_tiled()

# test_shade_vertical_slice()




# test_plot_points_in_boxes()

## test_plot_crossings_in_boxes0()

# test_plot_crossings_in_boxes()

# test_plot_merged_crossings_in_boxes1()

# make_mega_dataset()




# bc.test_plot_points_in_boxes()  

###test_plot_points_in_boxes()  



# test_plot_crossings_in_boxes()



test_merge_datasets()


# test_merge_more()





# test_plot_merged_crossings_in_boxes()

# test_plot_all_bounding_curves()


# test_get_boxes_containing_crossings()





# test_finding_a_good_mega_dataset()

# finding_a_densish_collection_near_the_crash_region()

