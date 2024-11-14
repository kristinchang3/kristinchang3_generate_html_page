#
#
#        ds_spatial_count_m = xr.open_mfdataset(fig_dir+"_"+model+"_"+region+"_spatial_count_m.nc")
#        ds_spatial_count = xr.open_mfdataset(fig_dir+"_"+model+"_"+region+"_spatial_count.nc")
#        ds_spatial_count_m_frequency = xr.open_mfdataset(fig_dir+"_"+model+"_"+region+"_spatial_count_m_frequency.nc")
#        ds_spatial_count_frequency = xr.open_mfdataset(fig_dir+"_"+model+"_"+region+"_spatial_count_frequency.nc")
#
#        spatial_count_m = ds_spatial_count_m.binary_tag
#        spatial_count = ds_spatial_count.binary_tag
#        spatial_count_m_frequency = ds_spatial_count_m_frequency.binary_tag
#        spatial_count_frequency = ds_spatial_count_frequency.binary_tag
#
#
#        ds_spatial_count_frequency = ds_spatial_count_frequency.bounds.add_missing_bounds()
#        ds_spatial_count_m_frequency = ds_spatial_count_m_frequency.bounds.add_missing_bounds()
#        spatial_count_CMIP_res_ds = ds_spatial_count_frequency.regridder.horizontal("binary_tag", ds_spatial_count_m_frequency, tool='regrid2').compute()
#        spatial_count_frequency_diff = spatial_count_m_frequency - spatial_count_CMIP_res_ds.binary_tag
#
#
#        level1 = np.linspace(0, 0.4,11)
#
#        maxvalue = np.max(spatial_count_frequency_diff)
#        minvalue = np.min(spatial_count_frequency_diff)
#        vlim = max(abs(maxvalue), abs(minvalue))#*0.85
#
#
#        level2 = np.linspace(vlim*-1, vlim, num=11)
#        level2 = np.linspace(vlim*-1, vlim, num=11)
#
#
#        projection0=ccrs.PlateCarree()
#        projection=ccrs.PlateCarree(central_longitude=180)
#        
#        if region in ['NPacific','SPacific']:
#            projection = projection
#        else:
#            projection = projection0
#
#
#        fig = plt.figure(figsize =([5, 10]))
#
#        gs = fig.add_gridspec(2, 5)
#        gs.update(wspace = 0.5, hspace = 0.2)
#
#
#        lon = spatial_count_m.coords['lon']
#        lat = spatial_count_m.coords['lat']
#
#
#        ax1 = fig.add_subplot(311, projection=projection)
#        ax1.coastlines()
#        ax1.set_title( model[6:] + ' AR frequency')
#        ax1.set_extent([np.min(spatial_count_m.lon),np.max(spatial_count_m.lon),np.min(spatial_count_m.lat),np.max(spatial_count_m.lat)],projection0)
#        cmap = plt.get_cmap('rainbow')
#        norm = mcolors.BoundaryNorm(boundaries=level1, ncolors=cmap.N, clip=True) # ncolors=cmap.N,
#        PCM=ax1.pcolormesh(spatial_count_m.lon, spatial_count_m.lat, spatial_count_m_frequency, transform=projection0, cmap=cmap, norm=norm)
#
#
#
#        cbar_ax = fig.add_axes([0.275, 0.65, 0.475, 0.015])  # [left, bottom, width, height]
#        cbar = plt.colorbar(PCM, cax=cbar_ax, orientation='horizontal', pad=0.1,format="%.2f")
#
#        gl = ax1.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),linewidth=0)
#        gl.top_labels, gl.right_labels = False, False
#        gl.xlocator = mticker.FixedLocator(range(-180, 181, 30))
#        gl.xformatter, gl.yformatter = LongitudeFormatter(), LatitudeFormatter()
#        
#        ax1.text(0.95, 0.1, f'{chr(97 + 0 + label_offset)}', transform=ax1.transAxes, ha='right', va='bottom', fontsize=15)#, fontweight='bold')
#
#        plt.subplots_adjust(hspace=0.55)
#
#
#
#        ax2 = fig.add_subplot(312, projection=projection)
#        ax2.coastlines()
#        ax2.set_title('ERA5 AR frequency')
#        ax2.set_extent([np.min(spatial_count.lon),np.max(spatial_count.lon),np.min(spatial_count.lat),np.max(spatial_count.lat)],projection0)
#        PCM=ax2.contourf(spatial_count.lon, spatial_count.lat, spatial_count_frequency, transform=projection0, cmap="rainbow", levels=level1)
#        cbar = plt.colorbar(PCM, ax=ax2, orientation='horizontal', pad=0.1,format="%.2f")
#        cbar.remove()
#        
#        gl = ax2.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),linewidth=0)
#        gl.top_labels, gl.right_labels = False, False
#        gl.xlocator = mticker.FixedLocator(range(-180, 181, 30))
#        gl.xformatter, gl.yformatter = LongitudeFormatter(), LatitudeFormatter()
#        
#        ax2.text(0.95, 0.1, f'{chr(97 + 1 + label_offset)}', transform=ax2.transAxes, ha='right', va='bottom', fontsize=15)
#
#
#
#
#        ax3 = fig.add_subplot(313, projection=projection)
#        ax3.coastlines()
#        ax3.set_title('difference')
#        ax3.set_extent([np.min(spatial_count_m.lon),np.max(spatial_count_m.lon),np.min(spatial_count_m.lat),np.max(spatial_count_m.lat)],projection0)
#        PCM=ax3.contourf(spatial_count_m.lon, spatial_count_m.lat, spatial_count_frequency_diff, transform=projection0, cmap="bwr", levels=level2)
#
#
#
#
#        cbar_ax = fig.add_axes([0.275, 0.35, 0.475, 0.015])  # [left, bottom, width, height]
#        cbar = plt.colorbar(PCM, cax=cbar_ax, orientation='horizontal', pad=0.1,format="%.2f")
#
#
#        gl = ax3.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),linewidth=0)
#        gl.top_labels, gl.right_labels = False, False
#        gl.xlocator = mticker.FixedLocator(range(-180, 181, 30))
#        gl.xformatter, gl.yformatter = LongitudeFormatter(), LatitudeFormatter()
#
#        ax3.text(0.95, 0.1, f'{chr(97 + 2 + label_offset)}', transform=ax3.transAxes, ha='right', va='bottom', fontsize=15)
#
#
#plt.savefig(fig_dir+'fig_freq_'+model+'_'+region+'_land_xf.png', bbox_inches='tight', dpi=300)
