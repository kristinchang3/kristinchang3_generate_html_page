customize params/config.py for user defined case

prepare input files and file-pointer(as .txt file) required to run ARMP in data/ or $dir_in

a list of AR object/tag netcdf files are specified in
"{}_tag_list.txt".format(model, ARDT)

for climate variable analysis e.g., precipitation, 
a list of climate files need to be included in
"{}_{}_clim_list.txt".format(model, clim_var_name)


ARMP is driven by the driver*.py files
python driver_AR.py to run ARMP

if climate analysis is desired and the processed AR tag netcdf files are already in place, 
run driver_clim.py directly


code structure of ARMP:

stats/:
    statistics workflow for AR features and climate variables

metrics/:
    metric functions

app/:
    scirpts for calculating metrics

graphics/:
    plotting scripts, run offline after executing ARMP
