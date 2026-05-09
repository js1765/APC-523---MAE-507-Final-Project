
import sys
import os
from time import monotonic
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) #This is so that this file knows the correct path to take, since I put it in a folder.


# from support.orbit_data import gather_analytic_resonant_with_specified_p_and_x_value, gather_dataset, gather_analytic_resonant, merge_datasets
# from support.plot import plot_given_boxes, plot_Poincare_2D_with_boxes, plot_Poincare_2D_with_balls, plot_Poincare_2D, plot_Poincare_3D, plot_Poincare_analytic, plot_cross_section_x_vy, plot_cross_section_x_vy_individual
import numpy as np
# from support.rectangle_calculations import Rect_Poincare_2D_get_boxes, calculate_mega_box
import matplotlib.pyplot as plt
from project_plot import plot_Poincare_2D, plot_Poincare_3D, plot_Poincare_analytic, plot_Poincare_2D_without_printing, plot_2D_crash_region_and_accessible_region
from scipy.interpolate import CubicSpline, PchipInterpolator, Akima1DInterpolator


from APC_523_MAE_507_Final_Project.project_main import get_list_of_points, multiple_get_list_of_points, multiple_isolate_one_quadrant




# Function to do the Lagrange interpolation
def lagrange_interpolant(x_nodes, y_nodes, x):
    x = np.array(x, dtype=float)
    p = len(x_nodes) - 1 - 1 
    g = np.zeros_like(x, dtype=float)

    for i in range(p+1):
        L = np.ones_like(x, dtype=float)
        for j in range(p+1):
            if j != i:
                L *= (x - x_nodes[j])/(x_nodes[i] - x_nodes[j])
        g += y_nodes[i] * L

    return g









def lagrange_interpolate_points(points, p=None):
    """
    Fit a Lagrange interpolant to a set of (x, vy) points.
    
    points : list of (x, vy) tuples, sorted by x
    p      : degree of interpolant (defaults to len(points)-1, i.e. exact fit)
    
    Returns a callable f(x) that evaluates the interpolant.
    """
    
    # if len(points) >= 20:
    #     indices = np.linspace(0, len(points) - 1, 10, dtype=int)
    #     points = [points[i] for i in indices]
    
    # print(len(points))
      
    # # if len(points) > 20:
    # #     n = len(points)
    # #     middle_count = n // 2 - 6
    # #     middle_indices = np.linspace(3, n - 4, middle_count, dtype=int)
    # #     points = points[:2] + [points[i] for i in middle_indices] + points[-2:]
    
    # print(len(points))
    
    
    # if len(points) >= 20:
    #     # indices = np.linspace(0, len(points) - 1, 10, dtype=int)
    #     points = points[::6]
        
        
        
    # if len(points) >= 20:
    #     # # indices = np.linspace(0, len(points) - 1, 10, dtype=int)
    #     # points = points[:3] + points[-3:]
        
    #     n = len(points)
    #     mid = n // 2
    #     points = points[:6] + [points[mid-1], points[mid], points[mid+1]] + points[-6:]
        
        
    
    xs, vys = zip(*points)
    x_nodes = np.array(xs,  dtype=float)
    y_nodes = np.array(vys, dtype=float)

    # print("--------------------------------------------------------------")
    # print("x_nodes length ", len(x_nodes))
     
    def interpolant(x):
        return lagrange_interpolant(x_nodes, y_nodes, x)

    return interpolant




# Helper method to select points close to Chebyshev nodes, which should give us a better interpolation.
def selecting_chebyshev_points(points, p):
    """
    Given a list of (x, y) points, select p+1 points whose x values are
    closest to the Chebyshev nodes scaled to the data range.
    """
    xs = np.array([p[0] for p in points])
    x_min, x_max = xs.min(), xs.max()


        

    # Function to get Chebyshev nodes
    def chebyshev_nodes(p):
        k = np.arange(p+1)
        return np.cos((2*k + 1) * np.pi / (2*(p+1)))

        
    
    # Get Chebyshev nodes scaled to data range
    cheb_nodes = chebyshev_nodes(p)
    x_nodes = 0.5 * (x_max + x_min) + 0.5 * (x_max - x_min) * cheb_nodes

    # For each Chebyshev node, find the closest data point
    selected = []
    for xn in x_nodes:
        closest_idx = np.argmin(np.abs(xs - xn))
        selected.append(points[closest_idx])

    return selected











### DEPRECATED. USE run_single_interpolation() OR test_run_single_interpolation() INSTEAD.
def test_single_interpolation():
    x_min, x_max = -0.75, 0
    y_min, y_max = 0, 6

    x_vy_points,fig,ax = get_list_of_points(max_p = 10, x_value = 0.1, quadrant = "top left", plot_points = False)

    # x_vy_points,fig,ax = get_list_of_points(max_p = 20, x_value = 0.2, quadrant = "top left", plot_points = False)


    print("x_vy_points: ", x_vy_points)


    f = lagrange_interpolate_points(x_vy_points)

    x_eval = np.linspace(x_min, x_max, 300)

    ax.plot(x_eval, f(x_eval), label='interpolant')
    ax.legend()

    plt.show()






