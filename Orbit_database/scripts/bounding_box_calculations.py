from support.orbit_data import gather_analytic_resonant_with_specified_p_and_x_value, gather_dataset, gather_analytic_resonant, merge_datasets, merge_lists
from support.plot import plot_given_boxes, plot_Poincare_2D_with_boxes, plot_Poincare_2D_with_balls, plot_Poincare_2D, plot_Poincare_3D, plot_Poincare_analytic, plot_cross_section_x_vy, plot_cross_section_x_vy_individual
from support.rectangle_calculations import Rect_Poincare_2D_get_boxes, calculate_mega_box, define_region
from support.constants import cr3bp, mu1, mu2, R_earth, R_moon, earth_collision_radius, E0, jacobimin, L2_info, L1_info, U_tilde, BASE_PATH  # type: ignore
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from scipy.optimize import brentq, fsolve






# x = np.linspace(-1.5, 1.5, 64000)
# line_width = 1




x_1 = np.linspace(-0.5, 0.5, 64000)
x_2 = np.linspace(-1.5, -0.5, 30000)
x_3 = np.linspace(0.5, 1.5, 30000)
# x_4 = np.linspace(-1.9, -1.5, 10000)
# x_5 = np.linspace(1.5, 1.9, 10000)
# x = np.concatenate((x_2, x_1, x_3, x_4, x_5))
x = np.concatenate((x_2, x_1, x_3))

# x_1 = np.linspace(-0.4, 0.4, 64000)
# x_2 = np.linspace(-0.447, -0.4, 60000)
# x_3 = np.linspace(0.4, -0.447, 60000)
# x_4 = np.linspace(-0.447, -1.5, 30000)
# x_5 = np.linspace(-0.447, 1.5, 30000)
# x = np.concatenate((x_2, x_1, x_3, x_4, x_5))


line_width = 1




def U_0(x):
    return -0.5*(x**2) - mu1/np.sqrt((x + mu2)**2) - mu2/np.sqrt((x - mu1)**2) - 0.5*mu1*mu2


def const_energy_curve(k,x):
        return np.sqrt(np.maximum(0, 2*(k*E0 - U_0(x))))
        # return np.maximum(0, 2*(k*E0 - U_0(x)))
    

    
    





