import math

import matplotlib.pyplot as plt


class BaseStation(object):
    def __init__(self, lat, lon, dist):
        self.lat = lat
        self.lon = lon
        self.dist = dist


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle(object):
    def __init__(self, point, radius):
        self.center = point
        self.radius = radius


class JSONData(object):
    def __init__(self, circles, inner_points, center):
        self.circles = circles
        self.inner_points = inner_points
        self.center = center


def serialize_instance(obj):
    d = {}
    d.update(vars(obj))
    return d


def get_two_points_distance(p1, p2):
    return math.sqrt(pow((p1.x - p2.x), 2) + pow((p1.y - p2.y), 2))


def get_two_circles_intersecting_points(c1, c2):
    p1 = c1.center
    p2 = c2.center
    r1 = c1.radius
    r2 = c2.radius

    d = get_two_points_distance(p1, p2)
    # if to far away, or self contained - can't be done
    if d >= (r1 + r2) or d <= math.fabs(r1 - r2):
        return None

    a = (pow(r1, 2) - pow(r2, 2) + pow(d, 2)) / (2 * d)
    h = math.sqrt(pow(r1, 2) - pow(a, 2))
    x0 = p1.x + a * (p2.x - p1.x) / d
    y0 = p1.y + a * (p2.y - p1.y) / d
    rx = -(p2.y - p1.y) * (h / d)
    ry = -(p2.x - p1.x) * (h / d)
    return [Point(x0 + rx, y0 - ry), Point(x0 - rx, y0 + ry)]


def get_all_intersecting_points(circles):
    points = []
    num = len(circles)
    for i in range(num):
        j = i + 1
        for k in range(j, num):
            res = get_two_circles_intersecting_points(circles[i], circles[k])
            if res:
                points.extend(res)
    return points


def is_contained_in_circles(point, circles):
    for i in range(len(circles)):
        if get_two_points_distance(point, circles[i].center) > circles[i].radius:
            return False
    return True


def get_polygon_center(points):
    center = Point(0, 0)
    num = len(points)
    for i in range(num):
        center.x += points[i].x
        center.y += points[i].y
    center.x /= num
    center.y /= num
    return center


if __name__ == '__main__':

    p1 = Point(0.81, 1.2)
    p2 = Point(1.21, 0.69)
    p3 = Point(0.87, 0.84)

    c1 = Circle(p1, 0.70)
    c2 = Circle(p2, 0.51)
    c3 = Circle(p3, 0.63)

    circle_list = [c1, c2]

    inner_points = []
    for p in get_all_intersecting_points(circle_list):
        if is_contained_in_circles(p, circle_list):
            inner_points.append(p)

    center = get_polygon_center(inner_points)

    ax = plt.gca()
    ax.cla()
    ax.set_xlim((0, 2.2))
    ax.set_ylim((0, 2.2))

    for c in circle_list:
        x, y, r = (c.center.x, c.center.y, c.radius)

        point = plt.Circle((x, y), 0.05, color='r')
        circle = plt.Circle((x, y), r, color='b', fill=False)

        ax.add_artist(point)
        ax.add_artist(circle)

    c = plt.Circle((center.x, center.y), 0.05, color='g')
    ax.add_artist(c)

    plt.show()
