# import glob

# Step 1: Create a list of .nc files
file_pattern = "path/to/your/files/*.nc"  # Adjust the path and pattern
file_list = glob.glob(file_pattern)

or

# Step 1: Read the list of .nc files from a .txt file
with open("path/to/your/file_list.txt", "r") as f:
    file_list = [line.strip() for line in f if line.strip()]  # Remove any whitespace


# Step 2: Read and concatenate the .nc files along the time dimension
combined_data = xr.open_mfdataset(file_list, concat_dim="time", combine="by_coords")

vars_in_ds = list(combined_data.data_vars.keys())
vars_to_drop = list(filter(lambda var: var!=clim_var, vars_in_ds))

combined_data = xr.open_mfdataset(file_list, concat_dim="time", combine="by_coords",
                                   chunks={'time': 1},
                                   #drop_variables=['variable_name1', 'variable_name2'])
                                   drop_variables=vars_to_drop)

combined_data = xr.open_mfdataset(file_list, concat_dim="time", combine="by_coords", chunks={'time': 10, 'lat': 5, 'lon': 5})

combined_data = combined_data.persist()

