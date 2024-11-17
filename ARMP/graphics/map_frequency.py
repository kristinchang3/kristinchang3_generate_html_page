import xarray as xr
import numpy as np
import os
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from itertools import product
from ARMP.io.input import case_combi, nc_in
from ARMP.lib.control import iter_list_ref, make_case
from ARMP.lib.convention import Case
from ARMP.lib.spatial import match_coords_precision
from ARMP.utils.graphics_utils import minmax_range
from ARMP.io.printting import str_fn
from ARMP.lib.loader import dic


def map_frequency(dic, mp, mp_ref, model, model_ref, ARDT, region, season):

#    ds_mp = mp.to_dataset()
#    ds_mp.lat.attrs["axis"] = "Y"
#    ds_mp.lon.attrs["axis"] = "X"
#    ds_mp = ds_mp.bounds.add_missing_bounds()
#    ds_mp_regrid = ds_mp.regridder.horizontal("binary_tag", ds_mp_ref, tool='regrid2').compute()

    # regrid ------------
    mp = match_coords_precision(mp, mp_ref)

    mp_diff = mp - mp_ref
    
    level1 = np.linspace(0, 1.0 ,11)
    _, vlim = minmax_range(mp_diff)
    level2 = np.linspace(vlim*-1, vlim, num=11)
    
    projection0=ccrs.PlateCarree()
    projection=ccrs.PlateCarree(central_longitude=180)
    
    if region in ['NPacific','SPacific']:
        projection = projection
    else:
        projection = projection0
    
    
    fig = plt.figure(figsize = ([5, 10]))
    
    #gs = fig.add_gridspec(2, 5)
    #gs.update(wspace = 0.5, hspace = 0.2)
    
    label_offset = 0
    
    ### subplot 1
    ax1 = fig.add_subplot(311, projection=projection)
    #ax1 = plt.subplot(gs[0, 0:2], projection=projection)
    ax1.coastlines()
    ax1.set_title( f"{model} {ARDT} {season} AR frequency")
    ax1.set_extent([np.min(mp.lon),np.max(mp.lon),np.min(mp.lat),np.max(mp.lat)],projection)
    
    cmap = plt.get_cmap('rainbow')
    norm = mcolors.BoundaryNorm(boundaries=level1, ncolors=cmap.N, clip=True) # ncolors=cmap.N,
    PCM=ax1.pcolormesh(mp.lon, mp.lat, mp, transform=projection, cmap=cmap, norm=norm)
    
    cbar_ax = fig.add_axes([0.275, 0.65, 0.475, 0.015])  # [left, bottom, width, height]
    cbar = plt.colorbar(PCM, cax=cbar_ax, orientation='horizontal', pad=0.1,format="%.2f")
    
    gl = ax1.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),linewidth=0)
    gl.top_labels, gl.right_labels = False, False
    gl.xlocator = mticker.FixedLocator(range(-180, 181, 30))
    gl.xformatter, gl.yformatter = LongitudeFormatter(), LatitudeFormatter()
    
    ax1.text(0.95, 0.1, f'{chr(97 + 0 + label_offset)}', transform=ax1.transAxes, ha='right', va='bottom', fontsize=15)#, fontweight='bold')
    
    plt.subplots_adjust(hspace=0.55)
    
    
    
    ### subplot 2 
    ax2 = fig.add_subplot(312, projection=projection)
    #ax2 = plt.subplot(gs[0, 2:4], projection=projection)
    ax2.coastlines()
    ax2.set_title( f"{model_ref} {ARDT} {season} AR frequency")
    ax2.set_extent([np.min(mp_ref.lon),np.max(mp_ref.lon),np.min(mp_ref.lat),np.max(mp_ref.lat)],projection)
    
    PCM=ax2.contourf(mp_ref.lon, mp_ref.lat, mp_ref, transform=projection, cmap="rainbow", levels=level1)
    #cbar = plt.colorbar(PCM, ax=ax2, orientation='horizontal', pad=0.1,format="%.2f")
    #cbar.remove()
    
    gl = ax2.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),linewidth=0)
    gl.top_labels, gl.right_labels = False, False
    gl.xlocator = mticker.FixedLocator(range(-180, 181, 30))
    gl.xformatter, gl.yformatter = LongitudeFormatter(), LatitudeFormatter()
    
    ax2.text(0.95, 0.1, f'{chr(97 + 1 + label_offset)}', transform=ax2.transAxes, ha='right', va='bottom', fontsize=15)
    
    
    
    ### subplot 3 
    ax3 = fig.add_subplot(313, projection=projection)
    #ax3 = plt.subplot(gs[1, 1:3], projection=projection)
    ax3.coastlines()
    ax3.set_title('difference')
    ax3.set_extent([np.min(mp.lon),np.max(mp.lon),np.min(mp.lat),np.max(mp.lat)],projection)
    PCM=ax3.contourf(mp.lon, mp.lat, mp_diff, transform=projection, cmap="bwr", levels=level2)
    
    cbar_ax = fig.add_axes([0.275, 0.35, 0.475, 0.015])  # [left, bottom, width, height]
    cbar = plt.colorbar(PCM, cax=cbar_ax, orientation='horizontal', pad=0.1,format="%.2f")
    
    gl = ax3.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),linewidth=0)
    gl.top_labels, gl.right_labels = False, False
    gl.xlocator = mticker.FixedLocator(range(-180, 181, 30))
    gl.xformatter, gl.yformatter = LongitudeFormatter(), LatitudeFormatter()
    
    ax3.text(0.95, 0.1, f'{chr(97 + 2 + label_offset)}', transform=ax3.transAxes, ha='right', va='bottom', fontsize=15)


    #plt.tight_layout()

    fig_filename = 'map_freq_'+ model + "_" + str_fn(region) + "_" + ARDT + "_" + season
    plt.savefig(os.path.join(dic["dir_fig"], fig_filename) + ".png", bbox_inches='tight', dpi=300)

    plt.close()



def plot_map_frequency(dic):

    layout_pool, model_ref = iter_list_ref(dic)

    for combi in product(*layout_pool):
        case = make_case(Case, combi, dic)

        model = case.model
        ARDT = case.ARDT
        region = case.region
        season = case.season

        case_name = case.case_name
        case_name_ref = case_combi(case_name, model, model_ref)

        freq_reg_mp = nc_in("freq", "mp.nc", case_name, dic['dir_out'])
        freq_reg_mp_ref = nc_in("freq", "mp.nc", case_name_ref, dic['dir_out'])

        #freq_reg_mp.attrs['model'] = model
        #freq_reg_mp_ref.attrs['model_ref'] = model_ref


        map_frequency(dic, freq_reg_mp, freq_reg_mp_ref, model, model_ref, ARDT, region, season)



if __name__ == "__main__":
    plot_map_frequency(dic)