class BoundingBox: ######NOTE TO SELF: I SHOULD REALLY MAKE THE "left_curve" AND "right_curve" GLOBAL CLASS FUNCTIONS, RATHER THAN CALCULATING THEM EACH TIME IN EACH METHOD. THIS MIGHT (?) SPEED THINGS UP A LITTLE BIT (PROBABLY NOT BY TOO MUCH THOUGH).
    

    def __init__(self, min_energy, max_energy, min_height, max_height):
        
        if min_height > max_height:
            raise ValueError("min_height cannot be greater than max_height.")
        elif min_energy > max_energy:
            raise ValueError("min_energy cannot be greater than max_energy.")
        
        
        self.min_energy = min_energy  
        self.max_energy = max_energy
        self.min_height = min_height
        self.max_height = max_height
        
        
    
    def get_min_energy(self):
        return self.min_energy
    
    def get_max_energy(self):
        return self.max_energy
    
    def get_min_height(self):
        return self.min_height
    
    def get_max_height(self):
        return self.max_height
    
    
    # def get_bounding_curves(self):
    #     """
    #     Returns the energy curves that bound the box horizontally, and the horizontal lines that bound the box vertically.
    #     """
        
    #     return const_energy_curve(self.max_energy,x), const_energy_curve(self.min_energy,x), self.min_height, self.max_height
    
    
    def contains_point(self, x0, y0):
        """
        Checks if a given point is in this box.
                
        Parameters
        ----------
        x0: float
            The x-coordinate of the point to check.
        y0: float
            The y-coordinate of the point to check.
        
        Returns
        -------
        bool
            True if the point is in the box, False otherwise.
        """  
        
        
        # Boundary curves
        left_curve = np.sqrt(np.maximum(0, const_energy_curve(self.max_energy,x0)))
        right_curve = np.sqrt(np.maximum(0, const_energy_curve(self.min_energy,x0)))
        
        
        
        # Given a point (x0, y0), we wish to determine if it lies within the bounding box.
        # The vertical requirements are easy to check. Just compare the y component of $p$ to the vertical bounds min_height and max_height. That is to say, just check the following
        
        if (self.min_height > y0) or (self.max_height < y0):
            return False
        
        
        
        
        
        ####OLD BAD METHOD FOR CHECKING THE HORIZONTAL BOUNDS:
        #----------------------------------------------------------------------
        # def find_x_given_energy_and_y_value(k,y_0): ###THIS USED TO BE OUTSIDE OF THE CLASS ENTIRELY, IN CASE SOMETHING BREAKS, THAT IS WHY.
        #     ###If we are looking at the left side of the plot:
        #     return brentq(lambda x: const_energy_curve(k, x) - y_0, -1, 0)

        #     ######THERE MIGHT BE PROBLEMS WITH THIS CASE ACTUALLY, NEED TO LOOK DEEPER INTO THIS:
        #     # ###If we are looking at the right side of the plot:
        #     # return brentq(lambda x: const_energy_curve(k, x) - y_0, 0, 1)
        
        
        
        
        # # The horizontal bounds are more nuanced. It is not as easy as seeing if f_1(p.x) < p.x < f_2(p.x), since f_i might require a different $x \neq p.x$ in order to achieve the same height.
        # # Since the general form of our curves of constant energy, and especially the component term $U(x,0)$, are not easily invertible, I have implemented scipy.brentq in order to find the respective $x_i$ such that $f_i(x_i) = p.y$.
        # # (Notably, I am concluding this somewhat naïvely, so maybe there is a clever mathematical argument that lets me do this)
        # # I have set the bounds in which scipy.brentq checks for solutions to be limited to $(-1, 0)$ (This is at least true for the case for negative x, though I will have to edit this later for positive x), since the accessible region on the left seems to be bounded by $x=-1$.
        
        # min_energy_x = find_x_given_energy_and_y_value(self.min_energy, y0)
        # max_energy_x = find_x_given_energy_and_y_value(self.max_energy, y0)
        
        # # print("min_energy_x", min_energy_x)
        # # print("max_energy_x", max_energy_x)
        
        
        # ####NOTE TO SELF: MIGHT WANT TO CHECK IF THIS WORKS PROPERLY IN THE CASE OF POSITIVE X VALUES AS WELL. MIGHT REQUIRE ADJUSTMENTS TO THE find_x_given_energy_and_y_value FUNCTION
        # if ( (x0 <= 0) and (min_energy_x <= x0 <= max_energy_x) ) or ( (x0 >= 0) and (min_energy_x >= x0 >= max_energy_x) ):
        #     return True
        
        # return False
        #----------------------------------------------------------------------
    


        ###NEW BETTER METHOD FOR CHECKING THE HORIZONTAL BOUNDS:
        #----------------------------------------------------------------------
        # Rearranging/isolating the equation of y0 = const_energy_curve(k*E0, x0) for k*E0, we get
        
        k = ( ((y0)**2)/2 + U_0(x0) ) / E0
        
        if (self.min_energy <= k <= self.max_energy): # If this k value (recall our energies are of the form k*E0), is between the min and max energy of the box, then we know that the point is between the left and right curves of the box
            return True
        
        return False # Otherwise, since we have already checked the vertical bounds, return False.
        
        #----------------------------------------------------------------------
        #####THIS^ IS GOOD, BUT I'VE GOT TO ADD A WAYH TO DISTINGUISH WHETHER I AM IN THE LEFT OR RIGHT SIDE OF THE v_y AXIS, (AND POSSIBLY ALSO THE CASES LEFT AND RIGHT OF THE MOON TOO, IF I WANT TO INLCUDE THAT TOO)

    
    
    
    
    
    
    
    
        
        
    
    def shade_box(self, plot_bounding_curves=False):
        """
        Visually plots the box.
                
        Parameters
        ----------
        plot_bounding_curves: bool
            Plots the curves bounding the box as well. Known issue is that if if this function is called on neighbouring boxes, these shared curves will be plotted again, massively impacting performace time. For now, just set this to False if you are plotting a lot of boxes.
        """    
        
        # y_left = np.sqrt(np.maximum(0, const_energy_curve(self.max_energy,x)))
        # y_right = np.sqrt(np.maximum(0, const_energy_curve(self.min_energy,x)))
        
        y_left = np.maximum(0, const_energy_curve(self.max_energy,x))
        y_right = np.maximum(0, const_energy_curve(self.min_energy,x))
        
        
        y_min_fill = np.maximum(self.min_height, y_left)
        y_max_fill = np.minimum(self.max_height, y_right)
        
        valid = y_max_fill > y_min_fill
        y_min_plot = np.where(valid, y_min_fill, np.nan)
        y_max_plot = np.where(valid, y_max_fill, np.nan)


        plt.fill_between(x, y_min_plot, y_max_plot, alpha=0.5, color='skyblue')
        
        if plot_bounding_curves:
            self.plot_bounding_curves()
        
        
        
    def plot_bounding_curves(self):
        """
        Plots the bounding curves of the specific box, without shading the interior.
        """
        
        # y_left = np.sqrt(np.maximum(0, const_energy_curve(self.max_energy,x)))
        # y_right = np.sqrt(np.maximum(0, const_energy_curve(self.min_energy,x)))
        
        y_left = np.maximum(0, const_energy_curve(self.max_energy,x))
        y_right = np.maximum(0, const_energy_curve(self.min_energy,x))
        
        # Plot the curves of contstant energy, bounding the box on the left and right
        plt.plot(x, y_left, 'm', label={f"{self.min_energy:.1f}"}, lw=line_width)
        plt.plot(x, y_right, 'm', label={f"{self.max_energy:.1f}"}, lw=line_width)
        
        # Plot the horizontal bounding lines (the lines of constant height)
        # plt.axhline(self.min_height, color='tab:orange', linestyle='--', lw=line_width)
        # plt.axhline(self.max_height, color='tab:orange', linestyle='--', lw=line_width)
        plt.axhline(self.min_height, color='tab:orange', linestyle='--', lw=0.7)
        plt.axhline(self.max_height, color='tab:orange', linestyle='--', lw=0.7)
    
    
    
    @staticmethod
    def plot_all_bounding_curves(h1, energy_min, energy_max, h2, y_min, y_max, line_width=0.3):
        """
        Plots the bounding curves of every box that would be generated by the given parameters via the generate_all_boxes function. Note that this should really be called automatically everytime you call the plot_boxes function, or anything like that. But because it should only be called once, and as it requires all of the information of h1, energy_min, energy_max, h2, y_min, y_max, and this is kind of messy to store in each box object locally, I guess for know we'll just call it everytime we plot the boxes whenever we actually generate the plot itself using plot.show.
        """
        
        energy_vals = np.linspace(energy_min, energy_max, round((energy_max - energy_min) / h1) + 1)
        
        y_heights = np.linspace(y_min, y_max, round((y_max - y_min) / h2) + 1)
        
        
        for energy in energy_vals:
            y_vals = np.maximum(0, const_energy_curve(energy,x))
            
            for i in range(len(y_vals)):
                if y_vals[i] == 0:
                    y_vals[i] = np.nan
            
            # plt.plot(x, y_vals, 'm--', label={f"{energy:.1f}"}, lw=line_width, dashes=(10, 3))
            # plt.plot(x, -y_vals, 'm--', label={f"{energy:.1f}"}, lw=line_width, dashes=(10, 3))
            
            plt.plot(x, y_vals, 'm--', lw=line_width, dashes=(10, 3))
            # plt.plot(x, -y_vals, 'm--', lw=line_width, dashes=(10, 3))
        
        plt.axhline(0, color='black', linestyle='-', lw=1)
            
    
    
        # X = range(0)
        # Y = range(0)
        # plt.plot(X, Y, 'm--', label='Energy Curves', lw=line_width, dashes=(10, 3))  
        
        
    
            
        for height in y_heights:
            plt.axhline(height, color='tab:orange', linestyle='--', lw=line_width)
            # if height != 0:
            #     plt.axhline(-height, color='tab:orange', linestyle='--', lw=line_width)



    
    @staticmethod
    def plot_accessible_region(h1, energy_min, energy_max, h2, y_min, y_max):

        y_pos = np.maximum(0, const_energy_curve(energy_min, x)).astype(float)
        y_neg = -np.maximum(0, const_energy_curve(energy_min, x)).astype(float)

        y_pos[y_pos == 0] = np.nan
        y_neg[y_neg == 0] = np.nan

        
        # plt.fill_between(x, y_neg, y_pos, alpha=0.1, color='#FFFFFF') ###I JUST CHANGED THE COLOUR TO WHITE. THE WHOLE THING IS FUNCITONAL, JUST CHANGE THE COLOUR TO SOMETHING NONWHITE IF YOU WANT TO SEE IT
        
        
        y_vals = np.maximum(0, const_energy_curve(energy_min,x))
            
        for i in range(len(y_vals)):
            if y_vals[i] == 0:
                y_vals[i] = np.nan
        
        # plt.plot(x, y_vals, color='black', label={f"{energy_min:.1f}"}, lw=line_width)
        # plt.plot(x, -y_vals, color='black', label={f"{energy_min:.1f}"}, lw=line_width)
        
        plt.plot(x, y_vals, color='black', lw=line_width)
        plt.plot(x, -y_vals, color='black', lw=line_width)
        
        # X = range(0)
        # Y = range(0)
        # plt.plot(X, Y, '-', color='black', label='Accessible Region Boundary', lw=line_width)  

        

    
    
    
    
    

