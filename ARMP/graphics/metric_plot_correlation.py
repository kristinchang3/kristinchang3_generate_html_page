import os

import matplotlib
#import matplotlib.ticker.FormatStrFormatter as FormatStrFormatter
from matplotlib.ticker import StrMethodFormatter
import numpy as np
from matplotlib import pyplot as plt

from ARMP.io.input import extract_dict, read_json_file, flatten_layout
from ARMP.lib.loader import dic
from ARMP.utils.portrait_plot import metric_plot


def metric_plot_correlation(
    matrix, xaxis_labels, yaxis_labels, cbar_label, title, fig_filename, fig_dir
):
    minvalue, maxvalue = 0.8, 1.0
    text_color_lower, text_color_upper = 0.8, 0.9

    fig = plt.figure(figsize=([8.5, 8.5]))

    fig, ax, im, cbar = metric_plot(
        matrix,
        fig=fig,
        xaxis_labels=xaxis_labels,
        yaxis_labels=yaxis_labels,
        annotate=True,
        annotate_format="{x:.2f}",
        annotate_textcolors_threshold=(text_color_lower, text_color_upper),
        annotate_fontsize=12,
        cmap="Oranges",
        cbar_label=cbar_label,
        vrange=(minvalue, maxvalue),
        cbar_label_fontsize=11,
        cbar_kw={"fraction": 0.03, "shrink": 1.0, "pad": 0.03},
        cbar_tick_fontsize=9,
        xaxis_fontsize=12,
        yaxis_fontsize=12,
        box_as_square=True,
    )

    ax.set_title(title, fontsize=17, color="black")

    # ax.axvline(x=2, color='k', linewidth = 3)
    # x = np.arange(matrix.shape[1] + 1)
    # y = np.arange(matrix.shape[0] + 1)
    # ax.pcolor(x, y, np.where((zscore >= -1.96) & (zscore < 1.96), matrix, np.nan), ec=None, lw=0.01, hatch='/////', alpha=0)

    #cbar.ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    cbar.ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))
    ax.grid(which="minor", color="k", linestyle="-", linewidth=0.01)
    im.set_clim(minvalue, maxvalue)
    for spine in ax.spines.values():
        spine.set_linewidth(1.1)
    ax.tick_params(width=0.5)

    plt.tight_layout()

    plt.subplots_adjust(left=0.2, right=0.95, top=0.75, bottom=0.03)

    plt.savefig(os.path.join(fig_dir, fig_filename) + ".png", dpi=300)

    plt.close()


if __name__ == "__main__":
    # set metrics for plotting
    model_list = dic["model_list"][1:]
    ARDT_list = dic["ARDT_list"][0]
    region_list = dic["region_list"]
    season_list = dic["season_list"][0]

    metric_layout = flatten_layout([model_list, ARDT_list, region_list, season_list])
    metric_var = "corr"
    # metric_sig = 'pvalue'
    metric = "metric_spatial_corr"

    # load metrics value
    dict_in = read_json_file(dic, metric)
    metric_value = extract_dict(dict_in["RESULTS"], metric_layout, metric_var)
    # metric_pvalue = extract_dict(dict_in['RESULTS'], metric_layout, metric_sig)

    # format and rotate metrics matrix if necessary
    if metric_value.shape == ():
        metric_value = np.array([[metric_value]])
    matrix = metric_value

    # metric plot setting
    xaxis_labels = region_list
    yaxis_labels = model_list

    fig_dir = dic["dir_fig"]
    cbar_label = "correlation"
    title = "AR spatial correlation"
    fig_filename = "AR_spatial_corr"

    # graphic settings
    matplotlib.rcParams["hatch.linewidth"] = 0.2
    float_formatter = "{:.2f}".format
    np.set_printoptions(formatter={"float_kind": float_formatter})

    metric_plot_correlation(
        matrix, xaxis_labels, yaxis_labels, cbar_label, title, fig_filename, fig_dir
    )
