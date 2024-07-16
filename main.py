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

# dict of streaming instances by artist
streams_per_artist = streams_by_artist(streams_dict)

# dict of artists and all-time stream counts
artist_total_streams = artist_ct(streams_per_artist)

artist_yearly_streams = artist_yr_ct(streams_per_artist)

# dict of streaming instances by album
streams_per_album = streams_by_album(streams_dict)

# dict of streaming instances by album
streams_per_song = streams_by_song(streams_dict)            

print(artist_total_streams)