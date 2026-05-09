"""
CR3BP Orbit Dataset Visualizations for Presentations
======================================

Purpose
-------

A place to load the CR3BP orbit datasets (from the "orbit_database" directory) and generate visualizations for presentations.
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

from matplotlib import patches





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




def make_mega_dataset():
    
    merged_data_collection = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.02)
    
    x_arr = np.linspace(0.02, 1.15, 20)

    for p in range(8,14):
        for x_val in x_arr:
            data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
            merged_data_collection = merge_datasets(merged_data_collection, data_analytic)
            
    return merged_data_collection




def plot_curves_of_constant_energy():
    
    
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",   
        "font.size": 14,
        "axes.labelsize": 20,
        "axes.titlesize": 16,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
    })
    
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    
    # ax.set_xlim(-0.5, 0.5)
    # ax.set_ylim(-6, 6)
    
    # ax.set_xlim(-0.8, 0.8)
    # ax.set_ylim(-6, 6)

    h1=0.2
    energy_min=1
    energy_max=8
    h2=0.2
    y_min=0
    y_max=6
    
    
    # boxes_arr = bc.generate_all_boxes(h1, energy_min, energy_max, h2, y_min, y_max)

    
    # bc.plot_crossings_in_boxes(crossings_analytic1, boxes_arr, colour='ro')
    
    # bc.plot_crossings_in_boxes(crossings_analytic2, boxes_arr, colour='bo')
    
    bc.BoundingBox.plot_all_bounding_curves(h1, energy_min, energy_max, h2, y_min, y_max, line_width=0.3)
    
    bc.BoundingBox.plot_accessible_region(h1, energy_min, energy_max, h2, y_min, y_max)
    
    
        

    
        
    # plt.title("Curves of Constant Energy")
    plt.xlabel(r"$x$")
    plt.ylabel(r"$v_y$")
    # plt.legend()
    
    # plt.savefig("Conference Images/test1.png", dpi=300, bbox_inches='tight')
    
    # plt.savefig(
    #     f"{BASE_PATH}/Conference Images/"
    #     f"Lines of Constant Energy.png",
    #     dpi=300,
    #     bbox_inches='tight'
    # )
    
    
    # plt.savefig(
    #     f"{BASE_PATH}/Conference Images/"
    #     f"Curves of Constant Energy with Horizontals.png",
    #     dpi=300,
    #     bbox_inches='tight'
    # )
    
    plt.savefig(
        f"{BASE_PATH}/Conference Images/"
        f"Upper Left Quadrant Curves of Constant Energy with Horizontals.png",
        dpi=300,
        bbox_inches='tight'
    )
    
    plt.show()




def test_plotting_all_boxes():
    
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",   
        "font.size": 14,
        "axes.labelsize": 20,
        "axes.titlesize": 16,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
    })
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)


    
    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    

    h1=0.2
    energy_min=1
    energy_max=8
    h2=0.2
    y_min=0
    y_max=6

    boxes_arr = bc.generate_all_boxes(h1, energy_min, energy_max, h2, y_min, y_max, chequerboard=0)
    
    
    bc.BoundingBox.plot_all_bounding_curves(h1, energy_min, energy_max, h2, y_min, y_max, line_width=0.3)
    
    
    bc.BoundingBox.plot_accessible_region(h1, energy_min, energy_max, h2, y_min, y_max)
    
    # print(boxes_arr)

    bc.plot_boxes(boxes_arr)
    
    
    
    
    
    
    # from support.helpers import earth_crash_vy_branches, generate_x_ranges, crash_surface_vy
    # from support.plot import plot_crash_region
    
    # x_min_moon=L1_info[0][0]
    # x_max_moon=L2_info[0][0]
    # x_min_earth=-0.8
    # x_max_earth=L1_info[0][0]

    # x_moon  = generate_x_ranges(x_min_moon,  x_max_moon, mu1, R_moon)
    # x_earth = generate_x_ranges(x_min_earth, x_max_earth, -mu2, earth_collision_radius)
    # plot_crash_region(ax=ax, x_range=x_moon, vx_fixed=0.0, mu_body=mu2, R_body=R_moon, x_body=1.0 - mu2, color="purple", label="Crash region Moon")
    # plot_crash_region(ax=ax, x_range=x_earth, vx_fixed=0.0, mu_body=mu1, R_body=earth_collision_radius, x_body=-mu2, color="red", label="Crash region Earth")

    
    
    
    
    plt.xlabel(r"$x$")
    plt.ylabel(r"$v_y$")
    # plt.legend()
    
    
    plt.savefig(
        f"{BASE_PATH}/Conference Images/"
        f"Upper Left Quadrant Boxes All Filled.png",
        dpi=300,
        bbox_inches='tight'
    )
    
    # plt.savefig(
    #     f"{BASE_PATH}/Conference Images/"
    #     f"Upper Left Quadrant Boxes With Crash Region.png",
    #     dpi=300,
    #     bbox_inches='tight'
    # )
    
    
    
    plt.show()





    
def finding_a_densish_collection_near_the_crash_region():
    
    
    merged_data0 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.008)


    # x_values = np.linspace(0.06, 1.15, 150)
    # x_values = np.linspace(0.06, 1.15, 20)
    x_values = np.linspace(0.06, 1.15, 1200)
    # # p_values = np.array([9,11,14])
    # # p_values = np.array([9,11,14,20,30,40,50])
    # # p_values = np.array([30,40,50])
    # # p_values = np.array([8,9,10,11,12,13,14,15,16,17,18,19,20])
    # p_values = np.array([8,10,11,13,16,20])
    # for p in p_values:
    #     for x_val in x_values:
    #         data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
    #         merged_data0 = merge_datasets(merged_data0, data_analytic)
        
    
    
    
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",   
        "font.size": 14,
        "axes.labelsize": 20,
        "axes.titlesize": 16,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
    })
    
        
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    
    # # ax.set_xlim(-0.5, 1.5)
    # # ax.set_ylim(-6, 6)
    
    
    

    p_values = np.array([8,10,11,13,16,20])
    for i in range(len(p_values)):
        p = p_values[i]
        for x_val in x_values:
            data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
            merged_data0 = merge_datasets(merged_data0, data_analytic)
        
        p_label =plt.cm.tab10.colors[i]
        # print("COLOUR COLOUR OCLOUR COLOUR ------", p_label)
        
        X = range(0)
        Y = range(0)
        plt.scatter(X, Y, marker = 'o', color = p_label, label='{p}:1 resonant orbit'.format(p=p))  
        
    
    
    
    
    orbits_merged0     = merged_data0["orbits"]
    crossings_merged0   = merged_data0["crossings"]
    families_id_merged0 = merged_data0["families_str"]


    


    # plot_Poincare_2D(orbits_merged0, crossings_merged0, families_id_merged0, 
    #                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    #                 plot_second_crossings = True, which="vy", show_only_lower_quadrant=True, print_legend=False)
    
    
    
    
 
 
    h1=0.2
    energy_min=1
    energy_max=8
    h2=0.2
    y_min=0.8
    y_max=6
    
    boxes_arr = bc.generate_all_boxes(h1, energy_min, energy_max, h2, y_min, y_max)

    boxes_with_crossings = bc.get_boxes_containing_crossings(crossings_merged0, boxes_arr)
    
    # fig = plt.figure(figsize=(12,8))
    # ax = fig.add_subplot(111)

    # ax.set_xlim(-0.5, 0)
    # ax.set_ylim(-0.1, 6)
    
    # # # ax.set_xlim(-0.5, 1.5)
    # # # ax.set_ylim(-6, 6)

    bc.plot_boxes(boxes_with_crossings)
    
    plot_Poincare_2D_without_printing(ax, orbits_merged0, crossings_merged0, families_id_merged0, 
                      earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0,
                      plot_second_crossings=True, which="vy", show_only_lower_quadrant=False, show_curves_of_constant_energy=False, print_legend=False)

    bc.BoundingBox.plot_all_bounding_curves(h1, energy_min, energy_max, h2, y_min, y_max, line_width=0.3)
    # bc.BoundingBox.plot_all_bounding_curves(h1, energy_min, energy_max, h2, y_min, y_max, line_width=0.5)
    
    bc.BoundingBox.plot_accessible_region(h1, energy_min, energy_max, h2, y_min, y_max)
    
    
    
    
    plt.scatter(-0.12184171, 3.12149768, marker = 'o', s=50, color = 'cyan', label='GEO')   # Plot the crossing (in the upper left quadrant) at GEO
    
    
    rect_height = 4

    rect = patches.Rectangle((-0.12184171, 3.12149768 - rect_height), 0.5, rect_height, linewidth=0.3, edgecolor='none', facecolor='lightcyan', alpha=0.6)
    #rect = patches.Rectangle((-0.12184171, 3.12149768 - rect_height), 0.5, rect_height, linewidth=0.3, edgecolor='none', facecolor='lightcyan', alpha=0.6)
    ax.add_patch(rect)



    

    plt.xlabel(r"$x$")
    plt.ylabel(r"$v_y$")
    # plt.xlabel("x")
    # plt.ylabel("y")
    plt.legend()
    
    
    plt.savefig(
        f"{BASE_PATH}/Conference Images/"
        f"Upper Left Quadrant Boxes Orbits 4.png",
        dpi=300,
        bbox_inches='tight'
    )
    
    
    
    plt.show()
    
    bc.find_percentage_covered(boxes_with_crossings, boxes_arr)









def plot_Poincare_3D():
    
    
    
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",   
        "font.size": 14,
        "axes.labelsize": 16,
        "axes.titlesize": 16,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
    })

    
    
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect((2, 1, 1))
    color_cycle = plt.cm.tab10.colors
    marker_cycle = ['o', '^', 's', 'd', 'v', '>', '<', 'p', 'h', 'x']
    label_to_color = {}
    label_to_marker_idx = {}

     # Plot the accessible region boundary surface.
    N_x   = 80
    N_th  = 60
    x_min = -0.8
    x_max = L2_info[0][0]
    # print("L2_info[0][0] IS THE FOLLOWING", L2_info[0][0])
    vy_min, vy_max = -6, 6
    vx_min, vx_max = -6, 6
    
    ##########THIS IS THE PART THAT ACTUALLY PLOTS THE 3D SURFACE:
    x_arr  = np.linspace(x_min, x_max, N_x)
    theta  = np.linspace(0, 2*np.pi, N_th)
    X, TH = np.meshgrid(x_arr, theta)
    mu1 = 1 - cr3bp.mu
    mu2 = cr3bp.mu
    U_vals = U_tilde(X, 0.0, mu1, mu2)
    val    = 2.0*(E0 - U_vals)
    val[val < 0] = np.nan
    R = np.sqrt(val)
    R_clipped = np.where(R > 6, 6, R)
    VX = R_clipped * np.cos(TH)
    VY = R_clipped * np.sin(TH)
    ax.plot_surface(X, VY, VX, alpha=0.4, color='grey', edgecolor='none')
    
    
    
    # ######TRYING TO PLOT A SIMILAR THING BUT FOR A LOWER ENERGY LEVEL (SO JUST THE SAME AS ABOVE BUT WITH A DIFFERNT E0):
    # x_arr  = np.linspace(x_min, x_max, N_x)
    # theta  = np.linspace(0, 2*np.pi, N_th)
    # X, TH = np.meshgrid(x_arr, theta)
    # mu1 = 1 - cr3bp.mu
    # mu2 = cr3bp.mu
    # U_vals = U_tilde(X, 0.0, mu1, mu2)
    # val    = 2.0*(0.9*E0 - U_vals)
    # val[val < 0] = np.nan
    # R = np.sqrt(val)
    # R_clipped = np.where(R > 6, 6, R)
    # VX = R_clipped * np.cos(TH)
    # VY = R_clipped * np.sin(TH)
    # ax.plot_surface(X, VY, VX, alpha=0.2, color='red', edgecolor='none')
    
    
    
    
    

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(vy_min, vy_max)
    ax.set_zlim(vx_min, vx_max)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$v_y$")
    ax.set_zlabel(r"$v_x$")
    ax.set_title(f"Earth–Moon CR3BP (Jacobi ≥ {jacobimin}) - 3D Plot")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    # plt.savefig(
    #     f"{BASE_PATH}/Figures/IC_plots/"
    #     f"IC_{families_str}_EM_CR3BP_x_vx_vy_2nd_{plot_second_crossings}.png",
    #     dpi=300,
    #     bbox_inches='tight'
    # )
    plt.show()

    
# def test_plot_poincare_3D():
#     plot_Poincare_3D(orbits_analytic1, crossings_analytic1, families_id_analytic1, 
#             earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
#             plot_second_crossings=True)


    
# plot_Poincare_3D()


# test_plot_poincare_3D()
    
    

# plot_Poincare_3D(orbits_analytic1, crossings_analytic1, families_id_analytic1, 
#             earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
#             plot_second_crossings=True)


# def plot_boxes():
    


# plot_curves_of_constant_energy()

test_plotting_all_boxes()

# finding_a_densish_collection_near_the_crash_region()