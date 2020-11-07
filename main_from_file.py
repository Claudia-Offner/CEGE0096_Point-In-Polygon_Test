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

# CATEGORISE input_points as inside, outside or boundary and save to category_result (list)

######MBR#######

# mini
def min_(a):
    res = a[0]
    for i in a:
        if i < res:
            res = i
    return res
# maxi
def max_(a):
    res = a[0]
    for i in a:
        if i > res:
            res = i
    return res

x_min_max = []
y_min_max = []
x_min_max.append(min_(poly_x))
y_min_max.append(min_(poly_y))
x_min_max.append(max_(poly_x))
y_min_max.append(max_(poly_y))

print(x_min_max)
print(y_min_max)

##MBR box
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

mbr = []
for i in input_points:
    if min_(poly_x) < i[0] < max_(poly_x) and min_(poly_y) < i[1] < max_(poly_y):
        mbr.append('inside')
    else:
        mbr.append('outside')
input_mbr = [input_x, input_y, mbr]

#MATRIX CREATOR: combine mbr results with data points (from columns to rows AND rows to columns)
def transpose_matrix(matrix):
    res = []
    result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))] #https://www.programiz.com/python-programming/examples/transpose-matrix
    for r in result:
        res.append(r)
    return res

print(transpose_matrix(input_mbr))

### CALCULATE LINES ###

def edges(self):
    ''' Returns a list of tuples that each contain 2 points of an edge '''
    edge_list = []
    for i, p in enumerate(self):
        p1 = p
        p2 = self[(i + 1) % len(self)]
        edge_list.append((p1, p2))
    return edge_list

polygon_sides = edges(poly_points)


def contains(self, point):
    import sys
    # _huge is used to act as infinity if we divide by 0
    _huge = sys.float_info.max
    # _eps is used to make sure points are not on the same line as vertexes
    _eps = 0.00001

    # We start on the outside of the polygon
    inside = False
    ypoint = [i[1] for i in point]
    xpoint = [i[0] for i in point]
    for edge in self:
        # Make sure A is the lower point of the edge
        A, B = edge[0], edge[1]
        if A[1] > B[1]:
            A, B = B, A

        # Make sure point is not at same height as vertex
        if ypoint == A[1] or ypoint == B[1]:
            ypointy += _eps

        if (ypoint > B[1] or ypoint < A[1] or xpoint > max(A[0], B[0])):
            # The horizontal ray does not intersect with the edge
            continue

        if xpoint < min(A[0], B[0]):  # The ray intersects with the edge
            inside = not inside
            continue

        try:
            m_edge = (B[1] - A[1]) / (B[0] - A[0])
        except ZeroDivisionError:
            m_edge = _huge

        try:
            m_point = (ypoint - A[1]) / (xpoint - A[0])
        except ZeroDivisionError:
            m_point = _huge

        if m_point >= m_edge:
            # The ray intersects with the edge
            inside = not inside
            continue

    return inside

contains(polygon_sides, input_points)




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

