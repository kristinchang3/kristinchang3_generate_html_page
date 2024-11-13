/pscratch/sd/d/dong12/metrics/package/panel_hist2_basin_character.py
/pscratch/sd/d/dong12/list/metrics_stats_list.txt
/pscratch/sd/d/dong12/ERA5_stats_out.txt

BlobStats installation
    https://github.com/ClimateGlobalChange/tempestextremes

documentation:
    https://climate.ucdavis.edu/tempestextremes.php

examples to run BlobStats

srun -n 32 $TE/BlobStats --in_list ERA5_stats_in_list.txt --out_file ERA5_stats_out_list.txt --out "centlat,centlon,area,wtpcawidth,wtpcalength" --var "binary_tag" --wtvar "_VECMAG(VIWVE,VIWVN)" --findblobs --latname latitude --lonname longitude

srun -n 32 $TE/BlobStats --in_list cmip6_BCC-CSM2-MR_stats_in_list.txt --out_file cmip6_BCC-CSM2-MR_stats_out_list.txt --out "centlat,centlon,area,wtpcawidth,wtpcalength" --var "binary_tag" --wtvar "_VECMAG(uhusavi,vhusavi)" --findblobs --latname lat --lonname lon



save file as case_name+"_blobstats.txt"
