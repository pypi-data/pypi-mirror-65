import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate


def circle_data(n, k):
    t = np.linspace(0, 2 * np.pi, n)
    X = np.vstack([np.cos(t), np.sin(t)]).T
    Y = np.repeat(np.arange(k), (n + k - 1) // k)[:n]
    return X, Y


def plot_linear(w, b, xmin, xmax, ymin, ymax, *args, **kwargs):
    if np.abs(w[1]) > np.abs(w[0]):
        y1 = -(b + w[0] * xmin) / w[1]
        y2 = -(b + w[0] * xmax) / w[1]
        plt.plot([xmin, xmax], [y1, y2], *args, **kwargs)
    else:
        x1 = -(b + w[1] * ymin) / w[0]
        x2 = -(b + w[1] * ymax) / w[0]
        plt.plot([x1, x2], [ymin, ymax], *args, **kwargs)


def apply_grid(f, fromx, tox, fromy, toy, resolution=100):
    ax = np.linspace(fromx, tox, resolution)
    ay = np.linspace(fromy, toy, resolution)
    x, y = np.meshgrid(ax, ay)
    data = np.vstack((x.reshape(-1), y.reshape(-1))).T
    z = f(data).reshape(x.shape)
    return (x, y, z)


def contour_fun(f, values, fromx, tox, fromy, toy, resolution=100, **opts):
    ax = np.linspace(fromx, tox, resolution)
    ay = np.linspace(fromy, toy, resolution)
    x, y = np.meshgrid(ax, ay)
    data = np.vstack((x.reshape(-1), y.reshape(-1))).T
    v = f(data).reshape(x.shape)
    return plt.contour(x, y, v, values, **opts)


def image_fun(f, fromx, tox, fromy, toy, resolution=100, **opts):
    ax = np.linspace(fromx, tox, resolution)
    ay = np.linspace(fromy, toy, resolution)
    x, y = np.meshgrid(ax, ay)
    data = np.vstack((x.reshape(-1), y.reshape(-1))).T
    v = f(data).reshape(x.shape)
    # return plt.contour(x, y, v, values, **opts)
    return plt.imshow(v, **opts)


def check_gradient(x, f, gf, eps=1e-5, toll=1e-4):
    g = gf(x)
    x1 = x + eps * g
    x2 = x - eps * g
    y1 = f(x1)
    y2 = f(x2)
    d = y1 - y2 - 2 * eps * (g ** 2).sum()
    if np.abs(d) >= toll:
        print(x)
        print(g)
        print(d)
    assert np.abs(d) < toll, "Wrong gradient approximation: %f" % d


def check_gradient2(x, f, gf, eps=1e-5):
    n = x.shape[0]
    d = np.empty_like(x)
    for i in range(n):
        x1 = x.copy()
        x1[i] += eps
        x2 = x.copy()
        x2[i] -= eps
        y1 = f(x1)
        y2 = f(x2)
        d[i] = y1 - y2 - 2 * eps
    print(d)
    assert np.abs(d) < 1000 * eps


def save_contour(c, filename, key=0, fmt="%f", k=5):
    """Save a matplotlib contour in a text file."""
    segs = c.collections[key].get_segments()
    m = max(s.shape[0] for s in segs)
    data = np.nan * np.ones((k * m - k + 1, 2 * len(segs)))
    for n, s in enumerate(segs):
        nx = s.shape[0]
        kx = k * nx - k + 1
        for i in (0, 1):
            ius = scipy.interpolate.InterpolatedUnivariateSpline(
                np.arange(nx), s[:, i])
            data[:kx, 2 * n + i] = ius(np.linspace(0, nx - 1, kx))
    np.savetxt(filename, data, fmt=fmt)
