import numpy as np
import scipy
from scipy.optimize import Bounds
from scipy.optimize import fsolve
from pyproj import Transformer

def hypocentre_search(stations: list[list]) -> scipy.optimize:
    velocity = 3000
    sts = []
    coordinate_shift = [0, 0]
    for x, y, z, t in stations:
        x, y = convert_to_xy(x, y)
        sts.append([x % 100000, y % 100000, z, t])
        coordinate_shift[0] += x // 100000
        coordinate_shift[1] += y // 100000
    coordinate_shift = [coordinate_shift[0] / len(stations), coordinate_shift[1] / len(stations)]

    func = lambda x: sum(
        [(st[3] - (x[3] + 1 / velocity * ((st[0] - x[0]) ** 2 + (st[1] - x[1]) ** 2 + (st[2] - x[2]) ** 2) ** 0.5)) ** 2
         for st in sts])

    # res = scipy.optimize.basinhopping(
    #     func, np.array([10000, 10000, 100, 40]),
    #     niter=10000,
    #     minimizer_kwargs={'method': 'BFGS'},
    #     disp=False)
    
    x, y, z, t = find_hypocenter([velocity, sts[0][0], sts[0][1], sts[0][2], sts[0][3],
                                  sts[1][0], sts[1][1], sts[1][2], sts[1][3],
                                  sts[2][0], sts[2][1], sts[2][2], sts[2][3],
                                  sts[3][0], sts[3][1], sts[3][2], sts[3][3],
                                  ])

    x, y = coordinate_shift[0] * 100000 + x, coordinate_shift[1] * 100000 + y
    x, y = convert_to_lonlat(x, y)

    S = 0
    n = 0
    
    print(x, y, z, t)
    print("FINISHED HYPO")
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
