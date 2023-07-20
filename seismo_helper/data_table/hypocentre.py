import numpy as np
import scipy
from scipy.optimize import Bounds
from scipy.optimize import fsolve
from pyproj import Transformer

def hypocentre_search(stations: list[list]) -> tuple:
    velocity = 6
    stations = np.array(stations)
    modulo = [0, 0]
    for ind_station, [x, y, z, t] in enumerate(stations):
        x, y = convert_to_xy(x, y)
        modulo[0] += x // 100000
        modulo[1] += y // 100000
        x, y = x % 100000 / 1000, y % 100000 / 1000
        z /= 1000
        stations[ind_station] = [x, y, z, t]
    func = lambda x: sum([
        (st[3] - (x[3] + 1 / velocity * (
                (st[0] - x[0]) ** 2 + (st[1] - x[1]) ** 2 + (st[2] - x[2]) ** 2) ** 0.5)) ** 2
        for st in stations]) / len(stations)
    bound = Bounds([np.array(stations)[:, 0].min() - 2, np.array(stations)[:, 1].min() - 2, -1, np.array(stations)[:, 3].mean() - 10],
                   [np.array(stations)[:, 0].max() + 2, np.array(stations)[:, 1].max() + 2, 4, np.array(stations)[:, 3].mean() + 5])

    res = scipy.optimize.differential_evolution(
        func,
        maxiter=10000,
        tol=10e-15,
        polish=True,
        strategy='best2exp',
        bounds=bound,
        disp=False)

    x, y, z, t = res.x
    x, y = modulo[0] / len(stations) * 100000 + x * 1000, modulo[1] / len(stations) * 100000 + y * 1000
    # x, y = convert_to_lonlat(x, y)
    return x, y, z, t


def convert_to_xy(lon: float, lat: float) -> tuple:
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y


def convert_to_lonlat(x: float, y: float) -> tuple:
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lon, lat


def eq(p, args):
    v, x1, y1, z1, t1, x2, y2, z2, t2, x3, y3, z3, t3, x4, y4, z4, t4 = args
    x, y, z, t0 = p
    return (
        t1 - t0 - (1 / v) * ((x1 - x)**2 + (y1 - y)**2 + (z1 - z)**2)**0.5,
        t2 - t0 - (1 / v) * ((x2 - x)**2 + (y2 - y)**2 + (z2 - z)**2)**0.5,
        t3 - t0 - (1 / v) * ((x3 - x)**2 + (y3 - y)**2 + (z3 - z)**2)**0.5,
        t4 - t0 - (1 / v) * ((x4 - x)**2 + (y4 - y)**2 + (z4 - z)**2)**0.5
    )


def find_hypocenter(args):
    x, y, z, t0 = fsolve(eq, (0, 0, 0, 0), args=args)
    return x, y, z, t0
