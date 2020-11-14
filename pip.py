import sys

# Sources:
# MBR: https://stackoverflow.com/questions/20808393/python-defining-a-minimum-bounding-rectangle
# RCA: https://rosettacode.org/wiki/Ray-casting_algorithm#Python
# RCA: http://philliplemons.com/posts/ray-casting-algorithm
# Boundary: https://stackoverflow.com/questions/328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment


def sqrt(n):
    # Square root function (used in lines 87-89)
    if n < 0:
        return
    else:
        return n**0.5


class Point:
    # Point Class #
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


class Polygon:
    # Polygon Class #
    def __init__(self, points):
        self.points = points

    def get_points(self):
        return self.points

    def edges(self):
        # Creates lines from points

        res = []
        for i, p in enumerate(self.points):
            p1 = p
            p2 = self.points[(i+1) % len(self.points)]
            res.append((p1, p2))
        return res

    def contains(self, point):
        # RCA Algorithm #

        _huge = sys.float_info.max    # act as infinity if we divide by 0
        _eps = 0.00001     # ensures points are not on the same line as vertexes

        inside = False
        for edge in self.edges():
            # Edge A needs to be the lower point of the edge
            a, b = edge[0], edge[1]
            if a.y > b.y:
                a, b = b, a

            # Point is not at same height as vertex
            if point.y == a.y or point.y == b.y:
                point.y += _eps
            if point.x == a.x or point.x == b.x:
                point.x += _eps

            # Ray does not intersect with the edge
            if point.y > b.y or point.y < a.y or point.x > max(a.x, b.x):
                continue

            # Ray intersects with the edge
            if point.x < min(a.x, b.x):
                inside = not inside
                continue

            try:
                m_edge = (b.y - a.y) / (b.x - a.x)
            except ZeroDivisionError:
                m_edge = _huge
            try:
                m_point = (point.y - a.y) / (point.x - a.x)
            except ZeroDivisionError:
                m_point = _huge

            # Ray intersects with the edge
            if m_point >= m_edge:
                inside = not inside
                continue

        return inside

    def bound(self, point):
        # Boundary identifier #

        boundary = False
        for edge in self.edges():
            a, b = edge[0], edge[1]

            ap = sqrt((a.x - point.x) ** 2 + (a.y - point.y) ** 2)  # Distance between A and point
            pb = sqrt((point.x - b.x) ** 2 + (point.y - b.y) ** 2)  # Distance between point and B
            ab = sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)  # Distance between A and B

            # The point is on the boundary
            if ap + pb == ab:
                boundary = not boundary
                continue

        return boundary


class Square(Polygon):
    # Square Class #
    def __init__(self, points):
        super().__init__(points)

    def basic_mbr(self):
        # MBR calculator #

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

    def mbr_box(self):
        # MBR coordinates #

        a = self.basic_mbr()
        min_x, min_y, max_x, max_y = a[0], a[1], a[2], a[3]
        return [[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]]

    def get_mbr(self, point):
        # MBR Algorithm #

        mbr = []
        a = self.basic_mbr()
        min_x, min_y, max_x, max_y = a[0], a[1], a[2], a[3]

        if min_x <= point.x <= max_x and min_y <= point.y <= max_y:
            mbr.append('inside')
        else:
            mbr.append('outside')
        return mbr