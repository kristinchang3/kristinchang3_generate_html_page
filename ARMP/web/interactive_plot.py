import json
import math
import os
from pathlib import Path

import holoviews as hv
import hvplot.pandas
import matplotlib as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from bokeh.io import show
from bokeh.layouts import row
from bokeh.models import (
    ColorBar,
    ColumnDataSource,
    Grid,
    HoverTool,
    HTMLLabel,
    Label,
    LinearColorMapper,
    LogColorMapper,
    LogTicker,
    Rect,
)
from bokeh.palettes import RdBu, diverging_palette, interp_palette
from bokeh.plotting import figure
from matplotlib import pyplot as plt
from PIL import Image
from pylab import *

from ARMP.io.input import extract_dict, flatten_layout, read_json_file

hv.extension("bokeh")  # noqa


if __name__ == "__main__":
    #  metric plot layout
    model_list = [
        "BCC-CSM2-MR",
        "CanESM2",
        "CCSM4",
        "CSIRO-Mk3-6-0",
        "NorESM1-M",
        "MRI-ESM2-0",
        "IPSL-CM51-LR",
        "IPSL-CM5B-LR",
        "IPSLCM61-LR",
    ]
    ARDT_list = ["TE"]
    region_list = ["N Pacific", "S Pacific", "N Atlantic", "S Atlantic", "Indian Ocean"]
    season_list = ["annual"]

    ARDT = ARDT_list[0]
    season = season_list[0]

    # load metric data from metric json file
    base_dir = base_dir = Path(__file__).parent.parent
    web_data_dir = "doc/demo_data"
    web_dir = (base_dir / path_obj).resolve()

    metric_layout = flatten_layout([model_list, ARDT_list, region_list, season_list])
    metric_var = "corr"
    # metric_sig = 'pvalue'
    metric = "metric_spatial_corr"

    # dict_in = read_json_file(dic, metric)
    metric_fn = os.path.join(web_dir, "{}.json".format(metric))
    with open(metric_fn, "r") as json_file:
        dict_in = json.load(json_file)

    metric_value = extract_dict(dict_in["RESULTS"], metric_layout, metric_var)

    # set web URL for data and image
    # img_path = 'https://raw.githubusercontent.com/PCMDI/ARMP/main/ARMP/web/data'
    # img_path = 'https://raw.githubusercontent.com/PCMDI/ARMP/main/ARMP/metrics/'
    img_path = "https://raw.githubusercontent.com/PCMDI/ARMP/main"

    img_links = []

    # fomrat metric data
    da = pd.DataFrame(data=metric_value, index=model_list, columns=region_list)

    dd = da.stack()
    dd = dd.reset_index()
    dd = dd.rename(columns={"level_0": "model", "level_1": "region", 0: "correlation"})

    for i, model in enumerate(model_list):
        for j, region in enumerate(region_list):
            filename = (
                img_path
                + "map_freq_"
                + model
                + "_"
                + str_fn(region)
                + "_"
                + ARDT
                + "_"
                + season
                + ".png"
            )
            img_links.append(filename)

    dd["img"] = img_links

    # adjust pandas settings to view full column width
    pd.set_option("max_colwidth", 1000)

    # hover plot
    hover_L = HoverTool(
        tooltips="""
        <div>
            <div>
                <img src="@img" width=500 style="float: left; margin: 0px 15px 15px 0px; border="2"></img>
            </div>
        </div>

    """
    )

    hover_R = HoverTool(
        tooltips="""
        <div>
            <div>
                <img src="@img" width=500 style="float: right; margin: 0px 15px 15px 0px; border="2"></img>
            </div>
        </div>

    """
    )

    # Use full df shape to determine plot size
    num_models = len(dd["model"].unique())
    num_regions = len(dd["region"].unique())
    aspect_ratio = num_regions / num_models

    # Define hook function to adjust clabel position
    def adjust_clabel(plot, element):
        color_bar = plot.state.right[0]
        color_bar.title = ""  # removes default title
        color_bar.major_label_text_font_size = (
            "14pt"  # adjust font size of colorbar tick labels
        )
        # create a custom title
        label = HTMLLabel(
            x=100 * num_regions + 80,
            y=((100 * num_models) / 2) + 20,
            metric_value=-math.pi / 2,
            x_units="screen",
            y_units="screen",
            text="correlation",
            text_font_size="14pt",
            text_font_style="normal",
        )
        plot.state.add_layout(label)

    # metric plot
    spatial_corr = dd.hvplot.heatmap(
        y="model",
        x="region",
        C="correlation",
        frame_height=100 * num_models,
        aspect=aspect_ratio,
        xaxis="top",
        clim=(0.80, 1),
        cmap="oranges_r",
        line_color="gray",
        line_width=0.5,
        hover_cols="img",
        tools=[hover_R],
    ).opts(
        xrotation=45,
        fontsize={"labels": 14, "xticks": 14, "yticks": 14},
        colorbar=True,
    )

    # text annotation
    bins = [0.8, 0.9, 1]
    label_colors = ["white", "black"]
    spatial_corr = spatial_corr * hv.Labels(spatial_corr).opts(
        text_color="correlation", color_levels=bins, cmap=label_colors, xaxis="top"
    )

    spatial_corr_plot = spatial_corr.opts(hooks=[adjust_clabel])

    # save portrait plot to charts folder as an html file
    # change file name each time saving a new version
    # update index.md file to match new html file name

    # hvplot.save(spatial_corr_plot, 'charts/spatial_corr_plot_01.html')

    # push changes to github to see updates on live webpage
