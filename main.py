
#FILE READER. OUTPUT: POINTS, X's, Y's
with open(path, 'r') as f:
    data = f.readlines()[1:] #skip header
    poly_points = []
    poly_x = []
    poly_y = []
    for line in data:
        res = line.rstrip().split(',')[1:]  # split by line
        res = [float(i) for i in res]  # convert to integers
        poly_points.append(res)
    poly_x = [i[0] for i in poly_points] #extract x column
    poly_y = [i[1] for i in poly_points] #extract y column
print(poly_points)
print(poly_x)
print(poly_y)
####set main, give path a string (make it relative, not pc based) --> NEEDS FIXING



### LECTURE CLASS EXAMPLE ###
class Geometry:
    def __init__(self, name):
        self.__name = name
    def get_name(self):
        return self.__name

class Point(Geometry):
    def __init__(self, name, x, y):
        super().__init__(name)
        self.__x = x
        self.__y = y
    def get_x(self):
        return self.__x
    def get_y(self):
        return self.__y

class Line(Geometry):
    def __init__(self, name, point_1, point_2):
        super().__init__(name)
        self.__point_1 = point_1
        self.__point_2 = point_2

class Polygon(Geometry):
    def __init__(self, name, points):
        super().__init__(name)
        self.__points = points
    def get_points(self):
        return self.__points
    def lines(self):
        res = []
        points = self.get_points()
        point_a = points[0]
        for point_b in points[1:]:
            res.append(Line(point_a.get_name() + '-' + point_b.get_name(), point_a, point_b))
            point_a = point_b
        res.append(Line(point_a.get_name() + '-' + points[0].get_name(), point_a, points[0]))
        return res




###PSEUDO CODE IDEAS####

##HELPFUL
## https://rosettacode.org/wiki/Ray-casting_algorithm#Python
## http://philliplemons.com/posts/ray-casting-algorithm
## https://excalibur.apache.org/framework/best-practices.html

#CLASS Creator
    #METHOD read points
        #clockwise, in order, as integers
    #METHOD read columns

#SUB CLASS Point_creator (Creator)
    #METHOD create points
        #extract y values from list and combine with a standard infinite x-value; output list to input_infinite

#SUB CLASS Line_creator (Creator)
    #METHOD connect points within lists
        #connect polygon_points; output list to polygon_side
    #METHOD connect points between lists
        #connect input_points with corresponding input_infinite points; output list to input_rays

#CLASS PIP_test
    #METHOD set as points
        #lists used as coordinates
    #METHOD set as lines
        #lists used as lines

#SUB CLASS MBR (PIP_Test)
    #(for points)
    #METHOD mini
        #extract minimum values from x and y columns; as x_min and y_min
    #METHOD maxi
        #extract maximum values from x and y columns; as x_max and y_max
    #METHOD get_MBR
        #extract list of points inside and outside rectangle; as MBR_results
        # IF x_min < point.x < x_max AND y_min < point.y < y.max:
            # THEN point is inside the MBR = TRUE (but we don't know about the polygon)
        # ELSE:
            # THEN point is outside the MBR = FALSE

#SUB CLASS Line_Crossing (PIP_test)
    #(for lines)
    #METHOD self
        #equation_list
    #METHOD slope
        #extract slope of lines; output to a new column in equation_list (do for both polygon_sides and input_rays)
    #METHOD y_int
        #extract y-int of a line list; ouput to a new column in equation_list (do for both polygon_sides and input_rays)
    #METHOD sorter
        #evaluate input_rays against each polygon_sides and sort them into parallel(same slope), coinciding(same slope & y-int) or intersecting
        #IF NOT coinciding OR parallel
            #THEN find the intersecting point
    #METHOD intersection
        #extract intersecting point for each input_ray on every
        #FOR each input_ray in range of polygon_sides
            #IF ray is NOT parallel to the x-axis
                #x point = (yintL - yintR)/(slopeR - slopeL)
                #y point = (yintL*slopeR - yintR*slopeL)/ (slopeR-slopeL)
            #ELSE
                #x point = (yintL - yR)/slopeR
                #y point = yR
    #METHOD checker
        #Check intersection point against the MBR(ray) and MBR(line)
        #IF intersection inside MBR(ray) AND MBR(side)set to TRUE


 #SUB CLASS RCA (PIP_test)
    #(for lines)
    #METHOD get_rca
        #Extract analysis; output to RCA_results
        #SET counting to 0
        #FOR each line of polygon:
            #IF ray crosses the line = TRUE:
                #THEN INC counting by 1
        #IF counting is odd:
            #THEN the point is inside
        #ELSE
            #THEN the point is outside

#SUB CLASS Point_on_line (RCA)
    #(for points)
    #METHOD get_boundary
        # Update RCA_results with boundary identification
        # FOR each input point(x3, y3) and each line (x1,y1,x2,y2):
                #IF x3,y3 is outside MBR
                    #THEN input is NOT on boundary (FALSE)
                #ELIF (x3-x1)/(x2-x1) * (y2-y1) + y1 = y3:
                    #THEN input point IS on the boundary (TRUE)
                #ELIF x3 = x1 OR x3 = x2:
                    #THEN input IS on the boundary (TRUE)
                #ELSE:
                    #THEN the point is NOT on the boundary (FALSE)

#SUB CLASS Point_on_vertices (RCA)
    #(for points)
    #METHOD get_vertices
        #Update RCA_results so that false positives/negatives are corrected
        #FOR ray in range(polygon_line)
            #IF current_line AND previous_line > ray y coordinate
                #THEN count none
            #ELIF current_line AND previous_line < ray y coordinate
                #THEN count none
            #ELSE
                #Then count one

#POLY CLASS Point_on_vertices
    # Point Crossing Vertices Algorithm (lines paralell with the x-axis)
    #???


# Write the result of each point in a CSV file;
# Plot the points and polygon in a plot window


