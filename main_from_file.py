from plotter import Plotter
import sys

## Sources
## https://rosettacode.org/wiki/Ray-casting_algorithm#Python
## http://philliplemons.com/posts/ray-casting-algorithm
## https://excalibur.apache.org/framework/best-practices.html
## https://www.programiz.com/python-programming/examples/transpose-matrix

def coord_reader(path):
    with open(path,'r') as f:
        data = f.readlines()[1:]  # skip header
        points = []
        for line in data:
            res = line.rstrip().split(',')  # split by line
            res = [float(i) for i in res]  # convert to integers
            points.append(res)
        return points

def transpose_matrix(matrix):
    res = []
    result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    for r in result:
        res.append(r)
    return res

def sqrt(n):
  if n < 0:
    return
  else:
    return n**0.5

class Point:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Polygon:
    def __init__(self, points):
        self.points = points

    def get_points(self):
        return self.points

    def edges(self):
        res = []
        for i,p in enumerate(self.points):
            p1 = p
            p2 = self.points[(i+1) % len(self.points)]
            res.append((p1,p2))
        return res

    def contains(self, point):
        # _huge is used to act as infinity if we divide by 0
        _huge = sys.float_info.max
        # _eps is used to make sure points are not on the same line as vertexes
        _eps = 0.00001

        # We start on the outside of the polygon
        inside = False
        for edge in self.edges():
            # Make sure A is the lower point of the edge
            A, B = edge[0], edge[1]
            if A.y > B.y:
                A, B = B, A

            # Make sure point is not at same height as vertex
            if point.y == A.y or point.y == B.y:
                point.y += _eps

            if point.x == A.x or point.x == B.x:
                point.x += _eps

            if (point.y > B.y or point.y < A.y or point.x > max(A.x, B.x)):
                # The horizontal ray does not intersect with the edge
                continue

            if point.x < min(A.x, B.x):  # The ray intersects with the edge
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

    def bound(self, point):
        boundary = False
        for edge in self.edges():
            A, B = edge[0], edge[1]

            AP = sqrt((A.x - point.x) ** 2 + (A.y - point.y) ** 2)
            PB = sqrt((point.x - B.x) ** 2 + (point.y - B.y) ** 2)
            AB = sqrt((A.x - B.x) ** 2 + (A.y - B.y) ** 2)

            if AP + PB == AB:
                boundary = not boundary
                continue

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
            if item.x < min_x:
                min_x = item.x

            if item.x > max_x:
                max_x = item.x

            if item.y < min_y:
                min_y = item.y

            if item.y > max_y:
                max_y = item.y

        return [min_x, min_y, max_x, max_y] # return [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)] if you want the coords

    def get_mbr(self, point):
        mbr = []
        a = self.basic_mbr()
        min_x, min_y, max_x, max_y = a[0], a[1], a[2], a[3]
        # for i in points:
        if min_x <= point.x <= max_x and min_y <= point.y <= max_y:
            mbr.append('inside')
        else:
            mbr.append('outside')
        return mbr

    def mbr_box(self):
        b = self.basic_mbr()
        min_x, min_y, max_x, max_y = b[0], b[1], b[2], b[3]
        return [[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]]


