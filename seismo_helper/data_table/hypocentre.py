import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.optimize import Bounds


def hypocentre_search(stations: list[list]) -> scipy.optimize:
    velocity = 5000
    sts = []
    for x, y, z, t in stations:
        y, x = converting_geographic_coordinates(y, x)
        sts.append([x % 100000, y % 100000, z, t])
    func = lambda x: sum(
        (st[3] - (x[3] + 1 / velocity * ((st[0] - x[0]) ** 2 + (st[1] - x[1]) ** 2 + (st[2] - x[2]) ** 2) ** 0.5)) ** 2
        for st in sts)
    # bound = Bounds([-np.inf, -np.inf, -np.inf, np.array(sts)[:, 3].mean() - 20],
    #                [np.inf, np.inf, np.inf, np.array(sts)[:, 3].mean() + 20])
    res = scipy.optimize.minimize(
        func, np.array([1000, 1000, 10, 40]),
        method='TNC',
        options={'maxiter': 100000, 'disp': True},
        # bounds=bound,
        tol=10e-10)
    return res


def converting_geographic_coordinates(d_lon: float, d_lat: float) -> tuple:
    zone = int(d_lon // 6.0 + 1)

    from math import sin, cos, tan, pi

    # Параметры эллипсоида Красовского
    a = 6378245.0  # Большая (экваториальная) полуось
    b = 6356863.019  # Малая (полярная) полуось
    e2 = (a ** 2 - b ** 2) / a ** 2  # Эксцентриситет
    n = (a - b) / (a + b)  # Приплюснутость

    # Параметры зоны Гаусса-Крюгера
    F = 1.0  # Масштабный коэффициент
    Lat0 = 0.0  # Начальная параллель (в радианах)
    Lon0 = (zone * 6 - 3) * pi / 180  # Центральный меридиан (в радианах)
    N0 = 0.0  # Условное северное смещение для начальной параллели
    E0 = zone * 1e6 + 500000.0  # Условное восточное смещение для центрального меридиана

    # Перевод широты и долготы в радианы
    Lat = d_lat * pi / 180.0
    Lon = d_lon * pi / 180.0

    # Вычисление переменных для преобразования
    v = a * F * (1 - e2 * (sin(Lat) ** 2)) ** -0.5
    p = a * F * (1 - e2) * (1 - e2 * (sin(Lat) ** 2)) ** -1.5
    n2 = v / p - 1
    M1 = (1 + n + 5.0 / 4.0 * n ** 2 + 5.0 / 4.0 * n ** 3) * (Lat - Lat0)
    M2 = (3 * n + 3 * n ** 2 + 21.0 / 8.0 * n ** 3) * sin(Lat - Lat0) * cos(Lat + Lat0)
    M3 = (15.0 / 8.0 * n ** 2 + 15.0 / 8.0 * n ** 3) * sin(2 * (Lat - Lat0)) * cos(2 * (Lat + Lat0))
    M4 = 35.0 / 24.0 * n ** 3 * sin(3 * (Lat - Lat0)) * cos(3 * (Lat + Lat0))
    M = b * F * (M1 - M2 + M3 - M4)
    I = M + N0
    II = v / 2 * sin(Lat) * cos(Lat)
    III = v / 24 * sin(Lat) * (cos(Lat)) ** 3 * (5 - (tan(Lat) ** 2) + 9 * n2)
    IIIA = v / 720 * sin(Lat) * (cos(Lat) ** 5) * (61 - 58 * (tan(Lat) ** 2) + (tan(Lat) ** 4))
    IV = v * cos(Lat)
    V = v / 6 * (cos(Lat) ** 3) * (v / p - (tan(Lat) ** 2))
    VI = v / 120 * (cos(Lat) ** 5) * (5 - 18 * (tan(Lat) ** 2) + (tan(Lat) ** 4) + 14 * n2 - 58 * (tan(Lat) ** 2) * n2)

    # Вычисление северного и восточного смещения (в метрах)
    N = I + II * (Lon - Lon0) ** 2 + III * (Lon - Lon0) ** 4 + IIIA * (Lon - Lon0) ** 6
    E = E0 + IV * (Lon - Lon0) + V * (Lon - Lon0) ** 3 + VI * (Lon - Lon0) ** 5

    return N, E


def perebor():
    t = lambda t0, velocity, x, x0, y, y0, z, z0: t0 + 1 / velocity * (
            (x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2) ** 0.5
    st1 = 51.34, 53.15, 84, 655.350
    st2 = 51.38, 53.19, 75, 655.002
    st3 = 51.29, 53.20, 80, 655.097
    velocity = 5000
    M = np.zeros((100, 100, 50, 100))
    xs0 = np.linspace(-100000, 400000, 100, False)
    ys0 = np.linspace(-100000, 400000, 100, False)
    zs0 = np.linspace(-10000, 10000, 50, False)
    ts0 = np.linspace(-10000, 4000, 100, False)
    for i in range(100):
        x0 = xs0[i]
        for j in range(100):
            y0 = ys0[j]
            for k in range(50):
                z0 = zs0[k]
                for l in range(100):
                    t0 = ts0[l]
                    T = 0
                    for x, y, z, T_obs in [st1, st2, st3]:
                        y, x = converting_geographic_coordinates(y, x)
                        x, dx, y, dy = x % 100000, x // 100000, y % 100000, y // 100000
                        # print(x, y)
                        T += (T_obs - t(t0, velocity, x, x0, y, y0, z, z0)) ** 2
                    M[i, j, k, l] = T
        print(T, x0, y0, z0, t0)
    # print(M)
    np.save(f'hypoc/M', M)
    np.save(f'hypoc/xs0', xs0)
    np.save(f'hypoc/ys0', ys0)
    np.save(f'hypoc/zs0', zs0)
    np.save(f'hypoc/ts0', ts0)

    # 3.8911462503877146 9451 2480 573 653
    # 14.269840605996908 8091 8673 91 656
    # 3.768981339955314 7847 8313 93 655


def drawing():
    path = f'hypoc/7/'
    xs0 = np.load(f'{path}xs0.npy')
    ys0 = np.load(f'{path}ys0.npy')
    zs0 = np.load(f'{path}zs0.npy')
    ts0 = np.load(f'{path}ts0.npy')
    M = np.load(f'{path}M.npy')
    fig, axs = plt.subplots(2, 3, figsize=(15, 9))
    tt = [3.086e+03, 4.693e+03, 1.000e+01, 6.352e+02]
    fig.colorbar(axs[0, 0].contourf(ts0, zs0, M[0, 0], levels=50))
    axs[0, 0].scatter(tt[3], tt[2])
    axs[0, 0].set_xlabel('t')
    axs[0, 0].set_ylabel('z')

    fig.colorbar(axs[0, 1].contourf(ts0, ys0, M[0, :, 0], levels=50))
    axs[0, 1].scatter(tt[3], tt[1])
    axs[0, 1].set_xlabel('t')
    axs[0, 1].set_ylabel('y')

    fig.colorbar(axs[0, 2].contourf(zs0, ys0, M[0, :, :, 80], levels=50))
    axs[0, 2].scatter(tt[2], tt[1])
    axs[0, 2].set_xlabel('z')
    axs[0, 2].set_ylabel('y')

    fig.colorbar(axs[1, 0].contourf(ts0, xs0, M[:, 0, 0], levels=50))
    axs[1, 0].scatter(tt[3], tt[0])
    axs[1, 0].set_xlabel('t')
    axs[1, 0].set_ylabel('x')

    fig.colorbar(axs[1, 1].contourf(zs0, xs0, M[:, 0, :, 80], levels=50))
    axs[1, 1].scatter(tt[2], tt[0])
    axs[1, 1].set_xlabel('z')
    axs[1, 1].set_ylabel('x')

    fig.colorbar(axs[1, 2].contourf(ys0, xs0, M[:, :, 0, 80], levels=50))
    axs[1, 2].scatter(tt[1], tt[0])
    axs[1, 2].set_xlabel('y')
    axs[1, 2].set_ylabel('x')
    fig.tight_layout()
    plt.show()
    # plt.savefig('draw_data/20191202 18.png')


# perebor()
# drawing()
# print(hypocentre_search())
