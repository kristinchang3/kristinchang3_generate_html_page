import os

from matplotlib import pyplot as plt

from ARMP.io.input import extract_dict, read_json_file
from ARMP.lib.control import iter_list
from ARMP.lib.loader import dic
from ARMP.utils.graphics_utils import minmax_range
from ARMP.utils.portrait_plot import metric_plot


def metric_plot_character(
    matrix,
    xaxis_labels,
    yaxis_labels,
    cbar_label,
    title,
    fig_filename,
    fig_dir,
    pvalue=None,
):
    minvalue, maxvalue = minmax_range(matrix)

    text_color_upper = maxvalue * 0.63
    text_color_lower = minvalue * 0.63

    fig = plt.figure(figsize=([8.5, 8.5]))

    fig, ax, im, cbar = metric_plot(
        matrix,
        fig=fig,
        xaxis_labels=xaxis_labels,
        yaxis_labels=yaxis_labels,
        annotate=True,
        annotate_format="{x:.2f}",
        annotate_textcolors_threshold=(text_color_lower, text_color_upper),
        annotate_fontsize=20,
        cmap="RdBu_r",
        cbar_label=cbar_label,
        vrange=(minvalue, maxvalue),
        # cbar_label_fontsize = 19,
        # cbar_tick_fontsize = 17,
        # xaxis_fontsize=26,
        # yaxis_fontsize=25,
        box_as_square=True,
    )

    ax.set_title(title, fontsize=20, color="black")

    # ax.axvline(x=2, color='k', linewidth = 3)

    plt.tight_layout()

    # plt.subplots_adjust(left=0.2, right=0.95, top=0.75, bottom=0.03)

    plt.savefig(os.path.join(fig_dir, fig_filename, ".png"), dpi=300)

    plt.close()


if __name__ == "__main__":
    field_list = ["lat", "lon", "area", "width", "length"]

    # set metrics for plotting
    model_list = dic["model_lsit"][1]
    ARDT_list = dic["ARDT_lsit"][0]
    region_list = dic["region_lsit"]
    season_list = dic["season_lsit"][0]

    model_ref = dic["model_lsit"][0]

    instance = model_list
    instance_ref = model_ref

    metric = "metric_character"
    metric_layout = list([model_list, ARDT_list, region_list, season_list])
    metric_var = "bias_norm"
    metric_sig = "zscore"

    # load metrics value
    dict_in = read_json_file(dic, metric)
    metric_dict_array = extract_dict(dict_in["RESULTS"], metric_layout, None)

    matrix = np.empty((metric_dict_array.shape[0], len(field_list)))
    matrix_pvalue = matrix.copy()

    # read in AR characteristics metrics
    for i, metric_item in enumerate(metric_dict_array):
        for j, character in enumerate(field_list):
            matrix[i][j] = metric_item[character][metric_var]
            matrix_pvalue[i][j] = metric_item[character][metric_sig]

    # format and rotate metrics matrix if necessary
    # matrix = matrix.T.astype(int)

    # metric plot setting
    xaxis_labels = field_list
    yaxis_labels = region_list

    fig_dir = dic["dir_fig"]
    cbar_label = "normalized bias"
    title = "{} - {}".format(instance, instance_ref)
    fig_filename = "character_bias_{instance}"

    metric_plot_character(
        matrix,
        xaxis_labels,
        yaxis_labels,
        cbar_label,
        title,
        fig_filename,
        fig_dir,
        pvalue=matrix_pvalue,
    )