def generate_all_boxes(h1, energy_min, energy_max, h2, y_min=0, y_max=6, chequerboard = 0):
    """
   Returns a 2D list with all of the generated boxes for the given discretisation parameters.

    Parameters
    ----------
    h1 : float
        The distance between energy values.
    energy_min : float
        The minimum energy (i.e.: the inner-most constant energy curve).
    energy_max: float
        The maximum energy (i.e.: the outer-most constant energy curve).
    h2 : float
        The distance between height values.
    y_min : float
        The minimum height. PROBABLY THIS SHOULD JUST BE -y_max ACTUALLY.
    y_max: float
        The maximum height. Arbitrarily defaults to 6 for now.
    chequerboard: int
        Allows you to only generate a chequerboard pattern of the boxes. This is probably never going to be relevant nor useful for you.
        
        
    Returns
    -------
    2D list
        Returns a 2D list of the generated boxes. The first index corresponds to energy, and the second index corresponds to height.
    """
    
    energy_vals = np.linspace(energy_min, energy_max, round((energy_max - energy_min) / h1) + 1)
    
    

    # y_min = -y_max
    

    y_heights = np.linspace(y_min, y_max, round((y_max - y_min) / h2) + 1)
    
    box_arr = []
    
    for j in range(len(energy_vals)-1):
        
        box_arr_j = []
        
        for i in range(len(y_heights)-1):
            # If we dont want a chequered pattern, then always do this. If we do want a chequered pattern, then only do this every other time:
            if (chequerboard == 1 and i % 2 == 0) or (chequerboard == 2 and i % 2 == 1) or (chequerboard == 0):
                
                box_arr_j.append(BoundingBox(energy_vals[j],energy_vals[j+1],y_heights[i],y_heights[i+1]))
       
        box_arr.append(box_arr_j)
        
    return box_arr
    
    

