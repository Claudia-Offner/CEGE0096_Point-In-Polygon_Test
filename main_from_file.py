from plotter import Plotter
import sys

##Import code from FUNCTION/CLASS file here

#sources
## https://rosettacode.org/wiki/Ray-casting_algorithm#Python
## http://philliplemons.com/posts/ray-casting-algorithm
## https://excalibur.apache.org/framework/best-practices.html


## READ list of x,y coordinates from POLGYON.CSV as poly_points (list)

# def coord_reader(path):
#     with open(path,'r') as f:
#         data = f.readlines()[1:]  # skip header
#         points = []
#         for line in data:
#             res = line.rstrip().split(',')[1:]  # split by line
#             res = [float(i) for i in res]  # convert to integers
#             points.append(res)
#MATRIX CREATOR: combine mbr results with data points (from columns to rows AND rows to columns)
def transpose_matrix(matrix):
    res = []
    result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))] #https://www.programiz.com/python-programming/examples/transpose-matrix
    for r in result:
        res.append(r)
    return res


with open('polygon.csv', 'r') as f:
    data = f.readlines()[1:] #skip header
    poly_points = []
    poly_x = []
    poly_y = []
    for line in data:
        res = line.rstrip().split(',')[1:] #split by line
        res = [float(i) for i in res] #convert to integers
        poly_points.append(res)
    poly_x = [i[0] for i in poly_points]
    poly_y = [i[1] for i in poly_points]
print(poly_points)
print(poly_x)
print(poly_y)

with open('input.csv', 'r') as f:
    data = f.readlines()[1:] #skip header
    input_points = []
    input_x = []
    input_y = []
    for line in data:
        res = line.rstrip().split(',')[1:] #split by line
        res = [float(i) for i in res] #convert to integers
        input_points.append(res)
    input_x = [i[0] for i in input_points]
    input_y = [i[1] for i in input_points]
print(input_points)
print(input_x)
print(input_y)

plotter = Plotter()
# plotter.add_polygon(poly_x, poly_y)
# plotter.add_point(input_x, input_y)
# plotter.show()



# CATEGORISE input_points as inside, outside or boundary and save to category_result (list)


#################  CLASS ###########################
## http://philliplemons.com/posts/ray-casting-algorithm
class Point:
    def __init__(self, x, y):
        """
        A point specified by (x,y) coordinates in the cartesian plane
        """
        self.x = x
        self.y = y

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

class Polygon:
    def __init__(self, points):
        """
        points: a list of Points in clockwise order.
        """
        self.points = points

    def edges(self):
        ''' Returns a list of tuples that each contain 2 points of an edge '''
        edge_list = []
        for i, p in enumerate(self.points):
            p1 = p
            p2 = self.points[(i + 1) % len(self.points)]
            edge_list.append((p1, p2))
        return edge_list

    def contains(self, point): ### RCA ALGORITHM ###
        _huge = sys.float_info.max # _huge is used to act as infinity if we divide by 0
        _eps = 0.00001  # _eps is used to make sure points are not on the same line as vertexes
        intersect = []
        for edge in self.edges():
            # A is the lower point of the edge
            A, B = edge[0], edge[1]
            X, Y = point[0], point[1]
            if A[1] > B[1]:
                A, B = B, A
            # Point is not at same height as vertex
            if Y == A[1] or Y == B[1]:
                Y += _eps

            # The ray does not NOT intersect with the edge
            if (Y > B[1] or Y < A[1] or X > max(A[0], B[0])):
                intersect.append('FALSE')
                continue
            # The ray intersects with the edge
            if X < min(A[0], B[0]):
                intersect.append('TRUE')
                continue
            #Get slope of line
            try:
                m_edge = (B[1] - A[1]) / (B[0] - A[0])
            except ZeroDivisionError:
                m_edge = _huge
            #Get slope of point
            try:
                m_point = (Y- A[1]) / (X - A[0])
            except ZeroDivisionError:
                m_point = _huge

            if m_point >= m_edge:
                # The ray intersects with the edge
                intersect.append('TRUE')
                continue

        return intersect

    def boundary(edges, point):
        _eps = 0.00001  # _eps is used to make sure points are not on the same line as vertexes
        boundary = False
        for edge in edges():
            # A is the lower point of the edge
            A, B = edge[0], edge[1]
            X, Y = point[0], point[1]

            crossproduct = (Y - A[1]) * (X - A[0]) - (X - A[0]) * (Y - A[1])

            # compare versus epsilon for floating point values, or != 0 if using integers
            if abs(crossproduct) > _eps:
                continue

            dotproduct = (X - A[0]) * (B[0] - A[0]) + (Y - A[1]) * (B[1] - A[1])
            if dotproduct < 0:
                continue

            squaredlengthba = (B[0] - A[0]) * (B[0] - A[0]) + (B[1] - A[1]) * (B[1] - A[1])
            if dotproduct > squaredlengthba:
                continue

            boundary = True

        return boundary

