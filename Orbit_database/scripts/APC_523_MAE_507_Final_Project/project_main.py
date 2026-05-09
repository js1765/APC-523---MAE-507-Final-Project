"""
Code for my final project for APC 523/MAE 507 (Numerical Methods for Scientific Computing) at Princeton, Winter Semester 2026.
======================================
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) #This is so that this file knows the correct path to take, since I put it in a folder.

from project_orbit_data import gather_analytic_resonant_with_specified_p_and_x_value, gather_analytic_resonant, merge_datasets
# from support.plot import plot_given_boxes, plot_Poincare_2D_with_boxes, plot_Poincare_2D_with_balls, plot_Poincare_2D, plot_Poincare_3D, plot_Poincare_analytic, plot_cross_section_x_vy, plot_cross_section_x_vy_individual, plot_Poincare_2D_without_printing
from project_plot import plot_Poincare_2D, plot_Poincare_3D, plot_Poincare_analytic, plot_Poincare_2D_without_printing
import numpy as np
from support.rectangle_calculations import Rect_Poincare_2D_get_boxes, calculate_mega_box
import matplotlib.pyplot as plt


np.set_printoptions(legacy='1.25') # This is just to make the printed output of numpy arrays a bit more readable, for some reason the default without it is to display numbers in the most bulky and hard to read way possible.



# def load_exact_data():
#     data = gather_dataset(
#         plot_second_crossings = True,
#         load_lunar                   = False,
#         load_prograde_resonant    = False,
#         load_prograde_resonant_x1    = False,
#         load_retrograde_resonant     = False,
#         load_retrograde_resonant_x1  = True,
#         load_crash                   = False,
#         load_circular                = False,
#     )



#     orbits      = data["orbits"]
#     crossings   = data["crossings"]
#     families_id = data["families_str"]
#     earth_crash_x0 = data["earth_crash_x0"]
#     earth_crash_vx0 = data["earth_crash_vx0"]
#     earth_crash_vy0 = data["earth_crash_vy0"]
#     moon_crash_x0  = data["moon_crash_x0"]
#     moon_crash_vx0  = data["moon_crash_vx0"]
#     moon_crash_vy0  = data["moon_crash_vy0"]
    
#     return {
#         "orbits":        orbits,
#         "crossings":      crossings,
#         "families_str":   families_id,
#         "earth_crash_x0": earth_crash_x0,
#         "earth_crash_vx0": earth_crash_vx0,
#         "earth_crash_vy0": earth_crash_vy0,
#         "moon_crash_x0":  moon_crash_x0,
#         "moon_crash_vx0": moon_crash_vx0,
#         "moon_crash_vy0": moon_crash_vy0,
#     }

# #load_exact_data() 







# # ###Change max_p to get more orbits (up to max_p : 1), change x_value to get higher resolution (but beware of long runtimes for small x_value)
# data_analytic = gather_analytic_resonant(max_p = 8, x_value = 0.1)

# orbits_analytic      = data_analytic["orbits"]
# crossings_analytic   = data_analytic["crossings"]
# families_id_analytic = data_analytic["families_str"]


# # print("OKAY")


# print("-----------------------------------------------------------------------------------------------------")
# print("orbits_analytic: ", orbits_analytic)
# print("-----------------------------------------------------------------------------------------------------")
# print("crossings_analytic: ", crossings_analytic)
# print("-----------------------------------------------------------------------------------------------------")
# print("families_id_analytic: ", families_id_analytic)
# print("-----------------------------------------------------------------------------------------------------")



# print("-----------------------------------------------------------------------------------------------------")
# for (x,vx,vy,label) in orbits_analytic:
#     print(f"Orbit with label {label}: x={x}, vx={vx}, vy={vy}")
# print("-----------------------------------------------------------------------------------------------------")

# print("-----------------------------------------------------------------------------------------------------")
# for (x,vx,vy,label) in crossings_analytic:
#     print(f"Orbit with label {label}: x={x}, vx={vx}, vy={vy}")
# print("-----------------------------------------------------------------------------------------------------")





earth_crash_x0 = np.array([])
earth_crash_vx0 = np.array([])
earth_crash_vy0 = np.array([])
moon_crash_x0  = np.array([])
moon_crash_vx0  = np.array([])
moon_crash_vy0  = np.array([])



    
def translate_to_better_data_structure(input_structure):
    """
    This is just a little helper function to help translate between the inherited, reallty really unintuitive and unnecessarily complicated data structure, and something at least marginally easier to work with.
    This function translates both ways (so perhaps "translate_to_**better**_data_structure" is a bit of a misnomer, since it can translate both ways.)
    
    If given a list containing one tuple, unwrap it: [(a,b,c,d)] -> (a,b,c,d)
    If given a tuple, wrap it:                       (a,b,c,d)   -> [(a,b,c,d)]
    """
    if isinstance(input_structure, list) and len(input_structure) == 1 and isinstance(input_structure[0], tuple):
        return input_structure[0]          # unwrap
    elif isinstance(input_structure, tuple):
        return [input_structure]           # wrap
    else:
        raise ValueError(f"Unexpected input type: {type(input_structure)}. Expected a list-of-one-tuple or a tuple.")







def isolate_one_quadrant(max_p, x_value, quadrant):
    """
    Runs gather_analytic_resonant to get all crossing points, but this notably includes points in two quadrants, which is not necessary and will confuse our polynomial interpolation algorithm later.
    As such, this function basically just isolates all of the crossing points that are in the desired quadrant (specified in parameter input "quadrant"), and discards the rest.
    (The revelevant comparison is done in the compare_to_point function, which checks if a given point (x,vx,vy) is in the desired quadrant or not.)
    
    Returns a data structure in the same format as the original data structure returned by gather_analytic_resonant, but with only the crossings in the desired quadrant.
    The orbits and families_id are unchanged from the original gather_analytic_resonant output, since we are only filtering the crossings, not the orbits.
    (Indeed, as the "orbits" list is just a list of the initial conditions of the orbits, we very simply ensure that this will be in the desired quadrant by only giving initial conditions in that quadrant.)
    """
    
    # data_analytic = gather_analytic_resonant(max_p = max_p, step_dx = x_value)
    data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = max_p, x_value = x_value)
    
    
    orbits_analytic      = data_analytic["orbits"]
    crossings_analytic   = data_analytic["crossings"]
    families_id_analytic = data_analytic["families_str"]
    
    

    translated_orbits_analytic = translate_to_better_data_structure(orbits_analytic)
    translated_crossings_analytic = translate_to_better_data_structure(crossings_analytic)    
    ####print("FAMILIES ID ANALYTIC: ", families_id_analytic)
    # No need to do the same for families_id_analytic, since it has a different structure (list of strings, not list of tuples).
    
      
    # print("translated_crossings_analytic: ", translated_crossings_analytic)
    
    
    def compare_to_point(x,vx,vy,label):  #including the vx and label parameters here just in case for some future use I need them, but for the foreseeable future I really only need to consider (x,vy) for the 2D case.
        if quadrant == "top left":
            return (x < 0) and (vy > 0)
        elif quadrant == "top right":
            return (x > 0) and (vy > 0)
        elif quadrant == "bottom left":
            return (x < 0) and (vy < 0)
        elif quadrant == "bottom right":
            return (x > 0) and (vy < 0)
        else:
            raise ValueError(f"Invalid quadrant: {quadrant}. Expected one of 'top left', 'top right', 'bottom left', 'bottom right'.")
    
    
    
    number_of_crossings = len(translated_crossings_analytic[0]) #Note that translated_crossings_analytic[0] is the list of x values, and this has the same size as the lsit of vx values and the list of vy values.
    
    
    new_crossings = []

    new_xs = []
    new_vxs = []
    new_vys = []


    #For each point, see if its in the quadrant that we want (specified in parameter input "quadrant"), and collect only those which are.
    #-----------------------------------------------------------------------------------------------------
    for i in range(number_of_crossings): 
        
        x = translated_crossings_analytic[0][i]
        vx = translated_crossings_analytic[1][i]
        vy = translated_crossings_analytic[2][i]
        label = translated_crossings_analytic[3]
        
        
        # new_point = (x, vx, vy, label)
        
        # if compare_to_point(x,vx,vy,label):
        #     new_crossings.append(new_point)
        
        if compare_to_point(x,vx,vy,label):
            new_xs.append(x)
            new_vxs.append(vx)
            new_vys.append(vy)

        ##new_crossings = list(zip(new_xs, new_vxs, new_vys, [label]*len(new_xs)))  # Repackage the new_crossings list to be in the same format as the original crossings_analytic data structure, so that we can use it in the same plotting functions.
        # new_crossings = [list(np.array(new_xs)), list(np.array(new_vxs)), list(np.array(new_vys)), label]  # Repackage the new_crossings list to be in the same format as the original crossings_analytic data structure, so that we can use it in the same plotting functions.
        new_crossings = [(np.array(new_xs), np.array(new_vxs), np.array(new_vys), label)]  # Repackage the new_crossings list to be in the same (horrible) format as the original crossings_analytic data structure, so that we can use it in the same plotting functions.

        # translated_new_crossings = translate_to_better_data_structure(new_crossings)    # Repackage to the [()] data structure to use in plotting. ####THIS WASNT WORKING SO I DID THAT^
    #-----------------------------------------------------------------------------------------------------
    
    
    
    
    new_data = {
        "orbits":         orbits_analytic,
        "crossings":      new_crossings,
        "earth_crash_x0": np.array([]),   # none created here
        "earth_crash_vx0": np.array([]),
        "earth_crash_vy0": np.array([]),
        "moon_crash_x0":  np.array([]),
        "moon_crash_vx0": np.array([]),
        "moon_crash_vy0": np.array([]),
        "families_str":   "analytic_reso",
    }
    
    
    

    # # print("-----------------------------------------------------------------------------------------------------")

    # # for i in range(len(new_crossings)):
    # #     x = new_crossings[i][0]
    # #     vx = new_crossings[i][1]
    # #     vy = new_crossings[i][2]
    # #     label = new_crossings[i][3]
    # #     print(f"Crossing with label {label}: x={x}, vx={vx}, vy={vy}")

    # # print("-----------------------------------------------------------------------------------------------------")
    
 
    # print("-----------------------------------------------------------------------------------------------------")
    # print(crossings_analytic)
    # print("-----------------------------------------------------------------------------------------------------")
    # print(new_crossings)
    # print("-----------------------------------------------------------------------------------------------------")
    
    
    
    new_orbits_analytic = new_data["orbits"]
    new_crossings_analytic = new_data["crossings"]
    new_families_id_analytic = new_data["families_str"]
    
    

    # plot_Poincare_2D(new_orbits_analytic, new_crossings_analytic, new_families_id_analytic, 
    #                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    #                 plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, print_legend=False)
    
    
    
    

    # print(new_orbits_analytic)
    # print("-----------------------------------------------------------------------------------------------------")
    # print(new_crossings_analytic)
    
    return {
        "orbits":         new_orbits_analytic,
        "crossings":      new_crossings_analytic,
        "families_str":   new_families_id_analytic
    }
    
    
    




def get_list_of_points(max_p, x_value, quadrant, plot_points = False):
    """
    Applies isolate_one_quadrant to get the crossings in the specified quadrant, and then extracts the (x, vy) points from those crossings and saves them out as a list of tuples.
    The result is a list of tuples of the form [(x1, vy1), (x2, vy2), ...], which are the (x, vy) coordinates of the crossings that lie in the specified quadrant.
    The function also plots these points on a scatter plot for visualization if desired (i.e.: if plot_points = True).
    """
    

    data = isolate_one_quadrant(max_p = max_p, x_value = x_value, quadrant = quadrant)

    orbits_analytic      = data["orbits"]
    crossings_analytic   = data["crossings"]
    families_id_analytic = data["families_str"]


    translated_crossings_analytic = translate_to_better_data_structure(crossings_analytic)

    # print("translated_crossings_analytic: ", translated_crossings_analytic)
    
    
    # number_of_crossings = len(translated_crossings_analytic[0]) #Note that translated_crossings_analytic[0] is the list of x values, and this has the same size as the list of vx values and the list of vy values.
    # for i in range(number_of_crossings):
    #     x = translated_crossings_analytic[0][i]
    #     # vx = translated_crossings_analytic[1][i]
    #     vy = translated_crossings_analytic[2][i]
    #     # label = translated_crossings_analytic[3]
        

    xs = translated_crossings_analytic[0]
    vys = translated_crossings_analytic[2]
    # x_vy_points = list(zip(xs, vys))
    x_vy_points = sorted(zip(xs, vys), key=lambda point: point[0])  # While saving the points to this list, make sure to sort them by x value. This will be important later when we do polynomial interpolation.
   
    # for i in range(number_of_crossings):
    #     x = translated_crossings_analytic[0][i]
    #     # vx = translated_crossings_analytic[1][i]
    #     vy = translated_crossings_analytic[2][i]
    #     # label = translated_crossings_analytic[3]
    
    
    
    
    # orbits_analytic      = data["orbits"]
    # crossings_analytic   = data["crossings"]
    # families_id_analytic = data["families_str"]
        
        
        
    
    
    # print(x_vy_points)
        
        
        
        
        
    if plot_points == True:
        xs_plot, vys_plot = zip(*x_vy_points)

        plt.scatter(xs_plot, vys_plot, s=10)
        plt.xlabel('x')
        plt.ylabel('vy')
        plt.title('vy vs x')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        ##To see a line plot instead of a scatter plot, uncomment this:
        # plt.figure(figsize=(8, 5))
        # plt.plot(xs_plot, vys_plot)
        # plt.xlabel('x')
        # plt.ylabel('vy')
        # plt.title('vy vs x')
        # plt.grid(True)
        # plt.tight_layout()
        # plt.show()
    

    #To do multiple at once, comment out this bit, and uncomment the bit labelled "AAAAAAAA UNCOMMENT ME IF YOU WANT MULTIPLE"
    # -----------------------------------------------------------------------------------------------------")
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    # -----------------------------------------------------------------------------------------------------")
    
    
    plot_Poincare_2D_without_printing(ax, orbits_analytic, crossings_analytic, families_id_analytic,
                                      earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0,
                                      plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, print_legend=False, show_accessible_region=True)
    
    
    # # plt.show()

    
    return x_vy_points, fig, ax
    

# AAAAAAAA UNCOMMENT ME IF YOU WANT MULTIPLE" (see note at the end of get_list_of_points function for more details on this)
# -----------------------------------------------------------------------------------------------------")
# fig = plt.figure(figsize=(12,8))
# ax = fig.add_subplot(111)

# ax.set_xlim(-0.5, 0)
# ax.set_ylim(-0.1, 6)


# # get_list_of_points(8, 0.1, "top left", plot_points = False)
# # get_list_of_points(9, 0.1, "top left", plot_points = False)
# # get_list_of_points(10, 0.1, "top left", plot_points = False)
# # get_list_of_points(11, 0.1, "top left", plot_points = False)
# # get_list_of_points(12, 0.1, "top left", plot_points = False)
# # get_list_of_points(13, 0.1, "top left", plot_points = False)
# # get_list_of_points(14, 0.1, "top left", plot_points = False)
# # get_list_of_points(15, 0.1, "top left", plot_points = False)
# # plt.show()


# get_list_of_points(8, 0.08, "top left", plot_points = False)
# plt.show()
# -----------------------------------------------------------------------------------------------------")









# x_vy_points = get_list_of_points(max_p = 8, x_value = 0.1, quadrant = "top left", plot_points = False)

# print("x_vy_points: ", x_vy_points)








def test_translate_to_better_data_structure():
        

    # ###Change max_p to get more orbits (up to max_p : 1), change x_value to get higher resolution (but beware of long runtimes for small x_value)
    # data_analytic = gather_analytic_resonant(max_p = 8, x_value = 0.1)
    
    data_analytic = gather_analytic_resonant(max_p = 8, step_dx = 0.1)

    orbits_analytic      = data_analytic["orbits"]
    crossings_analytic   = data_analytic["crossings"]
    families_id_analytic = data_analytic["families_str"]



    translated_orbits_analytic = translate_to_better_data_structure(orbits_analytic)


    print("-----------------------------------------------------------------------------------------------------")
    print("translated_orbits_analytic: ", translated_orbits_analytic)
    print("-----------------------------------------------------------------------------------------------------")


    translated_orbits_analytic = translate_to_better_data_structure(translated_orbits_analytic)


    print("-----------------------------------------------------------------------------------------------------")
    print("translated_orbits_analytic: ", translated_orbits_analytic)
    print("-----------------------------------------------------------------------------------------------------")


def test_isolate_one_quadrant(max_p = 8, x_value = 0.08, quadrant = "top left"):
    

    data = isolate_one_quadrant(max_p = max_p, x_value = x_value, quadrant = quadrant)
    # data = isolate_one_quadrant(max_p = 8, x_value = 0.08, quadrant = "bottom right")

    orbits_analytic      = data["orbits"]
    crossings_analytic   = data["crossings"]
    families_id_analytic = data["families_str"]

    # # print("orbits_analytic: ", orbits_analytic)
    # print("crossings_analytic: ", crossings_analytic)

    translated_crossings_analytic = translate_to_better_data_structure(crossings_analytic)

    print("translated_crossings_analytic: ", translated_crossings_analytic)



    number_of_crossings = len(translated_crossings_analytic[0]) #Note that translated_crossings_analytic[0] is the list of x values, and this has the same size as the lsit of vx values and the list of vy values.
    print("-----------------------------------------------------------------------------------------------------")
    for i in range(number_of_crossings): #Note that crossings_analytic[0] is the list of x values, and this has the same size as the lsit of vx values and the list of vy values.
        x = translated_crossings_analytic[0][i]
        vx = translated_crossings_analytic[1][i]
        vy = translated_crossings_analytic[2][i]
        label = translated_crossings_analytic[3]
        print(f"Crossing with label {label}: x={x}, vx={vx}, vy={vy}")
    print("-----------------------------------------------------------------------------------------------------")



    plot_Poincare_2D(orbits_analytic, crossings_analytic, families_id_analytic, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, print_legend=False)
    


# test_translate_to_better_data_structure()

# test_isolate_one_quadrant(8,0.08,"top left")
# # test_isolate_one_quadrant(8,0.08,"bottom right")
# test_isolate_one_quadrant(9,0.08,"top left")










# print("-----------------------------------------------------------------------------------------------------")
# print("-----------------------------------------------------------------------------------------------------")


# # data1 = isolate_one_quadrant(8,0.08,"top left")
# data1 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.08)
# orbits1      = data1["orbits"]
# crossings1   = data1["crossings"]
# families_id1 = data1["families_str"]

# # print("orbits1: ", orbits1)


# # data2 = isolate_one_quadrant(9,0.08,"top left")
# data2 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 9, x_value = 0.08)
# orbits2      = data2["orbits"]
# crossings2   = data2["crossings"]
# families_id2 = data2["families_str"]

# # print("orbits2: ", orbits2)



# merged_data = merge_datasets(data1, data2)
# merged_orbits      = merged_data["orbits"]
# merged_crossings   = merged_data["crossings"]
# merged_families_id = merged_data["families_str"]

# print("merged_crossings: ", merged_crossings)






# data_analytic = gather_analytic_resonant(max_p = 9, step_dx = 0.08)

# orbits_analytic      = data_analytic["orbits"]
# crossings_analytic   = data_analytic["crossings"]
# families_id_analytic = data_analytic["families_str"]

# # print("crossings_analytic: ", crossings_analytic)

# # # print(merged_crossings == crossings_analytic)
# # print(set(merged_crossings) & set(crossings_analytic))

# print("-----------------------------------------------------------------------------------------------------")
# print("-----------------------------------------------------------------------------------------------------")







def multiple_translate_to_better_data_structure(input_structure):
    if isinstance(input_structure, list):
        return tuple(input_structure)   # list -> tuple: unwrap
    elif isinstance(input_structure, tuple) and isinstance(input_structure[0], tuple):
        return list(input_structure)    # tuple of tuples -> list: wrap
    else:
        raise ValueError(f"Unexpected input type: {type(input_structure)}")







def single_isolate_one_quadrant(orbits, crossings, families_id, quadrant):
    """
    Runs gather_analytic_resonant to get all crossing points, but this notably includes points in two quadrants, which is not necessary and will confuse our polynomial interpolation algorithm later.
    As such, this function basically just isolates all of the crossing points that are in the desired quadrant (specified in parameter input "quadrant"), and discards the rest.
    (The revelevant comparison is done in the compare_to_point function, which checks if a given point (x,vx,vy) is in the desired quadrant or not.)
    
    Returns a data structure in the same format as the original data structure returned by gather_analytic_resonant, but with only the crossings in the desired quadrant.
    The orbits and families_id are unchanged from the original gather_analytic_resonant output, since we are only filtering the crossings, not the orbits.
    (Indeed, as the "orbits" list is just a list of the initial conditions of the orbits, we very simply ensure that this will be in the desired quadrant by only giving initial conditions in that quadrant.)
    
    This differs from isolate_one_quadrant in that it takes as input the orbits, crossings, and families_id data structures directly, rather than calling gather_analytic_resonant itself to get those data structures.
    This is useful for our implementation of multiple_isolate_one_quadrant, which was written concurently.
    
    Returns a result in our standard format:
        {
            "orbits":    [(x_i, vx_i, vy_i, label), ...],
            "crossings": [(x_c, vx_c, vy_c, label), ...],
            "families_str": "analytic_reso",
        }
    """
    
    # orbits_analytic      = orbits
    # crossings_analytic   = crossings
    
    

    # # # translated_orbits_analytic = translate_to_better_data_structure(orbits_analytic)
    # # # translated_crossings_analytic = translate_to_better_data_structure(crossings_analytic)    
    # # # ####print("FAMILIES ID ANALYTIC: ", families_id_analytic)
    # # # # No need to do the same for families_id_analytic, since it has a different structure (list of strings, not list of tuples).
    
    
    
    # translated_orbits_analytic = orbits
    # translated_crossings_analytic = crossings
    
    
    
    
    # def compare_to_point(x,vx,vy,label):  #including the vx and label parameters here just in case for some future use I need them, but for the foreseeable future I really only need to consider (x,vy) for the 2D case.
    #     if quadrant == "top left":
    #         return (x < 0) and (vy > 0)
    #     elif quadrant == "top right":
    #         return (x > 0) and (vy > 0)
    #     elif quadrant == "bottom left":
    #         return (x < 0) and (vy < 0)
    #     elif quadrant == "bottom right":
    #         return (x > 0) and (vy < 0)
    #     else:
    #         raise ValueError(f"Invalid quadrant: {quadrant}. Expected one of 'top left', 'top right', 'bottom left', 'bottom right'.")
    
    
    
    # number_of_crossings = len(translated_crossings_analytic[0]) #Note that translated_crossings_analytic[0] is the list of x values, and this has the same size as the lsit of vx values and the list of vy values.
    
    
    # new_crossings = []

    # new_xs = []
    # new_vxs = []
    # new_vys = []


    # #For each point, see if its in the quadrant that we want (specified in parameter input "quadrant"), and collect only those which are.
    # #-----------------------------------------------------------------------------------------------------
    # for i in range(number_of_crossings): 
        
    #     x = translated_crossings_analytic[0][i]
    #     vx = translated_crossings_analytic[1][i]
    #     vy = translated_crossings_analytic[2][i]
    #     label = translated_crossings_analytic[3]
        
        
        
    #     if compare_to_point(x,vx,vy,label):
    #         new_xs.append(x)
    #         new_vxs.append(vx)
    #         new_vys.append(vy)

    #     # new_crossings = [(np.array(new_xs), np.array(new_vxs), np.array(new_vys), label)]  # Repackage the new_crossings list to be in the same (horrible) format as the original crossings_analytic data structure, so that we can use it in the same plotting functions.
    

    #     new_crossings = (np.array(new_xs), np.array(new_vxs), np.array(new_vys), label)  # Repackage the new_crossings list to be in the same (horrible) format as the original crossings_analytic data structure, so that we can use it in the same plotting functions.

    
    # #-----------------------------------------------------------------------------------------------------
    
    
    
    
    # new_data = {
    #     "orbits":         orbits_analytic,
    #     "crossings":      new_crossings,
    #     "earth_crash_x0": np.array([]),   # none created here
    #     "earth_crash_vx0": np.array([]),
    #     "earth_crash_vy0": np.array([]),
    #     "moon_crash_x0":  np.array([]),
    #     "moon_crash_vx0": np.array([]),
    #     "moon_crash_vy0": np.array([]),
    #     "families_str":   families_id,
    # }
    
    
    # new_orbits_analytic = new_data["orbits"]
    # new_crossings_analytic = new_data["crossings"]
    # new_families_id_analytic = new_data["families_str"]
    
    

    # # plot_Poincare_2D(new_orbits_analytic, new_crossings_analytic, new_families_id_analytic, 
    # #                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    # #                 plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, print_legend=False)
    
    
    
    

    # # print(new_orbits_analytic)
    # # print("-----------------------------------------------------------------------------------------------------")
    # # print(new_crossings_analytic)
    
    # return {
    #     "orbits":         new_orbits_analytic,
    #     "crossings":      new_crossings_analytic,
    #     "families_str":   new_families_id_analytic
    # }
    
    
    
    
    
    def compare_to_point(x,vx,vy,label):  #including the vx and label parameters here just in case for some future use I need them, but for the foreseeable future I really only need to consider (x,vy) for the 2D case.
        if quadrant == "top left":
            return (x < 0) and (vy > 0)
        elif quadrant == "top right":
            return (x > 0) and (vy > 0)
        elif quadrant == "bottom left":
            return (x < 0) and (vy < 0)
        elif quadrant == "bottom right":
            return (x > 0) and (vy < 0)
        else:
            raise ValueError(f"Invalid quadrant: {quadrant}. Expected one of 'top left', 'top right', 'bottom left', 'bottom right'.")
    
    
    
    number_of_crossings = len(crossings[0]) #Note that translated_crossings_analytic[0] is the list of x values, and this has the same size as the lsit of vx values and the list of vy values.
    
    
    new_crossings = []

    new_xs = []
    new_vxs = []
    new_vys = []


    #For each point, see if its in the quadrant that we want (specified in parameter input "quadrant"), and collect only those which are.
    #-----------------------------------------------------------------------------------------------------
    for i in range(number_of_crossings): 
        
        x = crossings[0][i]
        vx = crossings[1][i]
        vy = crossings[2][i]
        label = crossings[3]
        
        
        
        if compare_to_point(x,vx,vy,label):
            new_xs.append(x)
            new_vxs.append(vx)
            new_vys.append(vy)

        # new_crossings = [(np.array(new_xs), np.array(new_vxs), np.array(new_vys), label)]  # Repackage the new_crossings list to be in the same (horrible) format as the original crossings_analytic data structure, so that we can use it in the same plotting functions.
    

        new_crossings = (np.array(new_xs), np.array(new_vxs), np.array(new_vys), label)  # Repackage the new_crossings list to be in the same (horrible) format as the original crossings_analytic data structure, so that we can use it in the same plotting functions.

    
    #-----------------------------------------------------------------------------------------------------
    
    
    
    
    new_data = {
        "orbits":         orbits,
        "crossings":      new_crossings,
        "earth_crash_x0": np.array([]),   # none created here
        "earth_crash_vx0": np.array([]),
        "earth_crash_vy0": np.array([]),
        "moon_crash_x0":  np.array([]),
        "moon_crash_vx0": np.array([]),
        "moon_crash_vy0": np.array([]),
        "families_str":   families_id,
    }
    
    
    new_orbits = new_data["orbits"]
    new_crossings = new_data["crossings"]
    new_families_id = new_data["families_str"]
    
    

    # plot_Poincare_2D(new_orbits_analytic, new_crossings_analytic, new_families_id_analytic, 
    #                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    #                 plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, print_legend=False)
    
    
    
    

    # print(new_orbits_analytic)
    # print("-----------------------------------------------------------------------------------------------------")
    # print(new_crossings_analytic)
    
    return {
        "orbits":         new_orbits,
        "crossings":      new_crossings,
        "families_str":   new_families_id
    }
    
  
def multiple_isolate_one_quadrant(p_arr = [8, 9], x_val_arr = [0.08, 0.08], quadrant = "top left"):
    """
    Isolates the crossings in the specified quadrant for multiple datasets (corresponding to different values of p and x_value), and then merges all of these isolated datasets together into one big dataset that we can use 'off-the-shelf'.
    It does so by calling single_isolate_one_quadrant for each dataset, and then merging the results together using merge_datasets.
    
    Returns a result in our standard format:
        {
            "orbits":    [(x_i, vx_i, vy_i, label), ...],
            "crossings": [(x_c, vx_c, vy_c, label), ...],
            "families_str": "analytic_reso",
        }
    """
    
    # temp_data_list = []
    
    ## Because of the way that merge_datasets works, we need the first dataset to be in the normal format, rather than empty.
    temp_data_list = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p_arr[0], x_value = x_val_arr[0])   

    ## We start the loop from 1 instead of 0 because of this.
    for i in range(1, len(p_arr)): 
        p = p_arr[i]
        x_val = x_val_arr[i]
        
        data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = p, x_value = x_val)
        temp_data_list = merge_datasets(temp_data_list, data_analytic)  # Merge the new data with the existing data in temp_data_list. This will accumulate all of the data from each iteration of the loop.

    orbits = temp_data_list["orbits"]
    crossings = temp_data_list["crossings"]
    families_id = temp_data_list["families_str"]
    
    # print("orbits: ", orbits)
    # print("crossings: ", crossings)
    # # print("families_id: ", families_id)
    

    
    
    # translated_orbits = multiple_translate_to_better_data_structure(orbits) # This is a list with all of our orbits now
    # translated_crossings = multiple_translate_to_better_data_structure(crossings) # This is a list with all of our crossings now

    

    
    temp_individual_orbits = []
    temp_individual_crossings = []
    
    
    
   
    for i in range(len(orbits)):    #note that len(orbits) = len(crossings)
        isolated_data = single_isolate_one_quadrant(orbits[i], crossings[i], families_id, quadrant)  # Pass it to the reduced, individual problem
        individual_orbits = isolated_data["orbits"]
        individual_crossings = isolated_data["crossings"]
        temp_individual_orbits.append(individual_orbits)
        temp_individual_crossings.append(individual_crossings)

    # print("temp_individual_orbits: ", temp_individual_orbits)
    # print("temp_individual_crossings: ", temp_individual_crossings)
        
        
        
        
    # print("orbits 0: ", orbits[0])
    # print("crossings 0: ", crossings[0])
        
        
    # # print("orbits 1: ", orbits[1])
    # # print("crossings 1: ", crossings[1])
    # # # print("families_id 1: ", families_id)
    
    
    # i=0
    # isolated_data = single_isolate_one_quadrant(orbits[i], crossings[i], families_id[i], quadrant)  # Pass it to the reduced, individual problem
    # isolated_orbits = isolated_data["orbits"]
    # isolated_crossings = isolated_data["crossings"]
    # # print("isolated_orbits: ", isolated_orbits)
    # print("isolated_crossings: ", isolated_crossings)
    
    
    
    
    # data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = max_p, x_value = x_value)
    
    
    # orbits_analytic      = data_analytic["orbits"]
    # crossings_analytic   = data_analytic["crossings"]
    # families_id_analytic = data_analytic["families_str"]
    
    

    # translated_orbits_analytic = translate_to_better_data_structure(orbits_analytic)
    # translated_crossings_analytic = translate_to_better_data_structure(crossings_analytic)    
    # ####print("FAMILIES ID ANALYTIC: ", families_id_analytic)
    # # No need to do the same for families_id_analytic, since it has a different structure (list of strings, not list of tuples).
    
      
    # # print("translated_crossings_analytic: ", translated_crossings_analytic)
    
    
    # def compare_to_point(x,vx,vy,label):  #including the vx and label parameters here just in case for some future use I need them, but for the foreseeable future I really only need to consider (x,vy) for the 2D case.
    #     if quadrant == "top left":
    #         return (x < 0) and (vy > 0)
    #     elif quadrant == "top right":
    #         return (x > 0) and (vy > 0)
    #     elif quadrant == "bottom left":
    #         return (x < 0) and (vy < 0)
    #     elif quadrant == "bottom right":
    #         return (x > 0) and (vy < 0)
    #     else:
    #         raise ValueError(f"Invalid quadrant: {quadrant}. Expected one of 'top left', 'top right', 'bottom left', 'bottom right'.")
    
    
    
    # number_of_crossings = len(translated_crossings_analytic[0]) #Note that translated_crossings_analytic[0] is the list of x values, and this has the same size as the lsit of vx values and the list of vy values.
    
    
    # new_crossings = []

    # new_xs = []
    # new_vxs = []
    # new_vys = []


    # #For each point, see if its in the quadrant that we want (specified in parameter input "quadrant"), and collect only those which are.
    # #-----------------------------------------------------------------------------------------------------
    # for i in range(number_of_crossings): 
        
    #     x = translated_crossings_analytic[0][i]
    #     vx = translated_crossings_analytic[1][i]
    #     vy = translated_crossings_analytic[2][i]
    #     label = translated_crossings_analytic[3]
        
        
    #     # new_point = (x, vx, vy, label)
        
    #     # if compare_to_point(x,vx,vy,label):
    #     #     new_crossings.append(new_point)
        
    #     if compare_to_point(x,vx,vy,label):
    #         new_xs.append(x)
    #         new_vxs.append(vx)
    #         new_vys.append(vy)

    #     ##new_crossings = list(zip(new_xs, new_vxs, new_vys, [label]*len(new_xs)))  # Repackage the new_crossings list to be in the same format as the original crossings_analytic data structure, so that we can use it in the same plotting functions.
    #     # new_crossings = [list(np.array(new_xs)), list(np.array(new_vxs)), list(np.array(new_vys)), label]  # Repackage the new_crossings list to be in the same format as the original crossings_analytic data structure, so that we can use it in the same plotting functions.
    #     new_crossings = [(np.array(new_xs), np.array(new_vxs), np.array(new_vys), label)]  # Repackage the new_crossings list to be in the same (horrible) format as the original crossings_analytic data structure, so that we can use it in the same plotting functions.

    #     # translated_new_crossings = translate_to_better_data_structure(new_crossings)    # Repackage to the [()] data structure to use in plotting. ####THIS WASNT WORKING SO I DID THAT^
    # #-----------------------------------------------------------------------------------------------------
    
    
    
    
    # new_data = {
    #     "orbits":         orbits_analytic,
    #     "crossings":      new_crossings,
    #     "earth_crash_x0": np.array([]),   # none created here
    #     "earth_crash_vx0": np.array([]),
    #     "earth_crash_vy0": np.array([]),
    #     "moon_crash_x0":  np.array([]),
    #     "moon_crash_vx0": np.array([]),
    #     "moon_crash_vy0": np.array([]),
    #     "families_str":   "analytic_reso",
    # }
    
    
    
    # new_orbits_analytic = new_data["orbits"]
    # new_crossings_analytic = new_data["crossings"]
    # new_families_id_analytic = new_data["families_str"]
    
    
    
    
    

    return {
        "orbits":         temp_individual_orbits,
        "crossings":      temp_individual_crossings,
        "families_str":   "analytic_reso"
    }
    
    
    

def single_get_list_of_points(orbits, crossings, families_id):
    """
    Applies isolate_one_quadrant to get the crossings in the specified quadrant, and then extracts the (x, vy) points from those crossings and saves them out as a list of tuples.
    The result is a list of tuples of the form [(x1, vy1), (x2, vy2), ...], which are the (x, vy) coordinates of the crossings that lie in the specified quadrant.
    The function also plots these points on a scatter plot for visualization if desired (i.e.: if plot_points = True).
    # """
    

    # orbits_analytic = orbits
    # crossings_analytic = crossings
    # families_id_analytic = families_id

    # # translated_crossings_analytic = translate_to_better_data_structure(crossings_analytic)
    
    # translated_crossings_analytic = crossings_analytic

    # xs = translated_crossings_analytic[0]
    # vys = translated_crossings_analytic[2]
    # # x_vy_points = sorted(zip(xs, vys), key=lambda point: point[0])  # While saving the points to this list, make sure to sort them by x value. This will be important later when we do polynomial interpolation.
    # x_vy_points = zip(xs, vys)
        
    # return x_vy_points
    

    xs = crossings[0]
    vys = crossings[2]
    # x_vy_points = sorted(zip(xs, vys), key=lambda point: point[0])  # While saving the points to this list, make sure to sort them by x value. This will be important later when we do polynomial interpolation.
    x_vy_points = zip(xs, vys)
        
    return x_vy_points
   

