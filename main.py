import json
import os
from data_fcts import *

# Update to take in user file paths
file_paths = ["SH_20_21.json", "SH_21_22.json", "SH_22_23.json", "SH_23_24.json"]
file = "full_spotify_streaming_history.json"
merge_files(file_paths, file)
print(f"Merged data written to '{file}")

# processed list of dictionaries of each stream
streams_dict = process_file(file)

# list of streaming instances by artist
streams_per_artist = streams_by_artist(streams_dict)

streams_per_album = streams_by_album(streams_dict)
print(streams_per_album)   
            
