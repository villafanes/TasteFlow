#https://www.geeksforgeeks.org/how-to-merge-multiple-json-files-using-python/
import json
import os

# condenses the multiple files downloaded from Spotify
def merge_files(file_paths, output_file):
    if os.path.exists(output_file):
        os.remove(output_file)

    merged_data = []
    for path in file_paths:
        with open(path, 'r') as in_file:
            data = json.load(in_file)
            merged_data.extend(data)
    with open(output_file, 'w') as outfile:
        json.dump(merged_data, outfile, indent=2)


# processes data in the new, condensed file to isolate only Date, Song, Artist, and Album
def process_file(in_file):
    with open(in_file, 'r') as file:
        data = json.load(file)
        
    song_dict = []
    for entry in data:
        formatted_instance = {
            "Date": entry["ts"][:10],  # Extract YYYY-MM-DD from ts
            "Song": entry["master_metadata_track_name"],
            "Artist": entry["master_metadata_album_artist_name"],
            "Album": entry["master_metadata_album_album_name"]
        }
        song_dict.append(formatted_instance)

    return song_dict

    

