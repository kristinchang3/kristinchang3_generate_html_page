from ARMP.app.clim_analysis import Clim_analysis
from ARMP.app.clim_metrics_bias import Clim_metrics_bias
from ARMP.lib.loader import dic, setting

# ##import ARMP


def run_ARMP_clim(var_stats="mean", dic=dic, setting=setting):
    if not dic["include_clim"]:
        raise NameError("climate variable NOT set in config")

    print("\nstarting to calculate metrics for AR related climate variables")

    # process climate data
    Clim_analysis(dic, setting)

    # calculate climate metrics
    Clim_metrics_bias(dic, "metric_clim", var_stats)

    print("\nARMP_clim done!")


# --------------------------
if __name__ == "__main__":
    run_ARMP_clim("mean")
