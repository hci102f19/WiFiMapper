import math
from scipy.optimize import minimize


def mse(x, locations, distances):
    mse = 0.0
    for location, distance in zip(locations, distances):
        distance_calculated = great_circle_distance(x[0], x[1], location[0], location[1])
        mse += math.pow(distance_calculated - distance, 2.0)
    return mse / len(locations)


EARTH_CIRCUMFERENCE = 6378137  # earth circumference in meters


def great_circle_distance(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) * math.sin(d_lon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = EARTH_CIRCUMFERENCE * c

    return d


def calc_stuff(locations, distances):
    initial_location = [0, 0]
    result = minimize(
        mse,  # The error function
        initial_location,  # The initial guess
        args=(locations, distances),  # Additional parameters for mse
        method='L-BFGS-B',  # The optimisation algorithm
        options={
            'ftol': 1e-5,  # Tolerance
            'maxiter': 1e+7  # Maximum iterations
        })
    location = result.x

    return location


if __name__ == '__main__':
    locations = [(57.012066380607, 9.990464594292007), (57.012071059249806, 9.99070602530378)]
    distances = [9.79, 9.89]

    print(calc_stuff(locations, distances))
