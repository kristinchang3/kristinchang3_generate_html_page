import os

import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from ARMP.io.input import extract_dict, read_json_file
from ARMP.lib.loader import dic
from ARMP.utils.graphics_utils import minmax_range
from ARMP.utils.portrait_plot import metric_plot


def extract_field_dict(dict_in, metric_layout, field_list):
    metric_dict_array = extract_dict(dict_in["RESULTS"], metric_layout, None)

    matrix = np.empty((metric_dict_array.shape[0], len(field_list)))
    matrix_pvalue = matrix.copy()

    # read in AR characteristics metrics
    for i, metric_item in enumerate(metric_dict_array):
        for j, character in enumerate(field_list):
            matrix[i][j] = metric_item[character][metric_var]
            matrix_pvalue[i][j] = metric_item[character][metric_sig]

    return matrix, matrix_pvalue


def metric_plot_character_panel(
    dict_in,
    model_list,
    ARDT_list,
    region_list,
    season_list,
    field_list,
    xaxis_labels,
    yaxis_labels,
    cbar_label,
    title,
    fig_filename,
    fig_dir,
):
    matplotlib.rcParams["hatch.linewidth"] = 0.2

    nrows = 1
    ncols = 5

    panel_label = ["(a)", "(b)", "(c)", "(d)", "(e)", ""]

    metric_layout = list([model_list, ARDT_list, region_list[0], season_list])
    matrix, zscore = extract_field_dict(dict_in, metric_layout, field_list)

    minvalue, maxvalue = minmax_range(matrix)

    # text_color_upper, text_color_lower = [value * 0.57 for value in (maxvalue, minvalue)]
    text_color_upper = maxvalue * 0.57
    text_color_lower = minvalue * 0.57

    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 5))

    for i, region in enumerate(region_list[:]):
        metric_layout = list([model_list, ARDT_list, region, season_list])
        matrix, zscore = extract_field_dict(dict_in, metric_layout, field_list)

        if i < 5:
            colorbar_off = True
        else:
            colorbar_off = False

        if i > 0:
            yaxis_labels = []

        fig, ax[i], im = metric_plot(
            matrix,
            fig=fig,
            ax=ax[i],
            xaxis_labels=xaxis_labels,
            yaxis_labels=yaxis_labels,
            annotate=True,
            annotate_fontsize=5,
            annotate_format="{x:.1f}",
            annotate_textcolors_threshold=(text_color_lower, text_color_upper),
            vrange=(minvalue, maxvalue),
            colorbar_off=colorbar_off,
            cbar_label="normalized bias (Z-score)",
            cbar_label_fontsize=6,
            cbar_kw={"fraction": 0.075, "shrink": 1.7, "pad": 0.11},
            cbar_tick_fontsize=5,
            xaxis_fontsize=6,
            yaxis_fontsize=6,
            box_as_square=True,
            logo_off=True,
        )

        ax[i].set_title(panel_label[i] + "  " + region, fontsize=9, color="black")

        ax[i].grid(which="minor", color="k", linestyle="-", linewidth=0.005)

        x = np.arange(matrix.shape[1] + 1)
        y = np.arange(matrix.shape[0] + 1)
        ax[i].pcolor(
            x,
            y,
            np.where((zscore >= -1.96) & (zscore < 1.96), matrix, np.nan),
            ec=None,
            lw=0.01,
            hatch="/////",
            alpha=0,
        )

        im.set_clim(minvalue, maxvalue)

        im.set_linewidth(0.005)

        for spine in ax[i].spines.values():
            spine.set_linewidth(0.7)  # Set

        ax[i].tick_params(width=0.7, length=1)

    # left bottom width height
    cbar_ax = fig.add_axes([0.92, 0.25, 0.017, 0.49])
    cbar = fig.colorbar(
        im, cax=cbar_ax, orientation="vertical", fraction=0.017, pad=10.0
    )
    cbar.ax.tick_params(labelsize=5, width=0.5, length=1)
    cbar.outline.set_linewidth(0.5)

    plt.subplots_adjust(wspace=0.2, hspace=0.1)
    plt.savefig(os.path.join(fig_dir, fig_filename, ".png"), dpi=300)

    plt.close()


if __name__ == "__main__":
    field_list = ["lat", "lon", "area", "width", "length"]

    # set metrics for plotting
    model_list = dic["model_lsit"][1:]
    ARDT_list = dic["ARDT_lsit"][0]
    region_list = dic["region_lsit"]
    season_list = dic["season_lsit"][0]

    metric = "metric_character"
    # metric_var = 'bias_norm'
    metric_var = "zscore"
    metric_sig = "zscore"

    # load metrics value
    dict_in = read_json_file(dic, metric)

    # metric plot setting
    xaxis_labels = field_list
    yaxis_labels = model_list

    fig_dir = dic["dir_fig"]
    cbar_label = "normalized bias"
    title = ""
    fig_filename = "character_bias_basin_panel"

    metric_plot_character_panel(
        dict_in,
        model_list,
        ARDT_list,
        region_list,
        season_list,
        field_list,
        xaxis_labels,
        yaxis_labels,
        cbar_label,
        title,
        fig_filename,
        fig_dir,
    )