def plot_boxes(input_arr, plot_bounding_curves=False):
    
    
    input_arr = np.array(input_arr)
    
    # print("DIMENSION:  -----------", input_arr.ndim)
    
    
    if input_arr.ndim == 2:
        
        if len(input_arr) == 0:
            raise Exception("Outer layer of input list is empty.")
        elif len(input_arr[0]) == 0:
            raise Exception("Inner layer of input list is empty.")
        
        
        for j in range(len(input_arr)):
                for i in range(len(input_arr[0])):
                    input_arr[j][i].shade_box(plot_bounding_curves)
    
    
    # print(input_arr)
    
    if input_arr.ndim == 1:
        
        if len(input_arr) == 0:
            raise Exception("Input list is empty.")
        
        for i in range(len(input_arr)):
            input_arr[i].shade_box(plot_bounding_curves)
    



def plot_points_in_boxes(point_arr, boxes_arr, colour='ro'):
    """
    Plots the given points, and visually indicates which of the given boxes they are in (by shading the box and plotting the point in red).
            
    Parameters
    ----------
    point_arr: list of tuples
        A list of (x, y) coordinates of points to check.
    boxes_arr: list of lists
        A 2D list of BoundingBox objects.

    Returns
    -------
    None
    
    """
    
    # fig = plt.figure(figsize=(12,8))
    # ax = fig.add_subplot(111)

    # ax.set_xlim(-0.5, 0)
    # ax.set_ylim(-0.1, 6)
    # line_width = 1

    # boxes_arr = generate_all_boxes(h1=1, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6)

    
    # # test_points_arr = [(-0.5, 0.2), (-0.5, 0.3), (-0.5, 0.4), (-0.6, 0.4), (-0.6, 0.2), (-0.6, 0), (1, 0.2), (0.5, 0.2), (-0.43, 0.2), (-0.41, 0.299)]
    # test_points_arr = [(-0.4, 0.15), (-0.3, 0.5), (-0.2, 2), (-0.15,3), (-0.059, 4.917), (-0.15, 0.1), (-0.45, 1.1)]
    
    for point in point_arr:
        for j in range(len(boxes_arr)):
            for i in range(len(boxes_arr[0])):
                if boxes_arr[j][i].contains_point(point[0], point[1]):
                    plt.plot(point[0], point[1], colour)  # Plot the point in the specified colour if it's in the box
                    # boxes_arr[j][i].plot_bounding_curves()
                    boxes_arr[j][i].shade_box()
                    break  # No need to check other boxes once we find one that contains the point
    
    # plot_boxes(boxes_arr)

    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.legend()
    # plt.show()





