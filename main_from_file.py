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

def edges(self):
    ''' Returns a list of tuples that each contain 2 points of an edge '''
    edge_list = []
    for i, p in enumerate(self):
        p1 = p
        p2 = self[(i + 1) % len(self)]
        edge_list.append((p1, p2))
    return edge_list

polygon_sides = edges(poly_points)

############################################

class Point:
    def __init__(self, x, y):
        """
        A point specified by (x,y) coordinates in the cartesian plane
        """
        self.x = x
        self.y = y


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
        # _huge is used to act as infinity if we divide by 0
        _huge = sys.float_info.max
        # _eps is used to make sure points are not on the same line as vertexes
        _eps = 0.00001

        # We start on the outside of the polygon
        inside = False
        for edge in self.edges:
            # Make sure A is the lower point of the edge
            A, B = edge[0], edge[1]
            if A.y > B.y:
                A, B = B, A

            # Make sure point is not at same height as vertex
            if point.y == A.y or point.y == B.y:
                point.y += _eps

            if (point.y > B.y or point.y < A.y or point.x > max(A.x, B.x)):
                # The horizontal ray does not intersect with the edge
                continue

            if point.x < min(A.x, B.x): # The ray intersects with the edge
                inside = not inside
                continue

            try:
                m_edge = (B.y - A.y) / (B.x - A.x)
            except ZeroDivisionError:
                m_edge = _huge

            try:
                m_point = (point.y - A.y) / (point.x - A.x)
            except ZeroDivisionError:
                m_point = _huge

            if m_point >= m_edge:
                # The ray intersects with the edge
                inside = not inside
                continue

        return inside

q = Polygon(poly_points)
test_points = Point(input_x, input_y)
print(str(q.contains(test_points)))




def main():
    plotter = Plotter()
    print("read polygon.csv")

    print("read input.csv")

    print("categorize points")

    print("write output.csv")

    print("plot polygon and points")
    #plotter.show()

##Put your solution here ^^^

if __name__ == "__main__":
    main()

