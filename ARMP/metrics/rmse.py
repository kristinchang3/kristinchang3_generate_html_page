import numpy as np
from scipy.ndimage import label


def rmse(y1, y2):
    return np.sqrt(((y1 - y2) ** 2).mean())


# below two functions in metrics/CMIP_basin_frequency_auto.py
def label_clusters(data):
    labeled_data, num_clusters = label(data)
    return labeled_data, num_clusters


def count_unique_numbers(data):
    unique_numbers = np.unique(data[data > 0])
    count = len(unique_numbers)
    return count, unique_numbers