def multiple_get_list_of_points(p_arr = [8, 9], x_val_arr = [0.08, 0.08], quadrant = "top left"):
    """
    Applies multiple_isolate_one_quadrant to get the crossings in the specified quadrant, and then extracts the (x, vy) points from those crossings and saves them out as a list of tuples.
    
    The result is a list of tuples of the form 
        [(x1, vy1), (x2, vy2), ...]
    , which are the (x, vy) coordinates of the crossings that lie in the specified quadrant.
    
    The function also plots these points on a scatter plot for visualization if desired (i.e.: if plot_points = True).
    """
    

    data = multiple_isolate_one_quadrant(p_arr = p_arr, x_val_arr = x_val_arr, quadrant = quadrant)

    orbits_analytic      = data["orbits"]
    crossings_analytic   = data["crossings"]
    families_id_analytic = data["families_str"]

    x_vy_points = []


    for i in range(len(crossings_analytic)): # for each crossing set
        temp_data = single_get_list_of_points(orbits_analytic[i], crossings_analytic[i], families_id_analytic) # get the list of points for that crossing set, and plot them if desired. Note that this will also print out the (x, vy) coordinates of each point in the console, which can be useful for debugging and verification purposes.
        for point in temp_data:
            x_vy_points.append(point) # add the points from this crossing set to the overall list of points.
            
    # print("x_vy_points: ", x_vy_points)

    sorted_x_vy_points = sorted(x_vy_points, key=lambda p: p[0])

    return sorted_x_vy_points

    # translated_crossings_analytic = translate_to_better_data_structure(crossings_analytic)

    # # print("translated_crossings_analytic: ", translated_crossings_analytic)
    
    
    # # number_of_crossings = len(translated_crossings_analytic[0]) #Note that translated_crossings_analytic[0] is the list of x values, and this has the same size as the list of vx values and the list of vy values.
    # # for i in range(number_of_crossings):
    # #     x = translated_crossings_analytic[0][i]
    # #     # vx = translated_crossings_analytic[1][i]
    # #     vy = translated_crossings_analytic[2][i]
    # #     # label = translated_crossings_analytic[3]
        

    # xs = translated_crossings_analytic[0]
    # vys = translated_crossings_analytic[2]
    # # x_vy_points = list(zip(xs, vys))
    # x_vy_points = sorted(zip(xs, vys), key=lambda point: point[0])  # While saving the points to this list, make sure to sort them by x value. This will be important later when we do polynomial interpolation.
   
    # # for i in range(number_of_crossings):
    # #     x = translated_crossings_analytic[0][i]
    # #     # vx = translated_crossings_analytic[1][i]
    # #     vy = translated_crossings_analytic[2][i]
    # #     # label = translated_crossings_analytic[3]
    
    
    
    
    # # orbits_analytic      = data["orbits"]
    # # crossings_analytic   = data["crossings"]
    # # families_id_analytic = data["families_str"]
        
        
        
    
    
    # # print(x_vy_points)
        
        
        
        
        
    # if plot_points == True:
    #     xs_plot, vys_plot = zip(*x_vy_points)

    #     plt.scatter(xs_plot, vys_plot, s=10)
    #     plt.xlabel('x')
    #     plt.ylabel('vy')
    #     plt.title('vy vs x')
    #     plt.grid(True)
    #     plt.tight_layout()
    #     plt.show()
        
    #     ##To see a line plot instead of a scatter plot, uncomment this:
    #     # plt.figure(figsize=(8, 5))
    #     # plt.plot(xs_plot, vys_plot)
    #     # plt.xlabel('x')
    #     # plt.ylabel('vy')
    #     # plt.title('vy vs x')
    #     # plt.grid(True)
    #     # plt.tight_layout()
    #     # plt.show()
    

    # #To do multiple at once, comment out this bit, and uncomment the bit labelled "AAAAAAAA UNCOMMENT ME IF YOU WANT MULTIPLE"
    # # -----------------------------------------------------------------------------------------------------")
    # fig = plt.figure(figsize=(12,8))
    # ax = fig.add_subplot(111)

    # ax.set_xlim(-0.5, 0)
    # ax.set_ylim(-0.1, 6)
    # # -----------------------------------------------------------------------------------------------------")
    
    
    # plot_Poincare_2D_without_printing(ax, orbits_analytic, crossings_analytic, families_id_analytic,
    #                                   earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0,
    #                                   plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, print_legend=False, show_accessible_region=True)
    
    
    # # # plt.show()

    
    # return x_vy_points, fig, ax
    












