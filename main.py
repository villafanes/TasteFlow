import json
import os
from data_fcts import merge_files, process_file

# Update to take in user file paths
file_paths = ["SH_20_21.json", "SH_21_22.json", "SH_22_23.json", "SH_23_24.json"]
file = "full_spotify_streaming_history.json"
merge_files(file_paths, file)
print(f"Merged data written to '{file}")

# processed list of dictionaries of each stream
streams_dict = process_file(file)
