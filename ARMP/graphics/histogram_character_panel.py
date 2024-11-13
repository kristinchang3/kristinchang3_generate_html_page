from lib.loader import dic
from lib.control import iter_list
from lib.convention import lon_swap
from utils.portrait_plot import metric_plot
from utils.graphics_utils import minmax_range
from io.input import read_json_file, extract_dict
from matplotlib import pyplot as plt
from app.ar_character import load_blobstats
from io.printting import str_print
import os


def plot_hist3_panel(data_obs, data_model, data_model2, region, obs, model, model2, field, ax, fig_dir, nbins=10,
                     bin_min=None, bin_max=None,
                     logx=False, logy=False):
    
    if bin_min is None:
        bin_min = np.min( np.concatenate([data_obs.flatten(), data_model.flatten(), data_model2.flatten()]) )

    if bin_max is None:
        bin_max = np.max( np.concatenate([data_obs.flatten(), data_model.flatten(), data_model2.flatten()]) )

    if field == 'lon':
        if region in ['NAtlantic','SAtlantic']:
            data_obs = np.array([lon_swap(v) for v in data_obs])
            data_model = np.array([lon_swap(v) for v in data_model])
            data_model2 = np.array([lon_swap(v) for v in data_model2])

    _, bins, _ = plt.hist(data_obs, bins=nbins,range=(bin_min, bin_max))
    bins = np.round(bins).astype(int)
    logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
    
    if logx:
        bins = logbins
        ax.set_xscale('log')
    else:
        ax.set_xscale('linear')
        ax.set_xticks(bins[::2])

    if logy:
        ax.set_yscale('log')

    ax.hist(data_obs, bins=bins, edgecolor='k', color='tab:blue', label=obs, alpha=0.7, lw=0.5)
    ax.hist(data_model, bins=bins, edgecolor='tab:orange' ,label=model, lw=1.0, histtype='step')
    ax.hist(data_model2, bins=bins, edgecolor='tab:olive' ,label=model2, lw=1.0, histtype='step')

    ax.tick_params(axis='both', which='major', labelsize=7) 

    ax.legend(fontsize=4)
    ax.set_xlabel(field, fontsize=10)
    ax.set_ylabel('count', fontsize=10)
    ax.set_title(region, fontsize=9)


    return ax


def get_blobstats_field(model, ARDT, region, season, field_id)

		case_name = "{}_tag".format('_'.join([model, ARDT, region, season]))
        fn_in = os.path.join(dic['dir_out'], case_name, "_blobstats.txt")
		columns = load_blobstats(fn_in)

		field_data = columns[:, field_id]

		return field_data


if __name__ == "__main__":

    # set metrics for plotting
    model_ref = dic['model_lsit'][0]
    model1 = dic['model_lsit'][1]
    model2 = dic['model_lsit'][2]
    ARDT = dic['ARDT_lsit'][0]
    region = dic['region_lsit'][0]
    season = dic['season_lsit'][0]


    fig_dir = dic['dir_fig']
    fig_filename = f'character_histogram_{str_fn(region)}'

	fig = plt.figure(figsize=[8.5, 5.0])

	gs = gridspec.GridSpec(2, 6, figure=fig)
	gs.update(wspace=1.8, hspace=0.5)

	ax1 = fig.add_subplot(gs[0, :2])
	ax2 = fig.add_subplot(gs[0, 2:4])
	ax3 = fig.add_subplot(gs[0, 4:])
	ax4 = fig.add_subplot(gs[1, 1:3])
	ax5 = fig.add_subplot(gs[1, 3:5])
	ax6 = fig.add_subplot(gs[1, 5:6])
	ax6.set_visible(False)
	ax = [ax1, ax2, ax3, ax4, ax5, ax6]

    field_list = ['lat','lon','area','width','length']
	panel_label = ["(a)","(b)","(c)","(d)","(e)",""]
	unit_list = ['(°N)', '(°E)', '(km²)', '(°Great Circle)', '(°Great Circle)',""]
	
	for i, field in enumerate(field_list):
	
	    plot_logx = True if field == 'area' else False
	
	    data1 = get_blobstats_field(model1, ARDT, region, season, i)
	    data2 = get_blobstats_field(model2, ARDT, region, season, i)
	    data_ref = get_blobstats_field(model_ref, ARDT, region, season, i)
	
	    ax[i] = plot_hist3_panel(data_ref, data1, data2, region, model_ref, model1, model2, field, ax[i], fig_dir, logx=plot_logx)
	
	    ax[i].set_title(panel_label[i], fontsize=9)
	
		ax[i].set_xlabel(field_list[i] + unit_list[i], fontsize=10)
	

#	ax[0].set_xlabel(field_list[0] + ' (°N)', fontsize=10) # ($^\circ$C)
#	ax[1].set_xlabel(field_list[1] + ' (°E)', fontsize=10)
#	ax[2].set_xlabel(field_list[2] + ' (km²)', fontsize=10) # km\u00B2
#	ax[3].set_xlabel(field_list[3] + ' (°Great Circle)', fontsize=10)
#	ax[4].set_xlabel(field_list[4] + ' (°Great Circle)', fontsize=10)
	
	
	plt.suptitle(str_print(region))
	plt.savefig(os.path.join(fig_dir, fig_filename, '.png'), dpi=300)
