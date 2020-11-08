from plotter import Plotter

##Import code from FUNCTION/CLASS file here

## READ list of x,y coordinates from POLGYON.CSV as poly_points (list)

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

#MATRIX CREATOR: combine mbr results with data points (from columns to rows AND rows to columns)
def transpose_matrix(matrix):
    res = []
    result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))] #https://www.programiz.com/python-programming/examples/transpose-matrix
    for r in result:
        res.append(r)
    return res

# CATEGORISE input_points as inside, outside or boundary and save to category_result (list)

######MBR#######


##MBR box_coords
def mbr_box(coords): #source: https://stackoverflow.com/questions/20808393/python-defining-a-minimum-bounding-rectangle

  min_x = 100000 # start with something much higher than expected min
  min_y = 100000
  max_x = -100000 # start with something much lower than expected max
  max_y = -100000

  for item in coords:
    if item[0] < min_x:
      min_x = item[0]

    if item[0] > max_x:
      max_x = item[0]

    if item[1] < min_y:
      min_y = item[1]

    if item[1] > max_y:
      max_y = item[1]

  return [(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y)]

mbr_x = []
mbr_y = []
mbr_res = mbr_box(poly_points)
mbr_x = [i[0] for i in mbr_res]
mbr_y = [i[1] for i in mbr_res]

# plotter.add_polygon(poly_x, poly_y)
# plotter.add_polygon(mbr_x, mbr_y)
# plotter.add_point(input_x, input_y)
# plotter.show()

# METHOD mini
def min_(a):
    res = a[0]
    for i in a:
        if i < res:
            res = i
    return res

# METHOD maxi
def max_(a):
    res = a[0]
    for i in a:
        if i > res:
            res = i
    return res

#PRINT MBC Results
mbr = []
for i in input_points:
    if min_(poly_x) < i[0] < max_(poly_x) and min_(poly_y) < i[1] < max_(poly_y):
        mbr.append('inside')
    else:
        mbr.append('outside')
input_mbr = [input_x, input_y, mbr]
print(transpose_matrix(input_mbr))

### CALCULATE RCA ###
# Find edges of the polygon
# def edges(self):
#     ''' Returns a list of tuples that each contain 2 points of an edge '''
#     edge_list = []
#     for i, p in enumerate(self):
#         p1 = p
#         p2 = self[(i + 1) % len(self)]
#         edge_list.append((p1, p2))
#     return edge_list
#
# poly_edge = edges(poly_points)

#find ray intersections
# from collections import namedtuple
# import sys
#
# Pt = namedtuple('Pt', 'x, y')  # Point
# Edge = namedtuple('Edge', 'a, b')  # Polygon edge from a to b
# Poly = namedtuple('Poly', 'name, edges')
#
# _eps = 0.00001
# _huge = sys.float_info.max
# _tiny = sys.float_info.min
#
# def rayintersectseg(p, edge):
#     ''' takes a point p=Pt() and an edge of two endpoints a,b=Pt() of a line segment returns boolean
#     '''
#     py, px = p[0], p[1]
#
#     intersect = False
#     for i in edge:
#         a, b = i[0], i[1]
#         ay, ax, bx, by = a[0], a[1], b[0], b[1]
#         #Make sure A is the lower point of the edge
#         if ay > by:
#             a, b = b, a
#         #Make sure point is not at the same height as the vertex
#         if py == ay or py == by:
#             py += _eps
#
#         if py > by or py < ay or px > max(ax, bx):
#             return False # The horizontal ray does not intersect with the edge
#
#         if px < min(ax, bx):
#             intersect = True # The ray intersects with the edge
#
#         else:
#             if abs(ax - bx) > _tiny:
#                 m_red = (by - ay) / float(bx - ax)
#             else:
#                 m_red = _huge
#             if abs(ax - px) > _tiny:
#                 m_blue = (py - ay) / float(px - ax)
#             else:
#                 m_blue = _huge
#             if m_blue >= m_red:
#                 intersect = True # The ray intersects with the edge
#
#         return intersect
#
# def _odd(x): return x % 2 == 1
#
# def ispointinside(p, poly):
#     return _odd(sum(rayintersectseg(p, edge) for edge in poly))
#
# for i in input_points:
#     print(rayintersectseg(input_points, poly_edge))







################# CLASSES ###########################

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

    def contains(self, point): ##need to make method iterable ##
        import sys
        _huge = sys.float_info.max # _huge is used to act as infinity if we divide by 0
        _eps = 0.00001  # _eps is used to make sure points are not on the same line as vertexes
        intersect = []
        inside = False # We start on the outside of the polygon
        for edge in self.edges():
            # A is the lower point of the edge
            A, B = edge[0], edge[1]
            if A[1] > B[1]:
                A, B = B, A

            # Point is not at same height as vertex
            if point.y == A[1] or point.y == B[1]:
                point.y += _eps

            if (point.y > B[1] or point.y < A[1] or point.x > max(A[0], B[0])):
                # The horizontal ray does not intersect with the edge
                intersect.append('No Intersect')
                continue

            if point.x < min(A[0], B[0]): # The ray intersects with the edge
                inside = not inside
                intersect.append('Intersect')
                continue

            try:
                m_edge = (B[1] - A[1]) / (B[0] - A[0])
            except ZeroDivisionError:
                m_edge = _huge

            try:
                m_point = (point.y - A[1]) / (point.x - A[0])
            except ZeroDivisionError:
                m_point = _huge

            if m_point >= m_edge:
                # The ray intersects with the edge
                inside = not inside
                intersect.append('Intersect')
                continue

        return intersect



q = Polygon(poly_points)
poly_edges = q.edges()
print(poly_edges)

p1 = Point(-0.5,5)
print(str(q.contains(p1)))

#print(str(q.contains(test_points)))



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