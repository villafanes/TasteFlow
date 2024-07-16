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

    stream_dict = []
    for entry in data:
        formatted_instance = {
            "Date": entry["ts"][:10],  # Extract YYYY-MM-DD from ts
            "Song": entry["master_metadata_track_name"],
            "Artist": entry["master_metadata_album_artist_name"],
            "Album": entry["master_metadata_album_album_name"]
        }
        stream_dict.append(formatted_instance)

    return stream_dict


# dictionary to store k,v where k is the artist, and v is every instance a song of their's was streamed
def streams_by_artist(data):
    artist_dict = {}

    for entry in data:
        artist = entry["Artist"]
        if artist not in artist_dict:
            artist_dict[artist] = []
        stream_inst = {k: v for k, v in entry.items() if k != "Artist"}
        artist_dict[artist].append(stream_inst)
    
    return artist_dict

# dictionary to store artist: number of streams ever
def artist_ct(data):
    total_counts = {}
    for k,v in data.items():
        total_counts[k] = len(v)

    return total_counts

# dictionary to store k,v where k is the album + artist, and v is every instance a song on it was streamed
def streams_by_album(data):
    album_dict = {}

    for entry in data:
        artist = entry["Artist"]
        album = entry["Album"]
        album_key = f"{album} by {artist}"

        if album_key not in album_dict:
            album_dict[album_key] = []
        stream_inst = {k: v for k, v in entry.items() if k != "Artist" and k != "Album"}
        album_dict[album_key].append(stream_inst)
    
    return album_dict


def streams_by_song(data):
    song_dict = {}

    for entry in data:
        song = entry["Song"]
        artist = entry["Artist"]
        song_key = f"{song} by {artist}"

        if song_key not in song_dict:
            song_dict[song_key] = []
        stream_inst = {k: v for k, v in entry.items() if k != "Song" and k != "Artist"}
        song_dict[song_key].append(stream_inst)
    
    return song_dict