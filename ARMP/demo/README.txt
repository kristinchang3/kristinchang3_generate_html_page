Input files required to run ARMP:

a list of AR object/tag files need to be included in
"{}_tag_list.txt".format(model, ARDT)

for climate variable analysism e.g., precipitation, 
a list of AR object/tag files need to be included in
"{}_{}_clim_list.txt".format(model, var_name)

run driver_AR.py in the package
if the processed AR tag netcdf files are already in place, 
run driver_clim.py directly


stats:
    include statistics workflow for AR features and cliamte variables

metrics:
    metric calculatioin

app:
    scirpts for calculating metrics

graphics:
    plotting scripts, run offline after executing ARMP
