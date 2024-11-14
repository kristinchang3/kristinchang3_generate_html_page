import matplotlib
import numpy as np
from matplotlib.colors import ListedColormap


def cyclic_cmap():
    top = matplotlib.colormaps["Blues_r"]
    bottom = matplotlib.colormaps["Blues"]

    newcolors = np.vstack((top(np.linspace(0, 1, 16)), bottom(np.linspace(0, 1, 16))))

    newcmp = ListedColormap(newcolors, name="cyclic0")

    return newcmp


def minmax_range(metric_value, scale_factor=1.0):
    maxvalue = np.max(metric_value)
    minvalue = np.min(metric_value)
    maxvalue = max(maxvalue, minvalue * -1) * scale_factor
    minvalue = maxvalue * -1

    return minvalue, maxvalue
