import json
import os
from data_fcts import *
import pandas as pd
import streamlit as st

st.title('Full Spotify Listening History')

files = st.file_uploader("Upload JSON listening files", type="json", accept_multiple_files=True)

if files:
    # storing pandas data frames
    data_frames = []

    for file in files:
        content = file.read()
        data = json.loads(content)

        # converting JSON to DataFrame 
        df = pd.json_normalize(data)
        data_frames.append(df)

    # combining all data frames into one
    streams_df = pd.concat(data_frames, ignore_index=True)

    # if an entry is not a song, exclude it from the data frame
    streams_df = streams_df.dropna(subset=['master_metadata_track_name'])

    # only keeping the date, song, artist, and album columns
    filtered_cols = [
        'ts',
        'master_metadata_track_name',
        'master_metadata_album_artist_name',
        'master_metadata_album_album_name'
    ]
    streams_df = streams_df[filtered_cols]

    # renaming
    renamed_cols = {
        'ts': 'date',
        'master_metadata_track_name': 'song',
        'master_metadata_album_artist_name': 'artist',
        'master_metadata_album_album_name': 'album'
    }
    streams_df = streams_df.rename(columns=renamed_cols)

    # display
    st.write(streams_df)