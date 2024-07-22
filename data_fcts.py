#https://www.geeksforgeeks.org/how-to-merge-multiple-json-files-using-python/
import json
import os

# condenses the multiple files downloaded from Spotify
def merge_files(file_paths, output_file):
    # avoids creating duplicate files
    if os.path.exists(output_file):
        os.remove(output_file)

    merged_data = []
    for path in file_paths:
        with open(path, 'r') as in_file:
            data = json.load(in_file)
            merged_data.extend(data) # writes all data into one list

    with open(output_file, 'w') as outfile:
        json.dump(merged_data, outfile, indent=2) # organizes data with indentations


# processes data in the new, condensed file to isolate only Date, Song, Artist, and Album
def process_file(in_file):
    with open(in_file, 'r') as file:
        data = json.load(file)

    stream_dict = []
    for entry in data: # processing data into a readable format
        formatted_instance = {
            "Date": entry["ts"][:10],  # extracting YYYY-MM-DD from ts
            "Song": entry["master_metadata_track_name"],
            "Artist": entry["master_metadata_album_artist_name"],
            "Album": entry["master_metadata_album_album_name"]
        }
        stream_dict.append(formatted_instance)

    return stream_dict


# dictionary to store k,v where k is the artist, and v is every instance a song of theirs was streamed
def streams_by_artist(data):
    artist_dict = {}

    for index, row in data.iterrows():
        artist = row["Artist"]
        if artist not in artist_dict:
            artist_dict[artist] = []

        stream_inst = row.drop("Artist").to_dict()  # Convert the row to a dictionary excluding "Artist"
        artist_dict[artist].append(stream_inst)
    
    return artist_dict

# dictionary to store artist: number of streams ever
def artist_ct(data):
    total_counts = {}
    artist_ct = {}
    for k,v in data.items():
        total_counts[k] = len(v) # counts all streams 

    artist_ct = {k: v for k, v in sorted(total_counts.items(), key=lambda item: item[1], reverse=True)} # descending order
    return artist_ct

# dictionary to store artist: number of streams per year
def artist_yr_ct(data):
    yearly_counts = {}

    for k,v in data.items():
        for stream in v:
            artist = k
            year = stream['Date'][:4]  

            # creates key for artist
            if artist not in yearly_counts:
                yearly_counts[artist] = {}

            # adds k,v pair into the inner dictionary for every new year in the data
            if year not in yearly_counts[artist]:
                yearly_counts[artist][year] = 0

            # increments the count for the artist's streams in a specific year
            yearly_counts[artist][year] += 1

    return yearly_counts
     

# dictionary to store k,v where k is the album + artist, and v is every instance a song on it was streamed
def streams_by_album(data):
    album_dict = {}

    for entry in data:
        artist = entry["Artist"]
        album = entry["Album"]
        album_key = f"{album} by {artist}" 

        if album_key not in album_dict:
            album_dict[album_key] = []

        stream_inst = {k: v for k, v in entry.items() if k != "Artist" and k != "Album"} # stores date and song name
        album_dict[album_key].append(stream_inst)
    
    return album_dict


# dictionary to store k,v where k is the song + artist, and v is every time it was played, and what album it was on
def streams_by_song(data):
    song_dict = {}

    for entry in data:
        song = entry["Song"]
        artist = entry["Artist"]
        song_key = f"{song} by {artist}"

        if song_key not in song_dict:
            song_dict[song_key] = []

        stream_inst = {k: v for k, v in entry.items() if k != "Song" and k != "Artist"} # stores date and album name
        song_dict[song_key].append(stream_inst)
    
    return song_dict