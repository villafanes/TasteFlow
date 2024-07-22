import json
import os
from data_fcts import *
import pandas as pd
import streamlit as st
import plotly.express as px

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
        'ts': 'Date',
        'master_metadata_track_name': 'Song',
        'master_metadata_album_artist_name': 'Artist',
        'master_metadata_album_album_name': 'Album'
    }
    streams_df = streams_df.rename(columns=renamed_cols)

   # Convert 'Date' column to datetime
    streams_df['Date'] = pd.to_datetime(streams_df['Date'])

    # Generate artist stats
    artist_stats = streams_by_artist(streams_df)

    # Select artist
    select_artist = st.selectbox("Select an artist", options=list(artist_stats.keys()))

    # Filter data for selected artist
    artist_data = streams_df[streams_df['Artist'] == select_artist]

    # Create scatter plot
    artist_fig = px.scatter(artist_data, x='Date', y='Song',
                            hover_data=['Song', 'Album', 'Date'],
                            title=f"Streaming History of {select_artist}",
                            labels={'Date': 'Date', 'Song': 'Song'},
                            template='plotly_white')

    # Update layout for better readability
    artist_fig.update_layout(xaxis_title="Date",
                             xaxis=dict(tickformat="%b %Y"))

    st.plotly_chart(artist_fig)