import numpy as np
from ARMP.lib.sampling import find_common_times


def iou(da1, da2):

    da1, da2 = find_common_times(da1, da2)

    intersection = da1 * da2
    union = da1 + da2

    iou = intersection.sum(dim='time')/union.sum(dim='time')

    return iou