#### DEPRECATED. USE run_multiple_interpolation with interpolation_method = "lagrange" AND/OR chebyshev_points = True INSTEAD
def test_multiple_interpolation():
    x_min, x_max = -0.75, 0
    y_min, y_max = 0, 6

    p_arr=[8,9,10,11,12]
    x_val_arr=[0.08, 0.08, 0.08, 0.08, 0.08]
    
    
    
    #This part is just to get the plot loaded.
    #--------------------------------------------------------------------------------------------------------------
    data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    orbits      = data["orbits"]
    crossings   = data["crossings"]
    families_id = data["families_str"]
    earth_crash_x0 = np.array([])
    earth_crash_vx0 = np.array([])
    earth_crash_vy0 = np.array([])
    moon_crash_x0  = np.array([])
    moon_crash_vx0  = np.array([])
    moon_crash_vy0  = np.array([])


    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)


    ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False)
    #--------------------------------------------------------------------------------------------------------------
    
    
    
    
    
    x_vy_points = multiple_get_list_of_points(p_arr, x_val_arr, quadrant = "top left")

    # Choose some points close to Chebyshev nodes to get a better interpolation
    x_vy_points = selecting_chebyshev_points(x_vy_points, p=10)
    # print("x_vy_points after selecting chebyshev points: ", x_vy_points)




    # print("x_vy_points: ", x_vy_points)


    f = lagrange_interpolate_points(x_vy_points)

    # x_eval = np.linspace(x_min, x_max, 300)
    
    # xs_plot, vys_plot = zip(*x_vy_points)

    # plt.scatter(xs_plot, vys_plot, s=10)
    # plt.xlabel('x')
    # plt.ylabel('vy')
    # plt.title('vy vs x')
    # plt.grid(True)
    # plt.tight_layout()

    # plt.plot(x_eval, f(x_eval), label='interpolant')
    # plt.legend()

    # plt.show()
    
    
    x_eval = np.linspace(x_min, x_max, 300)
    
    # xs_plot, vys_plot = zip(*x_vy_points)

    # plt.scatter(xs_plot, vys_plot, s=10)
    plt.xlabel('x')
    plt.ylabel('vy')
    plt.title('vy vs x')
    plt.grid(True)
    plt.tight_layout()
    plt.plot(x_eval, f(x_eval), label='interpolant', alpha=0.5)
    plt.legend()

    plt.show()
    
    
    
    
    
#### DEPRECATED. USE run_multiple_interpolation with interpolation_method = "PCHIP_remove_spikes" AND/OR "PCHIP_remove_dips" INSTEAD
# NOTE: It doesn't look monotonic because I am still printing out all of the points. But don't worry, it is only using the monotonicised points!
def PCHIP_interpolation(p_arr, x_val_arr, monotonic="remove spikes"):
    x_min, x_max = -0.75, 0
    y_min, y_max = 0, 6

    p_arr = p_arr
    x_val_arr = x_val_arr
    
    
    #This part is just to get the plot loaded.
    #--------------------------------------------------------------------------------------------------------------
    data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    orbits      = data["orbits"]
    crossings   = data["crossings"]
    families_id = data["families_str"]
    earth_crash_x0 = np.array([])
    earth_crash_vx0 = np.array([])
    earth_crash_vy0 = np.array([])
    moon_crash_x0  = np.array([])
    moon_crash_vx0  = np.array([])
    moon_crash_vy0  = np.array([])


    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)


    ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False)
    #--------------------------------------------------------------------------------------------------------------
    
    
    
    x_vy_points = multiple_get_list_of_points(p_arr, x_val_arr, quadrant = "top left") # Get the (x, vy) points that we want to interpolate between.
                                                                                       # the "multiple" is because we are getting points from multiple different p:1 familes, and with possibly different x_vals.



    # Remove some points to make sure the data is monotonic. This lets us use PCHIP interpolation.
    # As the data is supposed to be monotonic, minus the noise we have, this is reasonable to do.
    def make_monotonic(points, monotonic="remove spikes"):
        
        # This first if block makes it monotonic by removing the 'dips' rather than the 'spikes'.
        # E.g.: if I have the points (0,1),(1,3),(2,2), it removes (2,2).
        # But from visual inspection, I think it would be better if it removed (1,3)
        if monotonic == "remove dips":
            
            monotonic = [points[0]]
            for p in points[1:]:
                if p[1] > monotonic[-1][1]:
                    monotonic.append(p)
            pts = monotonic
        
        # This second block makes it monotonic by removing the 'spikes' rather than the 'dips', in contrast to the above.
        # It seems to lead to 'smoother' curves.
        elif monotonic == "remove spikes":    
            pts = list(points)
            changed = True
            while changed:
                changed = False
                new_pts = [pts[0]]
                for i in range(1, len(pts) - 1):
                    prev_y = new_pts[-1][1]
                    next_y = pts[i + 1][1]
                    curr_y = pts[i][1]
                    if curr_y > prev_y and curr_y > next_y:  # it's a spike
                        changed = True  # skip this point
                    else:
                        new_pts.append(pts[i])
                new_pts.append(pts[-1])
                pts = new_pts
                
        else:
            raise ValueError("Invalid option for monotonic. Use 'remove dips' or 'remove spikes'.")
                
        return pts



    x_vy_points = make_monotonic(x_vy_points, monotonic=monotonic) # Run the above helper function to make the data monotonic, so that we can use PCHIP interpolation.


    xs_plot, vys_plot = zip(*x_vy_points)
    
    f = PchipInterpolator(xs_plot, vys_plot)

    x_eval = np.linspace(x_min, x_max, 300)
    
    # xs_plot, vys_plot = zip(*x_vy_points)

    # plt.scatter(xs_plot, vys_plot, s=10)
    plt.xlabel('x')
    plt.ylabel('vy')
    plt.title('vy vs x')
    plt.grid(True)
    plt.tight_layout()
    plt.plot(x_eval, f(x_eval), label='interpolant', alpha=0.5)
    plt.legend()

    plt.show()
    
    
    
    
    
    
    
    
    
    

    

