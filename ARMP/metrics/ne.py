import numpy as np
from eofs.xarray import Eof
import scipy.stats as stats
import math


def Ne(da_grp):
    """
    effective sample size estimate as described in Dong et al. (2024)
    """
    coslat = np.cos(np.deg2rad(da_grp.coords["lat"].values))
    wgts = np.sqrt(coslat)[..., np.newaxis]
    solver = Eof(da_grp, weights=wgts)

    # eof1 = solver.eofs(neofs=50)
    # pc1 = solver.pcs(npcs=50, pcscaling=1)
    variance = solver.varianceFraction(neigs=50)
    # total_variance = solver.totalAnomalyVariance()

    total_var = 0.0
    for i, var in enumerate(variance):
        total_var += var
        if total_var >= 0.95:
            print("i = ", i + 1)
            print("variance = ", var.values, " %")
            return i
            # break


def calculate_pvalue(r, da_grp):
    """
    significance test for spatial correlation as described in Dong et al. (2024)
    """
    # effective sample size
    ne = Ne(da_grp)

    # Calculate the t-statistic
    t_stat = r * math.sqrt(ne - 2) / math.sqrt(1 - r**2)

    # Degrees of freedom for the t-distribution
    df = ne - 2

    # Calculate the p-value (two-tailed test)
    pvalue = 2 * (1 - stats.t.cdf(abs(t_stat), df))

    return pvalue

