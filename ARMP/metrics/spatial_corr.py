import math

import numpy as np
import scipy.stats as stats
from eofs.xarray import Eof
from scipy.stats import pearsonr

from ARMP.io.input import nc_in
from ARMP.lib.spatial import match_coords_precision
from ARMP.lib.temporal import dim_year_to_time, season_group


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
        if total_var >= 0.99999:
            # print("i = ", i + 1)
            # print("variance = ", var.values, " %")
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


def spatial_corr(
    mp,
    mp_ref,
    ne=False,
    mpts=None,
    season_month=None,
    fn_var_out=None,
    case_name=None,
    dir_out=None,
    **kwargs
):
    mp = match_coords_precision(mp, mp_ref)

    mp_1d = mp.to_numpy().flatten()
    mp_ref_1d = mp_ref.to_numpy().flatten()

    corr, pvalue = pearsonr(mp_1d, mp_ref_1d)

    if ne:
        mpts = nc_in(fn_var_out, "mpts.nc", case_name, dir_out)
        mpts_grp = season_group(mpts, season_month)
        mpts_grp = dim_year_to_time(mpts_grp)
        pvalue = calculate_pvalue(corr, mpts_grp)

    return corr, pvalue
