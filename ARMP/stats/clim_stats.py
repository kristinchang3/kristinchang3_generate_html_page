import numpy as np


def Clim_stats(clim_reg_ts):

    clim_mean = clim_reg_ts.mean(dim='time')

    return clim_mean