# Correct function to run interpolation for a single p and x_val orbital crossings.
def run_single_interpolation(x_vy_points, ax, show_plot=True, interpolation_method="Lagrange", chebyshev_points=False, num_points_for_chebyshev=10):
    x_min, x_max = -0.75, 0
    y_min, y_max = 0, 6

    
    # Check to make sure there are enough points to select the desired number of Chebyshev points
    if chebyshev_points == True and len(x_vy_points) < num_points_for_chebyshev+1:
        raise ValueError(f"Not enough points to select {num_points_for_chebyshev}+1 Chebyshev points. Only {len(x_vy_points)} points available.")
    
    
    
    # Getting the Chebyshev points here is only intended to be used for the Lagrange interpolation here.
    if chebyshev_points == True:
        x_vy_points = selecting_chebyshev_points(x_vy_points, p=num_points_for_chebyshev)      # Choose some points close to Chebyshev nodes to get a better interpolation


    f = lagrange_interpolate_points(x_vy_points)    # I am basically just doing this to initialise f, to avoid weird errors later with ax.plot(x_eval, f(x_eval), label='interpolant'). Not sure why this is happening, but this fixes it.
    

    if chebyshev_points == True:                    #For some reason ax.plot freaks out again if I put this within the if statement below. Not sure why, but this fixes it.
        label = "Lagrange with Chebysheved points"
    elif chebyshev_points == False:
        label = "Lagrange without Chebysheved points"
        
        
    if interpolation_method == "lagrange":
        
        # if chebyshev_points == True:
        #     label = "Lagrange with Chebysheved points"
        # elif chebyshev_points == False:
        #     label = "Lagrange without Chebysheved points"
            
        f = lagrange_interpolate_points(x_vy_points)
        
        



    x_eval = np.linspace(x_min, x_max, 300)


    # return x_eval, f(x_eval)


    #------- COMMENT OUT THIS FOR NOTE IN test_run_single_interpolation() --------
    # ax.plot(x_eval, f(x_eval), label='interpolant')
    ax.plot(x_eval, f(x_eval), label=label)
    ax.legend()
    
    if show_plot == True:
        plt.show()
    else:
        return ax
    #---------------------------------------------------------------------------------





    
def test_run_single_interpolation():
    
    
    
    ###UNCOMMENT THIS IF YOU WANT TO PUT MULTIPLE THINGS ON THE SAME PLOT (NOTE THAT THE SECOND ONE IS ALSO USING "ax****1*****")
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # x_vy_points,fig,ax1 = get_list_of_points(max_p = 10, x_value = 0.1, quadrant = "top left", plot_points = False)
    # run_single_interpolation(x_vy_points, ax1, show_plot=False, interpolation_method="Lagrange", chebyshev_points=True, num_points_for_chebyshev=5)
        
    # x_vy_points,fig,ax = get_list_of_points(max_p = 10, x_value = 0.1, quadrant = "top left", plot_points = False)
    # ax = run_single_interpolation(x_vy_points, ax1, show_plot=True, interpolation_method="Lagrange", chebyshev_points=False, num_points_for_chebyshev=5)
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    
    
    x_vy_points,fig,ax1 = get_list_of_points(max_p = 10, x_value = 0.01, quadrant = "top left", plot_points = False)
    run_single_interpolation(x_vy_points, ax1, show_plot=True, interpolation_method="Lagrange", chebyshev_points=False, num_points_for_chebyshev=5)
    
    
    x_vy_points,fig,ax1 = get_list_of_points(max_p = 10, x_value = 0.1, quadrant = "top left", plot_points = False)
    run_single_interpolation(x_vy_points, ax1, show_plot=True, interpolation_method="Lagrange", chebyshev_points=False, num_points_for_chebyshev=5)
    
    
    x_vy_points,fig,ax = get_list_of_points(max_p = 10, x_value = 0.1, quadrant = "top left", plot_points = False)
    ax = run_single_interpolation(x_vy_points, ax, show_plot=True, interpolation_method="Lagrange", chebyshev_points=True, num_points_for_chebyshev=5)
    
    
    x_vy_points,fig,ax = get_list_of_points(max_p = 20, x_value = 0.1, quadrant = "top left", plot_points = False)
    ax = run_single_interpolation(x_vy_points, ax, show_plot=True, interpolation_method="Lagrange", chebyshev_points=True, num_points_for_chebyshev=10)
        
        
    
    
    
    
    
    
    ### IF I WANT TO BE ABLE TO PRINT A LOT OF THINGS WITHOUT PRINTING A PLOT EACH TIME, I CAN UNCOMMENT THIS BELOW, AND ALSO COMMENT OUT THE SECTION IN run_single_interpolation DEMARKCATED BY "------- COMMENT OUT THIS FOR NOTE IN test_run_single_interpolation() --------"
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # x_vy_points,fig,ax1 = get_list_of_points(max_p = 10, x_value = 0.1, quadrant = "top left", plot_points = False)
    # x_eval1, f_values1 = run_single_interpolation(x_vy_points, ax1, show_plot=False, interpolation_method="Lagrange", chebyshev_points=True, num_points_for_chebyshev=5)
        
    
    # x_vy_points,fig,ax = get_list_of_points(max_p = 10, x_value = 0.1, quadrant = "top left", plot_points = False)
    # x_eval2, f_values2 = run_single_interpolation(x_vy_points, ax1, show_plot=True, interpolation_method="Lagrange", chebyshev_points=False, num_points_for_chebyshev=5)
        
    
    # ax.plot(x_eval1, f_values1, label='interpolant1')
    # ax.plot(x_eval2, f_values2, label='interpolant2')
    # ax.legend()
    
        
    # plt.show()
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        
test_run_single_interpolation()

    
# Helper function for anytime we do PCHIP interpolation.
# Remove some points to make sure the data is monotonic. This lets us use PCHIP interpolation.
# As the data is supposed to be monotonic, minus the noise we have, this is reasonable to do.
def make_monotonic(points, monotonic="remove spikes"):
    
    # This first if block makes it monotonic by removing the 'dips' rather than the 'spikes'.
    # E.g.: if I have the points (0,1),(1,3),(2,2), it removes (2,2).
    # But from visual inspection, I think it would be better if it removed (1,3)
    if monotonic == "remove dips":
        
        monotonic = [points[0]]
        for p in points[1:]:
            if p[1] > monotonic[-1][1]:
                monotonic.append(p)
        pts = monotonic
    
    # This second block makes it monotonic by removing the 'spikes' rather than the 'dips', in contrast to the above.
    # It seems to lead to 'smoother' curves.
    elif monotonic == "remove spikes":    
        pts = list(points)
        changed = True
        while changed:
            changed = False
            new_pts = [pts[0]]
            for i in range(1, len(pts) - 1):
                prev_y = new_pts[-1][1]
                next_y = pts[i + 1][1]
                curr_y = pts[i][1]
                if curr_y > prev_y and curr_y > next_y:  # it's a spike
                    changed = True  # skip this point
                else:
                    new_pts.append(pts[i])
            new_pts.append(pts[-1])
            pts = new_pts
            
    else:
        raise ValueError("Invalid option for monotonic. Use 'remove dips' or 'remove spikes'.")
            
    return pts







