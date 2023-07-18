import numpy as np
import scipy
from scipy.optimize import Bounds


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

    res = scipy.optimize.basinhopping(
        func, np.array([10000, 10000, 100, 40]),
        niter=10000,
        minimizer_kwargs={'method': 'BFGS'},
        disp=False)
    x, y, z, t = res.x
    x, y = coordinate_shift[0] * 100000 + x, coordinate_shift[1] * 100000 + y
    x, y = convert_to_lonlat(x, y)
    print("FINISHED HYPO")
    return x, y, z, t


def convert_to_xy(lon: float, lat: float) -> tuple:
    from pyproj import Transformer
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y


def convert_to_lonlat(x: float, y: float) -> tuple:
    from pyproj import Transformer
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lon, lat
