import numpy as np

def LFAR_mthly_ts(da_occur_ts):

    occur_ts_rsp = da_occur_ts.resample(time='1M')

    occur_ts_mthly = occur_ts_rsp.sum()
    #occur_ts_mthly = occur_ts_mthly.dropna(dim='time', how='all') # for non-annual data!!!

    return occur_ts_mthly


def peak_day_fft(clim_mean):

    yf = np.fft.fft(clim_mean)

    peak = -np.arctan2(yf[1].imag, yf[1].real)*365/(2*np.pi)+(365/12/2)
    peak = int(peak)
    peak = peak+365 if peak < 0 else peak

    return peak



def peak_day_stats(da_occur_ts, dic):

    occur_ts_mthly = LFAR_mthly_ts(da_occur_ts)

    occur_ts_grp = occur_ts_mthly.groupby('time.month')

    if len(occur_ts_grp) != 12:
        raise Exception('12 months of climatology data is not complete')

    clim_mean = occur_ts_grp.mean(dim='time')

    peak = peak_day_fft(clim_mean)

    if not dic['diag_peak_day_histogram']:
        return peak
    
    else:

    clim_std = occur_ts_grp.std(dim='time')
    clim = [list(occur_ts_grp)[k][1].values for k in range(len(occur_ts_grp))] # clim[k] are dots in histogram

    return peak, clim_mean, clim_std, clim