# Helper function that implements a rolling-average smoothing process, comparing points to points nearby in x-value (the exact definition of 'nearby' is determined by the window parameter).
def smooth_points(points, window=0.02):
    """
    Smooth points by replacing each vy with the average of neighbors
    within x_radius in x value.
    """
    pts = list(points)
    smoothed = []
    for i in range(len(pts)):
        xi = pts[i][0]
        neighbors_vy = [p[1] for p in pts if abs(p[0] - xi) <= window]
        avg_vy = np.mean(neighbors_vy)
        smoothed.append((xi, avg_vy))
    return smoothed





# Correct function for running any type of interpolation on points from multiple different p:1 families, and with possibly different x_vals.
def run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="Lagrange", chebyshev_points=False, smooth_points_window=0, smoothing_times=0, print_plot=True, extrapolate=True, hard_code_label="false", num_chebyshev_points=10):
    """
    If you want to print out the plot after just one interpolation, you can set print_plot = True.
    
    If you want to do multiple interpolations and only print the plot at the end, you can set print_plot = False, and then call this function multiple times with the same ax, and then call plt.show() at the end.
    For example, you could this this like shown in the method demonstrate_multiple_plottings_in_one(), seen below.
    
    If smoothing_times > 0, then the code will implement a sort of rolling average smoothing process, where outlying points become less prominent because all of the points are averaged together in a nice way.
    It does so by looking at points in a nearby 'window' (nearby in the sense of points with close x-values to a point). You can specify how large you want this window to be with the smooth_points_window parameter.
    Note that this is not a simple rolling average, but rather an average of points with close x-values, which I think makes more sense for our data.
    
    If hard_code_label is not "false", then it will simply print the inputed, hardcoded label (specify this in the same parameter itself: hard_code_label). Otherwise: just use the label convention specified within this method.
    """
    
    
    x_min, x_max = -0.75, 0
    y_min, y_max = 0, 6

    p_arr = p_arr
    x_val_arr = x_val_arr
    
    label = "interpolant" # This is just to initialise it, it will be changed later on in the code.
    
    if print_plot == True:
        #This part is just to get the plot loaded.
        #--------------------------------------------------------------------------------------------------------------
        data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
        
        orbits      = data["orbits"]
        crossings   = data["crossings"]
        families_id = data["families_str"]
        earth_crash_x0 = np.array([])
        earth_crash_vx0 = np.array([])
        earth_crash_vy0 = np.array([])
        moon_crash_x0  = np.array([])
        moon_crash_vx0  = np.array([])
        moon_crash_vy0  = np.array([])

        fig = plt.figure(figsize=(12,8))
        ax = fig.add_subplot(111)

        ax.set_xlim(-0.5, 0)
        ax.set_ylim(-0.1, 6)


        ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                        earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                        plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False)
        #--------------------------------------------------------------------------------------------------------------
    
    
    # if order_running == "last_time":
      
    #     ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
    #                     earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    #                     plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False)
    
    # if order_running == "middle":
    #     # Do nothing
    #     x=1
    
    
    
    
    x_vy_points = multiple_get_list_of_points(p_arr, x_val_arr, quadrant = "top left") # Get the (x, vy) points that we want to interpolate between.
                                                                                       # the "multiple" is because we are getting points from multiple different p:1 familes, and with possibly different x_vals.




    # Getting the Chebyshev points here is only intended to be used for the Lagrange interpolation here.
    if chebyshev_points == True:
        x_vy_points = selecting_chebyshev_points(x_vy_points, p=num_chebyshev_points)      # Choose some points close to Chebyshev nodes to get a better interpolation



    # if smooth_points_window > 0:
    #     for _ in range(smoothing_times):
            
    #         x_vy_points = make_monotonic(x_vy_points, monotonic="remove spikes") # Run the helper function make_monotonic to make the data monotonic, so that we can use PCHIP interpolation.
    #         x_vy_points = smooth_points(x_vy_points, window=smooth_points_window)   # Smooth the points by averaging each point with its neighbours, to make the curve smoother.
        
    #     # xs_plot, vys_plot = zip(*x_vy_points)
    #     # plt.scatter(xs_plot, vys_plot, s=10)
    #     # plt.show()
    
    
    if smooth_points_window > 0:
        for _ in range(smoothing_times):
            
            if interpolation_method == "PCHIP_remove_spikes":
                x_vy_points = make_monotonic(x_vy_points, monotonic="remove spikes") # Run the helper function make_monotonic to make the data monotonic, so that we can use PCHIP interpolation.
            elif interpolation_method == "PCHIP_remove_dips":
                x_vy_points = make_monotonic(x_vy_points, monotonic="remove dips") # Run the helper function make_monotonic to make the data monotonic, so that we can use PCHIP interpolation.
            
            if interpolation_method == "akima":
                x_vy_points = make_monotonic(x_vy_points, monotonic="remove dips")
            
            x_vy_points = smooth_points(x_vy_points, window=smooth_points_window)   # Smooth the points by averaging each point with its neighbours, to make the curve smoother.
        
        
        

    if interpolation_method == "lagrange":
        f = lagrange_interpolate_points(x_vy_points)
        
        if chebyshev_points == True:
            title = "Lagrange with Chebysheved points"
            label = "Lagrange interpolant, with Chebysheved points"
        elif chebyshev_points == False:
            title = "Lagrange without Chebysheved points"
            label = "Lagrange interpolant, without Chebysheved points"


    elif interpolation_method == "PCHIP_remove_spikes" or interpolation_method == "PCHIP_remove_dips":      # NOTE: It doesn't look monotonic because I am still printing out all of the points. But don't worry, it is only using the monotonicised points!
        
        if interpolation_method == "PCHIP_remove_spikes":
            monotonic_type = "remove spikes"
            title = "PCHIP with spikes removed"
            label = "PCHIP interpolant, with spikes removed"
        elif interpolation_method == "PCHIP_remove_dips":
            monotonic_type = "remove dips"
            title = "PCHIP with dips removed"
            label = "PCHIP interpolant, with dips removed"
            
        x_vy_points = make_monotonic(x_vy_points, monotonic=monotonic_type) # Run the helper function make_monotonic to make the data monotonic, so that we can use PCHIP interpolation.
            
        xs_plot, vys_plot = zip(*x_vy_points)
        
        f = PchipInterpolator(xs_plot, vys_plot)
        
    
    elif interpolation_method == "cubic_spline":
        xs_plot, vys_plot = zip(*x_vy_points)
        # f = PchipInterpolator(xs_plot, vys_plot)
        f = CubicSpline(xs_plot, vys_plot)
        title = "Cubic Spline Interpolation"
        label = "Cubic spline interpolant"
    
    
    elif interpolation_method == "akima":
    
        xs_plot, vys_plot = zip(*x_vy_points)
        f = Akima1DInterpolator(xs_plot, vys_plot)
        if extrapolate == True:
            f.extrapolate = True  # Extrapolates the curve beyond the endpoints in a (hopefully) reasonable way.
        title = "Akima Interpolation"
        label = "Akima interpolant"

    

    if smooth_points_window > 0:
        label += f", smoothing (window={smooth_points_window}, times={smoothing_times})"

    
    x_eval = np.linspace(x_min, x_max, 300)
    
    # xs_plot, vys_plot = zip(*x_vy_points)

    # plt.scatter(xs_plot, vys_plot, s=10)
    plt.xlabel('x')
    plt.ylabel('vy')
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    
    if hard_code_label != "false":
        label = hard_code_label
    
    
    plt.plot(x_eval, f(x_eval), label=label, alpha=0.5)
    plt.legend()
    
    
    if print_plot == True:
        plt.show()
    



    









    

    
    
    
    
