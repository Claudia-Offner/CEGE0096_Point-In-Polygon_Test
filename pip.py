import sys

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
        _huge = sys.float_info.max    # act as infinity if we divide by 0
        _eps = 0.00001     # ensures points are not on the same line as vertexes

        inside = False
        for edge in self.edges():
            # A needs to be the lower point of the edge
            A, B = edge[0], edge[1]
            if A.y > B.y:
                A, B = B, A

            # Point is not at same height as vertex
            if point.y == A.y or point.y == B.y:
                point.y += _eps

            if point.x == A.x or point.x == B.x:
                point.x += _eps

            if (point.y > B.y or point.y < A.y or point.x > max(A.x, B.x)):
                # The ray does NOT intersect with the edge
                continue

            if point.x < min(A.x, B.x):
                # The ray intersects with the edge
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

            AP = sqrt((A.x - point.x) ** 2 + (A.y - point.y) ** 2)  # Distance between A and point
            PB = sqrt((point.x - B.x) ** 2 + (point.y - B.y) ** 2)  # Distance between point and B
            AB = sqrt((A.x - B.x) ** 2 + (A.y - B.y) ** 2)  # Distance between A and B

            if AP + PB == AB:
                # The point is on the boundary
                boundary = not boundary
                continue

        return boundary

class Square(Polygon): ## MBR CLASS ##

    def __init__(self, points):
        super().__init__(points)

    def basic_mbr(self):  # source: https://stackoverflow.com/questions/20808393/python-defining-a-minimum-bounding-rectangle

        min_x, min_y = 100000, 100000  # start with something much higher than expected min
        max_x, max_y = -100000, -100000  # start with something much lower than expected max

        for item in self.points:
            if item.x < min_x:
                min_x = item.x

            if item.x > max_x:
                max_x = item.x

            if item.y < min_y:
                min_y = item.y

            if item.y > max_y:
                max_y = item.y

        return [min_x, min_y, max_x, max_y]

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
