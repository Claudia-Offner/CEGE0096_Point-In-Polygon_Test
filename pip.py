import sys
""" The sys module is used to provide a max finite float number """


def sqrt(n):
    """ Square root function used in boundary identifying method (lines 87-89) """

    if n < 0:
        return
    else:
        return n**0.5


class Point:
    """ Point Class """

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


class Polygon:
    """ Polygon Class """

    def __init__(self, points):
        self.points = points

    def get_points(self):
        """ Extract points from object """
        return self.points

    def edges(self):
        """ Creates lines from points """

        res = []
        for i, p in enumerate(self.points):
            p1 = p
            p2 = self.points[(i+1) % len(self.points)]
            res.append((p1, p2))
        return res

    def contains(self, point):
        """ RCA Algorithm categorising if points are inside or outside a polygon object """

        _huge = sys.float_info.max    # act as infinity if we divide by 0
        _eps = 0.00001

        inside = False
        for edge in self.edges():
            a, b = edge[0], edge[1]
            # Edge A needs to be the lower point of the edge
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
                m_edge = (b.y-a.y) / (b.x-a.x)
            except ZeroDivisionError:
                m_edge = _huge
            try:
                m_point = (point.y-a.y) / (point.x-a.x)
            except ZeroDivisionError:
                m_point = _huge

            # Ray intersects with the edge
            if m_point >= m_edge:
                inside = not inside
                continue

        return inside

    def bound(self, point):
        """ Identifies points on the boundary of a polygon objects """

        boundary = False
        for edge in self.edges():
            a, b = edge[0], edge[1]

            # Distance between A and point
            ap = sqrt((a.x-point.x)**2 + (a.y-point.y)**2)
            # Distance between point and B
            pb = sqrt((point.x-b.x)**2 + (point.y-b.y)**2)
            # Distance between A and B
            ab = sqrt((a.x-b.x)**2 + (a.y - b.y)**2)
            # The point is on the boundary
            if ap + pb == ab:
                boundary = not boundary
                continue

        return boundary


class Square(Polygon):
    """ Square Class """
    def __init__(self, points):
        super().__init__(points)

    def basic_mbr(self):
        """ Extracts min and max points of a polygon objects MBR """
        # Use a min higher than expected  and max lower than expected
        min_x, min_y = 100000, 100000
        max_x, max_y = -100000, -100000

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
        """ Gives MBR square coordinates for plotting """

        a = self.basic_mbr()
        min_x, min_y, max_x, max_y = a[0], a[1], a[2], a[3]
        return [[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]]

    def get_mbr(self, point):
        """ MBR Algorithm categorising if points are inside or outside a polygon object's MBR """

        mbr = []
        a = self.basic_mbr()
        min_x, min_y, max_x, max_y = a[0], a[1], a[2], a[3]

        if min_x <= point.x <= max_x and min_y <= point.y <= max_y:
            mbr.append('inside')
        else:
            mbr.append('outside')
        return mbr