### BASICALLY DEPRECATED. USE run_all_interpolations() INSTEAD.
#These are all of the tests/interpolations that I have made. Use run_all_interpolations instead.
def run_interpolations():
    
    # test_single_interpolation()
    # test_multiple_interpolation()
    
    
    
    p_arr=[8,9]
    x_val_arr=[0.08, 0.08]
    
    PCHIP_interpolation(p_arr, x_val_arr, monotonic="remove spikes")
    PCHIP_interpolation(p_arr, x_val_arr, monotonic="remove dips")
    
    
# run_interpolations()









# These are a test of a bunch of my interpolations.
def run_all_interpolations():

        
    # test_run_single_interpolation()



    # p_arr=[8,9]
    # x_val_arr=[0.08, 0.08]
    # # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="lagrange", chebyshev_points=True)


    # p_arr=[8,9,10,11,12]
    # x_val_arr=[0.08, 0.08, 0.08, 0.08, 0.08]
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    
    p_arr=[8,9,10,11,12]
    x_val_arr=[0.01, 0.01, 0.01, 0.01, 0.01]
        
    # # # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="lagrange", chebyshev_points=False)


    axes = run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="PCHIP_remove_spikes", chebyshev_points=False, print_plot=False)
    # #run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="PCHIP_remove_dips", chebyshev_points=False)
    
    
    
    # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="cubic_spline", chebyshev_points=False)
    
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, print_plot=False)
    
    
    
    
    # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.005, smoothing_times=1)
    
    
    
    # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.005, smoothing_times=2)
    
    
    
    # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.005, smoothing_times=3)
    
    
    
        
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.005, smoothing_times=1, print_plot=False)
    
    
    
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.003, smoothing_times=1, print_plot=False)
    
    
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.002, smoothing_times=1, print_plot=False) ###THIS ONE LOOKS THE BEST I THINK.
    
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.001, smoothing_times=1, print_plot=False) ### With f.extrapolate, this one looks better.
    
    
    
    p_arr=[8,9,10,11,12]
    x_val_arr=[0.08, 0.08, 0.08, 0.08, 0.08]
    
    
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.005, smoothing_times=1, print_plot=False)
    
    
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.003, smoothing_times=1,print_plot=False)



    data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    orbits      = data["orbits"]
    crossings   = data["crossings"]
    families_id = data["families_str"]
    earth_crash_x0 = np.array([])
    earth_crash_vx0 = np.array([])
    earth_crash_vy0 = np.array([])
    moon_crash_x0  = np.array([])
    moon_crash_vx0  = np.array([])
    moon_crash_vy0  = np.array([])




    ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False)
    
    
    
    p_arr=[8,9,10,11,12]
    x_val_arr=[0.01, 0.01, 0.01, 0.01, 0.01]
    
    data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    
    orbits      = data["orbits"]
    crossings   = data["crossings"]
    families_id = data["families_str"]
    earth_crash_x0 = np.array([])
    earth_crash_vx0 = np.array([])
    earth_crash_vy0 = np.array([])
    moon_crash_x0  = np.array([])
    moon_crash_vx0  = np.array([])
    moon_crash_vy0  = np.array([])

    ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=False, print_legend=False)
    
    
    
    
    
    
    # p_arr=[14,18,20]
    # x_val_arr=[0.2,0.2,0.2]
    
    
    # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.005, smoothing_times=1, print_plot=False)
    
    
    # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.003, smoothing_times=1,print_plot=False)



    # data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    # orbits      = data["orbits"]
    # crossings   = data["crossings"]
    # families_id = data["families_str"]
    # earth_crash_x0 = np.array([])
    # earth_crash_vx0 = np.array([])
    # earth_crash_vy0 = np.array([])
    # moon_crash_x0  = np.array([])
    # moon_crash_vx0  = np.array([])
    # moon_crash_vy0  = np.array([])




    # ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
    #                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    #                 plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=False, print_legend=False)
    
    
    
    

    plt.show()
    

