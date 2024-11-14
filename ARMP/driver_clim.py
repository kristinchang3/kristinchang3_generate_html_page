from ARMP.lib.loader import dic, setting
from ARMP.app.clim_analysis import Clim_analysis
from ARMP.app.clim_metrics_bias import Clim_metrics_bias


def run_ARMP_clim(dic, setting, var_stats='mean'):

    if not dic['include_clim']:
        raise NameError("climate variable NOT set in config")
    
    # process climate data
    Clim_analysis(dic, setting)

    # calculate climate metrics
    Clim_metrics_bias(dic, 'metric_clim', var_stats)


# --------------------------
if __name__ == "__main__":
    run_ARMP_clim(dic, setting, var_stats='mean')