def test_multiple_isolate_one_quadrant(p_arr=[8,9], x_val_arr=[0.08, 0.08], quadrant="top left"):

    data = multiple_isolate_one_quadrant(p_arr=p_arr, x_val_arr=x_val_arr, quadrant=quadrant)
    orbits = data["orbits"]
    crossings = data["crossings"]
    families_id = data["families_str"]




    new_data = {
        "orbits":         orbits,
        "crossings":      crossings,
        "earth_crash_x0": np.array([]),   # none created here
        "earth_crash_vx0": np.array([]),
        "earth_crash_vy0": np.array([]),
        "moon_crash_x0":  np.array([]),
        "moon_crash_vx0": np.array([]),
        "moon_crash_vy0": np.array([]),
        "families_str":   families_id,
    }


    new_orbits_analytic = new_data["orbits"]
    new_crossings_analytic = new_data["crossings"]
    new_families_id_analytic = new_data["families_str"]


    orbits      = new_data["orbits"]
    crossings   = new_data["crossings"]
    families_id = new_data["families_str"]
    earth_crash_x0 = new_data["earth_crash_x0"]
    earth_crash_vx0 = new_data["earth_crash_vx0"]
    earth_crash_vy0 = new_data["earth_crash_vy0"]
    moon_crash_x0  = new_data["moon_crash_x0"]
    moon_crash_vx0  = new_data["moon_crash_vx0"]
    moon_crash_vy0  = new_data["moon_crash_vy0"]


    # plot_Poincare_2D(new_orbits_analytic, new_crossings_analytic, new_families_id_analytic, 
    #                 earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
    #                 plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, print_legend=False)

    
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)


    plot_Poincare_2D_without_printing(ax, new_orbits_analytic, new_crossings_analytic, new_families_id_analytic, 
                    earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
                    plot_second_crossings = True, which="vy",show_only_lower_quadrant=False, show_accessible_region=True,print_legend=False)
    
    plt.show()