run_all_interpolations()





# Generate Figure 11 in the paper.
def run_fig_11():
    
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    
    
    
    p_arr=[8,9,10,11,12]
    x_val_arr=[0.01, 0.01, 0.01, 0.01, 0.01]
        
    # # # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="lagrange", chebyshev_points=False)
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="lagrange", chebyshev_points=True, print_plot=False, num_chebyshev_points=10, hard_code_label="Lagrange with Chebyshev points, x_val=0.01")
    
    p_arr=[8,9,10,11,12]
    x_val_arr=[0.1, 0.1, 0.1, 0.1, 0.1]
        
    # # # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="lagrange", chebyshev_points=False)
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="lagrange", chebyshev_points=True, print_plot=False, num_chebyshev_points=10, hard_code_label="Lagrange with Chebyshev points, x_val=0.1")
    
    
    
    
    
    
    p_arr=[8,9,10,11,12]
    x_val_arr=[0.01, 0.01, 0.01, 0.01, 0.01]
    
    data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    
    orbits      = data["orbits"]
    crossings   = data["crossings"]
    families_id = data["families_str"]
    earth_crash_x0 = np.array([])
    earth_crash_vx0 = np.array([])
    earth_crash_vy0 = np.array([])
    moon_crash_x0  = np.array([])
    moon_crash_vx0  = np.array([])
    moon_crash_vy0  = np.array([])

    ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=False, print_legend=False, show_crash_region=False)
    
    
    
    
    p_arr=[8,9,10,11,12]
    x_val_arr=[0.1, 0.1, 0.1, 0.1, 0.1]
    
    data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    
    orbits      = data["orbits"]
    crossings   = data["crossings"]
    families_id = data["families_str"]
    earth_crash_x0 = np.array([])
    earth_crash_vx0 = np.array([])
    earth_crash_vy0 = np.array([])
    moon_crash_x0  = np.array([])
    moon_crash_vx0  = np.array([])
    moon_crash_vy0  = np.array([])

    ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False, show_crash_region=True)
    
    

    plt.show()
    
run_fig_11()


def run_fig_12():
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    
    p_arr=[8,9,10,11,12]
    x_val_arr=[0.01, 0.01, 0.01, 0.01, 0.01]
    
    
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="cubic_spline", chebyshev_points=False)
    
    
    


run_fig_12()







# Just a method to demonstrate how I can run multiple different interpolations and plots on the same plot, without having to print the plot each time.
def demonstrate_multiple_plottings_in_one():

    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    
    
    
    p_arr=[8,9,10,11,12]
    x_val_arr=[0.01, 0.01, 0.01, 0.01, 0.01]
        

    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="PCHIP_remove_spikes", chebyshev_points=False, print_plot=False)
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, print_plot=False)
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.001, smoothing_times=1, print_plot=False) ### With f.extrapolate, this value for smooth_points_window=0.001 looks best, I think.
    
    
    
    p_arr=[8,9,10,11,12]
    x_val_arr=[0.08, 0.08, 0.08, 0.08, 0.08]
    
    
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.005, smoothing_times=1, print_plot=False)    
    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.003, smoothing_times=1,print_plot=False)



    data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    orbits      = data["orbits"]
    crossings   = data["crossings"]
    families_id = data["families_str"]
    earth_crash_x0 = np.array([])
    earth_crash_vx0 = np.array([])
    earth_crash_vy0 = np.array([])
    moon_crash_x0  = np.array([])
    moon_crash_vx0  = np.array([])
    moon_crash_vy0  = np.array([])


    ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False)
    
    
    p_arr=[8,9,10,11,12]
    x_val_arr=[0.01, 0.01, 0.01, 0.01, 0.01]
    
    data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    
    orbits      = data["orbits"]
    crossings   = data["crossings"]
    families_id = data["families_str"]
    earth_crash_x0 = np.array([])
    earth_crash_vx0 = np.array([])
    earth_crash_vy0 = np.array([])
    moon_crash_x0  = np.array([])
    moon_crash_vx0  = np.array([])
    moon_crash_vy0  = np.array([])

    ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False)

    plt.show()
    
    
    
    
    ### Also note that I can run it with print_plot=True like so:

    p_arr=[8,9,10,11,12]
    x_val_arr=[0.08, 0.08, 0.08, 0.08, 0.08]


    run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.005, smoothing_times=1, print_plot=True)









