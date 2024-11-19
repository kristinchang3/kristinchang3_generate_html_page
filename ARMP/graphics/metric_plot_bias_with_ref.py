import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import transforms
from matplotlib.colors import ListedColormap

from ARMP.io.input import extract_dict, flatten_layout, read_json_file
from ARMP.lib.loader import dic

# plotting template for Fig.10 and Fig.11 in Dong et al. (2024)


def metrics_plot_bias_with_ref(
    matrix,
    metric_value,
    xaxis_labels,
    yaxis_labels,
    cbar_label,
    title,
    fig_filename,
    fig_dir,
):
    # user defined white only colormap
    custom_cmap = ListedColormap(["white", "white"])

    maxvalue = np.max(metric_value)
    minvalue = np.min(metric_value)
    maxvalue = max(maxvalue, minvalue * -1)
    minvalue = maxvalue * -1

    # threshold for flipping over text color
    text_color_upper = maxvalue * 0.57
    text_color_lower = maxvalue * -0.57

    fig, ax = plt.subplots(figsize=(8, 8))

    plt.pcolormesh(
        xaxis_labels[0],
        yaxis_labels,
        matrix[:, 0].reshape(len(yaxis_labels), -1),
        cmap=custom_cmap,
    )
    plt.pcolormesh(
        xaxis_labels[1:],
        yaxis_labels,
        matrix[:, 1:],
        cmap="RdBu",
        vmin=minvalue,
        vmax=maxvalue,
    )

    ax.set_xticks(
        np.arange(len(xaxis_labels)), labels=xaxis_labels, minor=False
    )  # set xaxis labels
    ax.tick_params(
        top=True, labeltop=True, bottom=False, labelbottom=False
    )  # move xaxis labels to the top
    plt.setp(
        ax.get_xticklabels(), rotation=30, ha="left", rotation_mode="anchor"
    )  # matrix and orient xaxis labels

    ax.set_yticks(np.arange(len(yaxis_labels)), labels=yaxis_labels)  # set yaxis labels

    # Minor ticks
    ax.set_xticks(np.arange(-0.5, matrix.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, matrix.shape[0], 1), minor=True)
    ax.grid(
        which="minor", color="black", linewidth=0.5
    )  # create grid lines based off of ticks
    ax.tick_params(which="minor", bottom=False, left=False)  # Remove minor ticks

    ## add hatch pattern where data falls within certain range
    # pattern = '///'
    # hatch_above = -5
    # hatch_below = 5
    #
    ## create a transparent layer with the pattern
    # hatch = ax.pcolor((np.arange(matrix[:,1:].shape[1])),
    #          (np.arange(matrix[:,1:].shape[0])),
    #          np.where((matrix[:,1:] >= hatch_above) & (matrix[:,1:]< hatch_below), matrix[:,1:], np.nan),
    #          alpha=0,
    #          hatch=pattern,
    #          ec='none',
    #          lw=1
    #          )
    ## add the transform
    # hatch.set_transform(trans + hatch.get_transform())

    # define own transform to set overlay at correct data coords
    x_shift = 1
    y_shift = 0
    transforms.Affine2D().translate(x_shift, y_shift)

    # Loop over data dimensions and create text annotation
    for i in range(len(yaxis_labels)):
        for j in range(len(xaxis_labels)):
            if j > 0 and matrix[i, j] > text_color_upper:
                ax.text(j, i, matrix[i, j], ha="center", va="center", color="w")
            elif j > 0 and matrix[i, j] < text_color_lower:
                ax.text(j, i, matrix[i, j], ha="center", va="center", color="w")
            else:
                ax.text(j, i, matrix[i, j], ha="center", va="center", color="black")

    # create square cells
    ax.set_aspect(1)

    # add a separation line between ref data and model data
    ax.axvline(x=0.5, color="k", linewidth=3)

    ax.set_title(title, fontsize=20, color="black")

    # add colorbar
    plt.colorbar().set_label(cbar_label, rotation=270, labelpad=10)

    plt.gca().invert_yaxis()
    fig.tight_layout()

    plt.savefig(os.path.join(fig_dir, fig_filename) + ".png", dpi=300)

    plt.close()


if __name__ == "__main__":
    # set metrics for plotting
    model_list = dic["model_list"][1:]
    ARDT_list = dic["ARDT_list"][0]
    region_list = dic["region_list"]
    season_list = dic["season_list"][0]

    metric_layout = flatten_layout([model_list, ARDT_list, region_list, season_list])
    metric_var = "freq_bias"
    metric = "metric_freq_bias"

    # load metrics value
    dict_in = read_json_file(dic, metric)
    metric_value = extract_dict(dict_in["RESULTS"], metric_layout, metric_var)

    # retrieve ref var_stats
    var_stats = "freq"
    model_ref = dic["model_list"][0]
    ref_layout = flatten_layout([model_ref, ARDT_list, region_list, season_list])
    ref_value = extract_dict(dict_in["REF"], ref_layout, var_stats)

    # merge ref and metrics results into one matrix
    ref_value = ref_value.reshape(len([model_ref]), len(region_list))
    metric_merge = np.vstack((ref_value, metric_value))

    # format and rotate metrics matrix if necessary
    matrix = metric_merge.T.astype(int)

    # metric plot setting
    xaxis_labels = [model_ref] + model_list
    yaxis_labels = region_list

    fig_dir = dic["dir_fig"]
    cbar_label = "AR frequency bias (%)"
    title = "landfalling AR frequency bias"
    fig_filename = "AR_freq_bias"

    metrics_plot_bias_with_ref(
        matrix,
        metric_value,
        xaxis_labels,
        yaxis_labels,
        cbar_label,
        title,
        fig_filename,
        fig_dir,
    )
