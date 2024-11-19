from ARMP.lib.loader import dic


def plot_diagnostic(dic=dic):
    if dic["diag_peak_day_histogram"]:
        # diagnostic plot for peak day histogram
        print("\ncustom and run graphics/histogram_peak_day.py")

    if dic["diag_character_histogram"]:
        # histogram for AR characteristics
        print("\ncustom and run graphics/histogram_character_panel.py")

    if dic["diag_freq_map"]:
        # diagnostic map for AR frequency
        print("\ncustom and run graphics/map_frequency.py")