def make_evenly_spaced_plot(interpolation_method="akima", chebyshev_points=False, p_arr=[8,9,10,11,12], possible_x_vals=[0.01, 0.02, 0.03, 0.04, 0.06, 0.08]):
    
    
    interpolation_method = interpolation_method
    chebyshev_points = chebyshev_points
    
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    
    
    
    # p_arr=[8,9,10,11,12]
    # # x_val_arr=[0.01, 0.01, 0.01, 0.01, 0.01]
    
    # possible_x_vals = [0.01, 0.02, 0.03, 0.04, 0.06, 0.08]
    
    p_arr = p_arr
    possible_x_vals = possible_x_vals
    
    
    
    
    # # This whole block is just doing the 
    # ###----------------------------------------------------------------------------------------------------------------------------------------------------------------
    # val = possible_x_vals[0]
    
    
    # x_val_arr = np.full(len(p_arr), val) # make x_val_arr look like [val, val, ..., val]
    
    
    # # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="PCHIP_remove_spikes", chebyshev_points=False, print_plot=False)
    # # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, print_plot=False)
    # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.001, smoothing_times=1, print_plot=False, extrapolate=False) ### With f.extrapolate, this value for smooth_points_window=0.001 looks best, I think.
    
        

    # data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    # orbits      = data["orbits"]
    # crossings   = data["crossings"]
    # families_id = data["families_str"]
    # earth_crash_x0 = np.array([])
    # earth_crash_vx0 = np.array([])
    # earth_crash_vy0 = np.array([])
    # moon_crash_x0  = np.array([])
    # moon_crash_vx0  = np.array([])
    # moon_crash_vy0  = np.array([])
    
        
    # ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
    #                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    #                 plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False, show_crash_region=True)
    # ###----------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    
    
    
    
    method_for_label = ""
    
    match interpolation_method:
        case "akima":     
            method_for_label = "Akima"
        case "lagrange":
            method_for_label = "Lagrange"
        case "PCHIP_remove_spikes":
            method_for_label = "PCHIP, sans spikes"
        case "PCHIP_remove_dips":
            method_for_label = "PCHIP, sans dips"
        case "cubic_spline":
            method_for_label = "Cubic Spline"
    
    
    

    ax = plot_2D_crash_region_and_accessible_region(ax, which="vy", show_only_lower_quadrant=True, show_accessible_region=True, print_legend=False, show_crash_region=True)

    
    for val in possible_x_vals: # For all x_vals
        
        x_val_arr = np.full(len(p_arr), val) # make x_val_arr look like [val, val, ..., val]
        
        # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="PCHIP_remove_spikes", chebyshev_points=False, print_plot=False)
        # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, print_plot=False)
        
        
        
        # formatted = ', '.join(f"{p}:1" for p in p_arr)
        # label = "Akima, smoothed, (" + formatted + f"), x_val = {val}"
        
        formatted = ', '.join(f"{p}:1" for p in p_arr)
        label = method_for_label + ", smoothed, (" + formatted + f"), x_val = {val}"
        
        
        ### Change "extrapolate" to True in the following if you want to predict what the curve will do after the edges. Be warned, however, that it doesn't do that very well.
        run_multiple_interpolation(p_arr, x_val_arr, interpolation_method=interpolation_method, chebyshev_points=chebyshev_points, smooth_points_window=0.001, smoothing_times=1, print_plot=False, extrapolate=False,
                                   hard_code_label = label ) ### With f.extrapolate, this value for smooth_points_window=0.001 looks best, I think.

        
        data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
        
        orbits      = data["orbits"]
        crossings   = data["crossings"]
        families_id = data["families_str"]
        earth_crash_x0 = np.array([])
        earth_crash_vx0 = np.array([])
        earth_crash_vy0 = np.array([])
        moon_crash_x0  = np.array([])
        moon_crash_vx0  = np.array([])
        moon_crash_vy0  = np.array([])
        
        
        # print("--------------------------------------------------------------------------------")
        # print("LABELS", orbits)
        # print("--------------------------------------------------------------------------------")
        
    
        
        if val == possible_x_vals[0]: # If this is the first time looping, show the crash region and the accessible region boundary
            # ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
            #                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
            #                 plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False, show_crash_region=True)
             ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                            earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                            plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=False, print_legend=False, show_crash_region=False)
        else:   # Otherwise, dont show those (note show_accessible_region=False, show_crash_region=False). This is so that the plot doesn't plot it a bunch of times unnecessarily.
            ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                            earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                            plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=False, print_legend=False, show_crash_region=False)
            
    plt.title("")
    # plt.title("Interpolations for various orbital data")
    ## plt.title("Interpolations for various orbital data, with edge extrapolation")
    
    

    # data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    # orbits      = data["orbits"]
    # crossings   = data["crossings"]
    # families_id = data["families_str"]
    # earth_crash_x0 = np.array([])
    # earth_crash_vx0 = np.array([])
    # earth_crash_vy0 = np.array([])
    # moon_crash_x0  = np.array([])
    # moon_crash_vx0  = np.array([])
    # moon_crash_vy0  = np.array([])
    
    
    # # data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
    
    # # orbits      = np.array([])
    # # crossings   = np.array([])
    # # families_id = np.array([])
    # # earth_crash_x0 = np.array([])
    # # earth_crash_vx0 = np.array([])
    # # earth_crash_vy0 = np.array([])
    # # moon_crash_x0  = np.array([])
    # # moon_crash_vx0  = np.array([])
    # # moon_crash_vy0  = np.array([])


    # ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
    #                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    #                 plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False)
    
        
    plt.show()
        


##Uncomment this one
make_evenly_spaced_plot(interpolation_method="lagrange", chebyshev_points=True, p_arr=[8,9,10,11,12], possible_x_vals=[0.01, 0.02, 0.03, 0.04, 0.06, 0.08])


