from lib.loader import dic, setting
import run_ARMP_clim
from app.ar_frequency import AR_frequency
from app.ar_metrics_bias import AR_metrics_bias
from app.ar_character import AR_character_stats_json
from app.ar_metrics_character_bias import AR_character_bias
from app.ar_metrics_spatial_correlation import AR_spatial_correlation


def run_ARMP(dic, setting, var_stats='freq', ref=False):
    '''
    set ref=True if inclduing reference data in the diagnostic plot
    '''
    # AR frequency/count analysis from tag files
    if not dic['restart']:
        AR_frequency(dic, setting)

    # workflow on AR metrics
    if dic['metric_freq']:
        # calculate AR frequency/count metrics
        AR_metrics_bias(dic, 'metric_freq', var_stats)

    if dic['metric_peak_day']:
        # calculate AR peak day metrics
        AR_metrics_bias(dic, 'metric_peak_day', var_stats)

    if dic['metric_character']:
        # calculate AR characteristics metrics
        print("run stats/blobstats.py")
        AR_character_stats_json(dic, 'metric_character')
        AR_character_bias(dic, 'metric_character')

    if dic['metric_spatial_correlation']:
        # calculate AR frequency spatial correlation metrics
        AR_spatial_correlation(dic, 'metric_spatial_correlation')

    if dic['metric_IOU']:
        # calculate IOU for specific case
        print("run app/ar_iou.py with user defined cases")

    if dic['include_clim']:
        # calculate climate metrics
        run_ARMP_clim(dic, setting, var_stats='pr')

    # make metrics and diagnostics plots
    if dic['make_plot']:
        # make metrics plot
        plot_metrics(dic)

        # make diagnostics plot
        plot_diagnostic(dic)


# --------------------------
if __name__ == "__main__":
    run_ARMP(dic, setting, var_stats='freq', ref=True)