def plot_crossings_in_boxes(crossings_arr, boxes_arr, colour='ro'):
    """
    This just calls plot_points_in_boxes, but it is specifically implemented for the format of the crossings dataset generated bythe function gather_analytic_resonant_with_specified_p_and_x_value in orbit_data.py.
    
    For example, crossings_arr might be generated by the following code:
        >>> data_analytic1 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.1)
        >>> crossings_analytic1 = data_analytic1["crossings"]
    

    Parameters
    ----------
    crossings_arr: 
        (possibly a list of) multidimensional list(s) in the format of the crossings dataset generated by the function gather_analytic_resonant_with_specified_p_and_x_value in orbit_data.py. That is: [(x_vals, vx_vals, vy_vals, label), ...]
    boxes_arr: list of lists
        A 2D list of BoundingBox objects.

    Returns
    -------
    None
    
    """
    
    for (x_vals, vx_vals, vy_vals, label) in crossings_arr:

        # print("x_vals ------------------------------", x_vals)

        point_arr = []
        for i in range(len(x_vals)): #Note that len(x_vals) = len(vy_vals) = number of crossings in this dataset.
            point_arr.append((x_vals[i], vy_vals[i]))

        plot_points_in_boxes(point_arr, boxes_arr, colour)

        
        
        
    
    # x_vals = crossings_arr[0][0]
    # vy_vals = crossings_arr[0][2]

    # print("x_vals ------------------------------", x_vals)


    # point_arr = []
    # for i in range(len(x_vals)): #Note that len(x_vals) = len(vy_vals) = number of crossings in this dataset.
    #     point_arr.append((x_vals[i], vy_vals[i]))

    # plot_points_in_boxes(point_arr, boxes_arr, colour)