# make_evenly_spaced_plot(interpolation_method="lagrange", chebyshev_points=True, p_arr=[8,9,10,11,12], possible_x_vals=[0.01, 0.02, 0.04, 0.06, 0.08, 0.1])


# make_evenly_spaced_plot(interpolation_method="cubic_spline", chebyshev_points=False, p_arr=[8,9,10,11,12], possible_x_vals=[0.01, 0.02, 0.04, 0.06, 0.08, 0.1])




# Makes the PCHIP plots
def run_fig_14_15():
        
    
    # fig = plt.figure(figsize=(12,8))
    # ax = fig.add_subplot(111)

    # ax.set_xlim(-0.5, 0)
    # ax.set_ylim(-0.1, 6)
    
        
    # p_arr=[8,9,10,11,12]
    # possible_x_vals=[0.08, 0.08, 0.08, 0.08, 0.08]

    # run_multiple_interpolation(p_arr=p_arr, x_val_arr=possible_x_vals, interpolation_method="PCHIP_remove_spikes", chebyshev_points=False, print_plot=False)
    # run_multiple_interpolation(p_arr=p_arr, x_val_arr=possible_x_vals, interpolation_method="PCHIP_remove_dips", chebyshev_points=False, print_plot=False)
    
    # plt.show()
    
    
    p_arr=[8,9,10,11,12]
    possible_x_vals=[0.01, 0.02, 0.03, 0.04, 0.06, 0.08]
    
    make_evenly_spaced_plot(interpolation_method="PCHIP_remove_spikes", chebyshev_points=False, p_arr=p_arr, possible_x_vals=possible_x_vals)
    make_evenly_spaced_plot(interpolation_method="PCHIP_remove_dips", chebyshev_points=False, p_arr=p_arr, possible_x_vals=possible_x_vals)


run_fig_14_15()



def run_fig_16():
    
    p_arr=[8,9,10,11,12]
    possible_x_vals=[0.01, 0.02, 0.03, 0.04, 0.06, 0.08]
    
    make_evenly_spaced_plot(interpolation_method="akima", chebyshev_points=False, p_arr=p_arr, possible_x_vals=possible_x_vals)
    
run_fig_16()




def make_figure_with_points_wihtout_curves():
    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    
    
    
    p_arr = [8]
    possible_x_vals=[0.08]
    
    
    ax = plot_2D_crash_region_and_accessible_region(ax, which="vy", show_only_lower_quadrant=True, show_accessible_region=True, print_legend=False, show_crash_region=True)
    
    
    
    
    for val in possible_x_vals: # For all x_vals
        
        x_val_arr = np.full(len(p_arr), val) # make x_val_arr look like [val, val, ..., val]
        
        # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="PCHIP_remove_spikes", chebyshev_points=False, print_plot=False)
        # run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, print_plot=False)
        
        
        
        # formatted = ', '.join(f"{p}:1" for p in p_arr)
        # label = "Akima, smoothed, (" + formatted + f"), x_val = {val}"
        
        formatted = ', '.join(f"{p}:1" for p in p_arr)
        label = formatted + f"), x_val = {val}"
        
        
        data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")
        
        orbits      = data["orbits"]
        crossings   = data["crossings"]
        families_id = data["families_str"]
        earth_crash_x0 = np.array([])
        earth_crash_vx0 = np.array([])
        earth_crash_vy0 = np.array([])
        moon_crash_x0  = np.array([])
        moon_crash_vx0  = np.array([])
        moon_crash_vy0  = np.array([])
        
        
        # print("--------------------------------------------------------------------------------")
        # print("LABELS", orbits)
        # print("--------------------------------------------------------------------------------")
        
    
        
        if val == possible_x_vals[0]: # If this is the first time looping, show the crash region and the accessible region boundary
            # ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
            #                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
            #                 plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True, print_legend=False, show_crash_region=True)
             ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                            earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                            plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=False, print_legend=True, show_crash_region=False)
        else:   # Otherwise, dont show those (note show_accessible_region=False, show_crash_region=False). This is so that the plot doesn't plot it a bunch of times unnecessarily.
            ax = plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
                            earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                            plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=False, print_legend=False, show_crash_region=False)
            
            
    # plt.title("Interpolations for various orbital data")
    # # plt.title("Interpolations for various orbital data, with edge extrapolation")
    
    ax.legend(loc='upper right', bbox_to_anchor=(1, 0.5))
    plt.show()

    
    
    
#make_figure_with_points_wihtout_curves()
    





# fig = plt.figure(figsize=(12,8))
# ax = fig.add_subplot(111)

# ax.set_xlim(-0.5, 0)
# ax.set_ylim(-0.1, 6)


# p_arr=[14,18,20]
# x_val_arr=[0.2,0.2,0.2]



# run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.005, smoothing_times=1, print_plot=False)


# run_multiple_interpolation(p_arr, x_val_arr, interpolation_method="akima", chebyshev_points=False, smooth_points_window=0.003, smoothing_times=1,print_plot=False)



# data = multiple_isolate_one_quadrant(p_arr, x_val_arr, quadrant="top left")

# orbits      = data["orbits"]
# crossings   = data["crossings"]
# families_id = data["families_str"]
# earth_crash_x0 = np.array([])
# earth_crash_vx0 = np.array([])
# earth_crash_vy0 = np.array([])
# moon_crash_x0  = np.array([])
# moon_crash_vx0  = np.array([])
# moon_crash_vy0  = np.array([])




# plot_Poincare_2D_without_printing(ax, orbits, crossings, families_id, 
#                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
#                 plot_second_crossings = True, which="vy",show_only_lower_quadrant=True, show_accessible_region=True, print_legend=True)

# plt.show()