import numpy as np
import warnings

def safe_mean(arr):

    empty_slice = False

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        if isinstance(arr, xr.DataArray):
            mean_value = np.nanmean(arr.values)
        else:
            mean_value = np.nanmean(arr)

        for wi in w:
            if issubclass(wi.category, RuntimeWarning) and "empty slice" in str(wi.message):
                print("\nWARNING!!!!!!!   -  all nans")
                empty_slice = True
                return 0, empty_slice

        return mean_value, empty_slice


def sig_test(a, b):

    n_a = a.shape[0]
    n_b = b.shape[0]

    #mean_a = np.mean(a)
    #mean_b = np.mean(b)

    mean_a, empty_a = safe_mean(a)
    mean_b, empty_b = safe_mean(b)

    if empty_a or empty_b:
        return 0., 0., 1.

    bias = mean_a - mean_b

    std_a = np.std(a)
    std_b = np.std(b)

    t_statistic = (mean_a - mean_b) / np.sqrt((std_a**2 / n_a) + (std_b**2 / n_b))

    z_score = t_statistic

    # Compute degrees of freedom for each element (using a simplified formula for equal n_a and n_b)
    df = ( (std_a**2 / n_a + std_b**2 / n_b)**2 ) / ( ( (std_a**2 / n_a)**2 / (n_a - 1) ) + ( (std_b**2 / n_b)**2 / (n_b - 1) ) )

    # Compute the p-values
    p_value = 2 * (1 - stats.t.cdf(np.abs(t_statistic), df=df))

    # Compute the p-values for the z-test (if desired)
    p_value_z = 2 * (1 - stats.norm.cdf(np.abs(z_score)))

    return bias, z_score, p_value