def test_multiple_get_list_of_points(p_arr=[8,9], x_val_arr=[0.08, 0.08], quadrant="top left"):
    points = multiple_get_list_of_points(p_arr, x_val_arr, quadrant)
    print("points: ", points)



# test_multiple_get_list_of_points(p_arr=[8,9], x_val_arr=[0.08, 0.08], quadrant="top left")


# test_multiple_isolate_one_quadrant(p_arr=[8,9,10], x_val_arr=[0.08, 0.08, 0.08], quadrant="top left")


# specific_p_arr=[8,9,10,11,12,13,14,15,16,17,18]
# specific_x_val_arr = []
# for p in specific_p_arr:
#     specific_x_val_arr.append(0.01)  # This is the x_value that we will use for each value of p in p_arr. We can change this if we want to use a different x_value for each p, but for now we will just use the same x_value for all of them.

# test_multiple_isolate_one_quadrant(p_arr=specific_p_arr, x_val_arr=specific_x_val_arr, quadrant="top left")







# earth_crash_x0 = np.array([])
# earth_crash_vx0 = np.array([])
# earth_crash_vy0 = np.array([])
# moon_crash_x0  = np.array([])
# moon_crash_vx0  = np.array([])
# moon_crash_vy0  = np.array([])


# ###Change max_p to get more orbits (up to max_p : 1), change step_dx to get higher resolution (but beware of long runtimes for small step_dx)
# data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, step_dx = 0.1)

# orbits     = data_analytic["orbits"]
# crossings  = data_analytic["crossings"]
# families_id = data_analytic["families_str"]


# plot_Poincare_2D(orbits, crossings, families_id, 
#                  earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
#                  plot_second_crossings = True, which="vy")



# data_analytic = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 10, step_dx = 0.08, x_value = 0.08)

# orbits     = data_analytic["orbits"]
# crossings  = data_analytic["crossings"]
# families_id = data_analytic["families_str"]

# print("orbits: ", orbits)

# plot_Poincare_2D(orbits, crossings, families_id, 
#                  earth_crash_x0, earth_crash_vx0, earth_crash_vy0, moon_crash_x0, moon_crash_vx0, moon_crash_vy0, 
#                  plot_second_crossings = True, which="vy")