def get_boxes_containing_crossings(crossings_arr, boxes_arr):
    """
    Returns a list of the boxes that contain the crossings in the given crossings_arr. Our implementation ensures that no box will be added to the list multiple times. I.e., even if a box contains multiple crossings, it will only be added to the list once.
    
    For example, crossings_arr might be generated by the following code:
        >>> data_analytic1 = gather_analytic_resonant_with_specified_p_and_x_value(max_p = 8, x_value = 0.1)
        >>> crossings_analytic1 = data_analytic1["crossings"]
    

    Parameters
    ----------
    crossings_arr: 
        (possibly a list of) multidimensional list(s) in the format of the crossings dataset generated by the function gather_analytic_resonant_with_specified_p_and_x_value in orbit_data.py. That is: [(x_vals, vx_vals, vy_vals, label), ...]
    """
    
    boxes_containing_crossings = []
    
    
    for (x_vals, vx_vals, vy_vals, label) in crossings_arr:

        for i in range(len(x_vals)): #Note that len(x_vals) = len(vy_vals) = number of crossings in this dataset.
            point = (x_vals[i], vy_vals[i])

            for j in range(len(boxes_arr)):
                for k in range(len(boxes_arr[0])):
                    if boxes_arr[j][k].contains_point(point[0], point[1]) and (boxes_arr[j][k] not in boxes_containing_crossings):  # If the box contains the point AND we haven't already added this box to the list (to avoid duplicates)
                        
                        boxes_containing_crossings.append(boxes_arr[j][k])
                        break  # No need to check other boxes once we find one that contains the point
    
    return boxes_containing_crossings
#######I CAN SPEED THIS UP^. FOR A GIVEN POINT, INSTEAD OF CHECKING EVERY BOX, WE NEED TO ALTER OUR contains_point FUNCTION TO TELL US WHETHER THE y CHECK FAILED, the x CHECK FAILED, or both.
####### IF THE x CHECK FAILED, THEN I DON'T NEED TO CHECK ANY OTHER BOXES IN THE COLUMN. (SHOULD BE EASY TO IMPLEMENT)
####### IF THE y CHECK FAILED, THEN I DON'T NEED TO CHECK ANY OTHER BOXES IN THE ROW (MIGHT BE A BIT MORE TEDIOUS/INDEX SENSITIVE TO IMPLEMENT)
####### I THINK THIS MEANS THAT THE BOX CHECKING PART OF THE ABOVE ALGORITHM SHOULD GO FROM O(n*m) TO O(n+m).

def find_percentage_covered(boxes_containing_crossings, all_boxes):
    """
    Returns the percentage of boxes that contain a crossing.
    
    Parameters
    ----------
    boxes_containing_crossings: list of BoundingBox objects
        A list of BoundingBox objects that contain the crossings.
    all_boxes: list of lists
        A 2D list of all BoundingBox objects generated by the generate_all_boxes function.

    Returns
    -------
    float
        The percentage of boxes that contain a crossing.
    """
    
    total_boxes = len(all_boxes) * len(all_boxes[0])  # Total number of boxes in the 2D list
    boxes_with_crossings = len(boxes_containing_crossings)  # Number of boxes that contain crossings
    
    percentage = (boxes_with_crossings / total_boxes) * 100  # Calculate percentage
    
    print(f"Total boxes: {total_boxes}")
    print(f"Boxes with crossings: {boxes_with_crossings}")
    print(f"Percentage of boxes with crossings: {percentage:.2f}%")
    
    return percentage
    
    
    
    

# def get_boxes_not_fully_in_crash_region(boxes_arr, crash_region_x_bound):





    
    
    
def test_plotting_one_box():
    box1 = BoundingBox(1.2,1.6,0,1)

    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)

    box1.shade_box(plot_bounding_curves=True)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()


