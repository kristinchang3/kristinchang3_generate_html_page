from driver_clim import run_ARMP_clim

from ARMP.app.ar_character import AR_character_stats_json
from ARMP.app.ar_frequency import AR_frequency
from ARMP.app.ar_metrics_bias import AR_metrics_bias
from ARMP.app.ar_metrics_character_bias import AR_character_bias
from ARMP.app.ar_metrics_spatial_correlation import AR_spatial_correlation
from ARMP.app.plot_diagnostic import plot_diagnostic
from ARMP.app.plot_metrics import plot_metrics
from ARMP.io.printting import print_armp
from ARMP.lib.loader import dic, setting

# ##import ARMP


def run_ARMP(dic, setting, var_stats="freq", ref=False):
    """
    set ref=True if inclduing reference data in the diagnostic plot
    """
    print_armp()

    # AR frequency/count analysis from tag files
    if not dic["restart"]:
        AR_frequency(dic, setting)

    # workflow on AR metrics
    if dic["metric_freq"]:
        # calculate AR frequency/count metrics
        AR_metrics_bias(dic, "metric_freq", var_stats)

    if dic["metric_peak_day"]:
        # calculate AR peak day metrics
        AR_metrics_bias(dic, "metric_peak_day", "peak_day")

    if dic["metric_character"]:
        # calculate AR characteristics metrics
        print("\nrun stats/blobstats.py")
        AR_character_stats_json(dic, "metric_character")
        AR_character_bias(dic, "metric_character")

    if dic["metric_spatial_corr"]:
        # calculate AR frequency spatial correlation metrics
        AR_spatial_correlation(dic, "metric_spatial_corr")

    if dic["metric_iou"]:
        # calculate IOU for specific case
        print("\nrun app/ar_iou.py with user defined cases")

    if dic["include_clim"]:
        # calculate climate metrics
        run_ARMP_clim(dic, setting, var_stats="mean")

    # make metrics and diagnostics plots
    if dic["make_plot"]:
        # make metrics plot
        plot_metrics(dic)

        # make diagnostics plot
        plot_diagnostic(dic)

    print("\nJob done!")


# --------------------------
if __name__ == "__main__":
    # print_armp()
    print("Job starts!")
    run_ARMP(dic, setting, var_stats="freq", ref=True)
