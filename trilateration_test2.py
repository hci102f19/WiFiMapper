import numpy as np


class Point(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return "Point"

    def __str__(self):
        return f"(Point) Lat: {self.lat}, Lon: {self.lon}"


class Circle(object):
    def __init__(self, point: Point, distance):
        self.point = point
        self.distance = distance

    @property
    def lat(self):
        return self.point.lat

    @property
    def lon(self):
        return self.point.lon

    def __repr__(self):
        return "Circle"

    def __str__(self):
        return f"(Circle) Lat: {self.lat}, Lon: {self.lon}, Distance: {self.distance}"


class Measurements(object):
    def __init__(self, *args):
        self.measurements = [a for a in args]

    def mean(self):
        return Point(
            np.mean([p.lat for p in self.measurements]),
            np.mean([p.lon for p in self.measurements])
        )

    def __repr__(self):
        return "Measurements"

    def __str__(self):
        return f"{self.measurements}"


if __name__ == '__main__':
    locations = [
        Point(57.012066380607, 9.990464594292007),
        Point(57.012071059249806, 9.99070602530378),
    ]


    def get_distance(frequency, signal):
        return 10 ** ((27.55 - (20 * np.log10(frequency)) - signal) / 20.0)


    measurements = Measurements(
        Circle(locations[0], get_distance(2437, -60)),
        Circle(locations[1], get_distance(2412, -60)),
    )

    initial_location = measurements.mean()

    print(initial_location)
    print(measurements)