if __name__ == "__main__":

    # Read data from files
    poly_list = coord_reader('polygon.csv')
    input_list = coord_reader('input.csv')


    # Extract X's and Y's from points for plotter inputs
    poly_x = [i[1] for i in poly_list]
    poly_y = [i[2] for i in poly_list]
    input_x = [i[1] for i in input_list]
    input_y = [i[2] for i in input_list]

    # Convert polygon and input lists into points
    poly_p = []
    for i in poly_list:
        point = Point(i[0], i[1], i[2])
        poly_p.append(point)

    input_p = []
    for i in input_list:
        point = Point(i[0], i[1], i[2])
        input_p.append(point)

    # Create a MBR Object, s
    s = Square([point for point in poly_p])
    # Create a Polygon Object, p
    p = Polygon([point for point in poly_p])
    # Create Plotter Object, plotter
    plotter = Plotter()

    '''
    Get MBR results
    '''
    # Extract MBR outputs
    mbr_id = [i.id for i in input_p]
    mbr_x = [i.x for i in input_p]
    mbr_y = [i.y for i in input_p]
    mbr_out = [s.get_mbr(i) for i in input_p]
    mbr_out = [item for l in mbr_out for item in l]
    mbr_res = transpose_matrix([mbr_id, mbr_x, mbr_y, mbr_out])
    print('MBR Results: ', mbr_res)

    # Separate inside & outside MBR points
    mbr_in = []
    mbr_out = []
    for i in mbr_res:
        if i[3] == 'inside':
            mbr_in.append(i)
        else:
            mbr_out.append(i)
            continue
    print('Points outside MBR: ', mbr_out)
    print('Points inside mbr: ', len(mbr_in))   # should be 55
    print('Points outside mbr: ', len(mbr_out))

    # Create point object for points inside mbr (for boundary analysis)
    in_mbr = []
    for i in mbr_in:
        point = Point(i[0], i[1], i[2])
        in_mbr.append(point)

    '''
    Get BOUNDARY results based on point inside mbr without vertex points
    '''
    # Extract Boundary outputs
    bound_id = [i.id for i in in_mbr]
    bound_x = [i.x for i in in_mbr]
    bound_y = [i.y for i in in_mbr]
    bound_out = [p.bound(i) for i in in_mbr]

    # Categorise if points are on/off polygon boundaries
    bound_res = []
    for i in bound_out:
        if i == True:
            bound_res.append('boundary')
        else:
            bound_res.append('n/a')
    bound_res = transpose_matrix([bound_id, bound_x, bound_y, bound_res])

    # Categorise vertices as on boundary
    vertex_on = []
    for i in bound_res:
        for j in poly_list:
            if i[1] == j[1] and i[2] == j[2]:
                vertex_on.append(i)
    for i in vertex_on:
        i[3] = 'boundary'
    # Replace vertex values with the correct category
    for i in bound_res:
        for j in vertex_on:
            if i[0] == j[0]:
                i = j
    print('Boundary Results: ', bound_res)

    # Separate points that are on and off the boundary
    bound_on = []
    bound_off = []
    for i in bound_res:
        if i[3] == 'boundary':
            bound_on.append(i)
        else:
            bound_off.append(i)
            continue
    print('Points on Boundary: ', bound_on)
    print('Points on boundary: ', len(bound_on))    # should be 24
    print('Points off boundary: ', len(bound_off))

    # Create point object for points not on boundary (for RCA analysis)
    off_bound = []
    for i in bound_off:
        point = Point(i[0], i[1], i[2])
        off_bound.append(point)

    ''' 
    Get RCA results based on points inside mbr and not on boundary 
    '''
    # Extract Boundary outputs
    rca_id = [i.id for i in off_bound]
    rca_x = [i.x for i in off_bound]
    rca_y = [i.y for i in off_bound]
    rca_out = [p.contains(i) for i in off_bound]
    rca_res = []
    for i in rca_out:
        if i == True:
            rca_res.append('inside')
        else:
            rca_res.append('outside')
    rca_res = transpose_matrix([rca_id, rca_x, rca_y, rca_res])
    print('RCA Results: ', rca_res)

    # Separate points that are inside and outside RCA
    rca_in = []
    rca_out = []
    for i in rca_res:
        if i[3] == 'inside':
            rca_in.append(i)
        else:
            rca_out.append(i)
            continue
    print('Points Inside RCA: ', rca_in)
    print('Points in rca: ', len(rca_in))   # should be 15
    print('Points out of rca: ', len(rca_in))

    '''
    Classify data outputs
    '''
    # Combine points outside the RCA with points outside the MBR
    for i in rca_out:
        mbr_out.append(i)

    # Categorise points
    final = []
    for p in input_p:
        for i in mbr_out:
            if p.id == i[0]:
                final.append(i)
            else:
                continue
        for i in bound_on:
            if p.id == i[0]:
                final.append(i)
            else:
                continue
        for i in rca_in:
            if p.id == i[0]:
                final.append(i)

    print(len(mbr_out) + len(bound_on) + len(rca_in))   # should be 100
    final = transpose_matrix(final)
    print(final)

    '''
    Plot points
    '''
    plotter.add_polygon(poly_x, poly_y)
    # plotter.add_point(bound_x, bound_y)
    for x, y, label in zip(final[1], final[2], final[3]):
        plotter.add_point(x, y, kind = label)
    plotter.show()



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