class Square(Polygon): ## MBR CLASS ##

    def __init__(self, points):
        super().__init__(points)

    def basic_mbr(self):  # source: https://stackoverflow.com/questions/20808393/python-defining-a-minimum-bounding-rectangle

        min_x = 100000  # start with something much higher than expected min
        min_y = 100000
        max_x = -100000  # start with something much lower than expected max
        max_y = -100000

        for item in self.points:
            if item[0] < min_x:
                min_x = item[0]

            if item[0] > max_x:
                max_x = item[0]

            if item[1] < min_y:
                min_y = item[1]

            if item[1] > max_y:
                max_y = item[1]

        return [min_x, min_y, max_x, max_y] # return [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)] if you want the coords

    def get_mbr(self, points):
        mbr = []
        a = self.basic_mbr()
        min_x, min_y, max_x, max_y = a[0], a[1], a[2], a[3]
        for i in points:
            if min_x < i[0] < max_x and min_y < i[1] < max_y:
                mbr.append("inside")
            else:
                mbr.append("outside")
        return mbr

    def mbr_box(self):
        b = self.basic_mbr()
        min_x, min_y, max_x, max_y = b[0], b[1], b[2], b[3]
        return [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]

#check if a list of points is within in the polygon
q = Polygon(poly_points)
a = [q.contains(p) for p in input_points]
b = [q.edges(p) for p in input_points]
c = []

# b = [q.boundary(p) for p in input_points]


# for point in input_points:
#     if q.boundary[point] is True:
#         c.append(point)

print(a)
print(b)
print(c)
#count intersections & determine if inside/outside/boundary polygon
# count = ([i.count('TRUE') for i in a], [i.count('FALSE') for i in a], [i.count(True) for i in b])
# count_2 = transpose_matrix(count)
# print(count_2)
# lb = []
# for i in count_2:
#     if i[2] == 0:
#         if (i[0] % 2) == 0:
#             lb.append('outside')
#         else:
#             lb.append('inside')
#     else:
#         lb.append('boundary')
# print(lb)

# Plot points
plotter.add_polygon(poly_x, poly_y)
for x, y, label in zip(input_x,input_y,lb):
    plotter.add_point(x, y, kind = label)
plotter.show()

###### GET MBR ########
# p = Square(poly_points)
# label_mbr = p.get_mbr(input_points)
# boxy = transpose_matrix(p.mbr_box())
# print(boxy)
# plotter.add_polygon(poly_x, poly_y)
# plotter.add_polygon(boxy[0], boxy[1])
# for x, y, label in zip(input_x,input_y,label_mbr):
#     plotter.add_point(x, y, kind = label)
# plotter.show()


# def main():
#     plotter = Plotter()
#     print("read polygon.csv")
#
#     print("read input.csv")
#
#     print("categorize points")
#
#     print("write output.csv")
#
#     print("plot polygon and points")
#     #plotter.show()
#
# ##Put your solution here ^^^
#
# if __name__ == "__main__":
#     main()