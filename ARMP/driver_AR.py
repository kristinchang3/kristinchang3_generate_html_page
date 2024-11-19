from driver_clim import run_ARMP_clim

from ARMP.app.ar_character import AR_character_stats_json
from ARMP.app.ar_frequency import AR_frequency
from ARMP.app.ar_metrics_bias import AR_metrics_bias
from ARMP.app.ar_metrics_character_bias import AR_character_bias
from ARMP.app.ar_metrics_spatial_correlation import AR_spatial_correlation
from ARMP.app.plot_diagnostic import plot_diagnostic
from ARMP.app.plot_metrics import plot_metrics
from ARMP.io.input import load_config
from ARMP.io.printting import print_armp
from ARMP.lib.loader import dic, setting

load_config(dic, globals())


def run_ARMP(var_stats="freq", ref=False, dic=dic, setting=setting):
    """
    set ref=True if inclduing reference data in the diagnostic plot
    """
    print_armp()

    # AR frequency/count analysis from tag files
    if not restart:  # noqa
        # AR_frequency(dic, setting)
        AR_frequency()

    # workflow on AR metrics
    if metric_freq:  # noqa
        # calculate AR frequency/count metrics
        AR_metrics_bias("metric_freq", "freq")

    if metric_peak_day:  # noqa
        # calculate AR peak day metrics
        AR_metrics_bias("metric_peak_day", "peak_day")

    if metric_character:  # noqa
        # calculate AR characteristics metrics
        print("\nrun stats/blobstats.py")
        AR_character_stats_json("metric_character")
        AR_character_bias("metric_character")

    if metric_spatial_corr:  # noqa
        # calculate AR frequency spatial correlation metrics
        AR_spatial_correlation("metric_spatial_corr")

    if metric_iou:  # noqa
        # calculate IOU for specific case
        print("\nrun app/ar_iou.py with user defined cases")

    if include_clim:  # noqa
        # calculate climate metrics
        run_ARMP_clim("mean")

    # make metrics and diagnostics plots
    if make_plot:  # noqa
        # make metrics plot
        plot_metrics()

        # make diagnostics plot
        plot_diagnostic()

    print("\nJob done!")


# --------------------------
if __name__ == "__main__":
    # print_armp()
    print("Job starts!")
    run_ARMP()
