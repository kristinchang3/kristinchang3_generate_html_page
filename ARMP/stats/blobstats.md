AR characteristics stats are obtained after running BlobStats
This step is done offline, before calling app/ar_character.py and app/ar_metrics_character_bias.py
BlobStats will be integrated as part of the ARMP in future development

BlobStats installation
    https://github.com/ClimateGlobalChange/tempestextremes

documentation:
    https://climate.ucdavis.edu/tempestextremes.php

BlobStats python package
    https://anaconda.org/conda-forge/tempest-extremes

examples to run BlobStats

srun -n 32 $TE/BlobStats --in_list ERA5_stats_in_list.txt --out_file ERA5_stats_out_list.txt --out "centlat,centlon,area,wtpcawidth,wtpcalength" --var "binary_tag" --wtvar "_VECMAG(VIWVE,VIWVN)" --findblobs --latname latitude --lonname longitude

srun -n 32 $TE/BlobStats --in_list cmip6_BCC-CSM2-MR_stats_in_list.txt --out_file cmip6_BCC-CSM2-MR_stats_out_list.txt --out "centlat,centlon,area,wtpcawidth,wtpcalength" --var "binary_tag" --wtvar "_VECMAG(uhusavi,vhusavi)" --findblobs --latname lat --lonname lon

save file as case_name+"_blobstats.txt" before calling app/ar_character.py and app/ar_metrics_character_bias.py
