from eofs.xarray import Eof


new_da_mthly = ds_tag_land.resample(time='1M').mean(dim='time', skipna=True)
da_tag = new_da_mthly.dropna(dim='time', how='all')




def Ne(da_tag):
    """
    effective sample size
    """
    coslat = np.cos(np.deg2rad(da_tag.coords['lat'].values))
    wgts = np.sqrt(coslat)[..., np.newaxis]
    solver = Eof(da_tag, weights=wgts)
    
    eof1 = solver.eofs(neofs=50)
    pc1 = solver.pcs(npcs=50, pcscaling=1)
    variance = solver.varianceFraction(neigs=50)
    total_variance = solver.totalAnomalyVariance()
    
    total_var = 0.
    for i, var in enumerate(variance):
        total_var += var
        if total_var >=0.95:
            print("i = ", i + 1)
            print("variance = ", var.values, " %")
            return i
            #break


# calculate p-value
def pvalue(dic, case_name, case_name_ref):

    dir_out = dic['dir_out']

    tag_reg_mpts = nc_in('tag', 'mpts.nc', case_name, dir_out)
    tag_reg_mpts_ref = nc_in('tag', 'mpts.nc', case_name_ref, dir_out)




    model = dic['model_list'][1]
    ARDT = dic['ARDT_list'][1]
    ARDT_ref = dic['ARDT_list'][0]
    region = dic['region_list'][0]
    season = dic['season_list'][0]

    case_name = "{}_tag".format('_'.join([model,ARDT,region,season]))
    case_name_ref = "{}_tag".format('_'.join([model,ARDT_ref,region,season]))