def test_plotting_all_boxes():
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    line_width = 1

    boxes_arr = generate_all_boxes(h1=1, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6, chequerboard = 0)
    
    # print(boxes_arr)

    plot_boxes(boxes_arr)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()


def test_plotting_some_boxes():
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    line_width = 1

    boxes_arr = generate_all_boxes(h1=1, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6, chequerboard = 0)

    new_boxes_arr_inner = []
    new_boxes_arr_inner.append(boxes_arr[0][0])
    new_boxes_arr_inner.append(boxes_arr[3][4])
    
    # new_boxes_arr_inner.append(boxes_arr[1][2])

    new_boxes_arr_outer = []
    new_boxes_arr_outer.append(new_boxes_arr_inner)
    
    # print(new_boxes_arr_outer)

    plot_boxes(new_boxes_arr_outer, plot_bounding_curves=True)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()


def test_find_x_given_energy_and_y_value():
    x_val = find_x_given_energy_and_y_value(1.2,0.2)
    print(x_val)
    print(const_energy_curve(1.2, x_val))


def test_contains_point():
    box1 = BoundingBox(1.2,1.6,0.1,0.3)
    print("(-0.5, 0.2)", box1.contains_point(-0.5, 0.2))  # Should be True
    print("(-0.5, 0.3)", box1.contains_point(-0.5, 0.3))  # Should be True (boundary points are included)
    print("(-0.5, 0.4)", box1.contains_point(-0.5, 0.4))  # Should be False
    print("(-0.6, 0.4)", box1.contains_point(-0.6, 0.4))  # Should be False
    print("(-0.6, 0.2)", box1.contains_point(-0.6, 0.2))  # Should be False
    print("(-0.6, 0)", box1.contains_point(-0.6, 0))  # Should be False
    print("(1, 0.2)", box1.contains_point(1, 0.2))  # Should be False
    print("(0.5, 0.2)", box1.contains_point(0.5, 0.2))  # Should be False
    print("(-0.43, 0.2)", box1.contains_point(-0.43, 0.2))  # Should be True
    print("(-0.41, 0.299)", box1.contains_point(-0.41, 0.299))  # Should be True



####### I IMPLEMENTED A CLEANER VERSION INSTEAD
# def test_plot_points_in_boxes0():
#     fig = plt.figure(figsize=(12,8))
#     ax = fig.add_subplot(111)

#     ax.set_xlim(-0.5, 0)
#     ax.set_ylim(-0.1, 6)
#     line_width = 1

#     boxes_arr = generate_all_boxes(h1=1, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6)

    
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


def test_plot_points_in_boxes():
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)

    ax.set_xlim(-0.5, 0)
    ax.set_ylim(-0.1, 6)
    

    boxes_arr = generate_all_boxes(h1=1, energy_min=1, energy_max=6, h2=0.2, y_min=0, y_max=6)

    
    # test_points_arr = [(-0.5, 0.2), (-0.5, 0.3), (-0.5, 0.4), (-0.6, 0.4), (-0.6, 0.2), (-0.6, 0), (1, 0.2), (0.5, 0.2), (-0.43, 0.2), (-0.41, 0.299)]
    test_points_arr = [(-0.4, 0.15), (-0.3, 0.5), (-0.2, 2), (-0.15,3), (-0.059, 4.917), (-0.15, 0.1), (-0.45, 1.1)]

    
    plot_points_in_boxes(test_points_arr, boxes_arr)
    BoundingBox.plot_all_bounding_curves(h1=1, energy_min=1,energy_max=6, h2=0.2, y_min=0, y_max=6, line_width=1)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()




# test_plotting_one_box()

# test_plotting_all_boxes()

# test_plotting_some_boxes()

# test_find_x_given_energy_and_y_value()

# test_contains_point()

##### test_plot_points_in_boxes0()

# test_plot_points_in_boxes()