import json
import os
from data_fcts import *
import pandas as pd
import streamlit as st
import plotly.express as px

st.title('Welcome to TasteFlow')

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
    renamed_cols = {
        'ts': 'Date',
        'master_metadata_track_name': 'Song',
        'master_metadata_album_artist_name': 'Artist',
        'master_metadata_album_album_name': 'Album'
    }
    streams_df = streams_df.rename(columns=renamed_cols)

   # converting to datetime type
    streams_df['Date'] = pd.to_datetime(streams_df['Date'])

    # generating new artist stats data frame
    artist_stats = streams_by_artist(streams_df)

    # user selects artist
    select_artist = st.selectbox("Select an artist", options=list(artist_stats.keys()))
    artist_data = streams_df[streams_df['Artist'] == select_artist]

    # creating scatter plot, organized by album and listening date
    artist_fig = px.scatter(artist_data, x='Date', y='Album',
                            hover_data={'Song': True, 'Album': True, 'Date': '|%m-%d-%Y'},
                            title=f"Streaming History of {select_artist}",
                            labels={'Date': 'Date', 'Album': 'Album'},
                            template='plotly_white')

    # cleaning chart labels
    artist_fig.update_layout(xaxis_title="Date",
                             yaxis_title="Album", 
                             xaxis=dict(tickformat="%m %Y"),
                             yaxis=dict(categoryorder="total ascending")) 

    st.plotly_chart(artist_fig)


    # bar graph for listens per album
    album_stats = artist_data.groupby('Album').size().reset_index(name='Number of Streams')

    # orders albums by most to least listened to 
    album_stats = album_stats.sort_values(by='Number of Streams', ascending=False)  

    # creating bar plot, organized by album and number of streams 
    album_fig = px.bar(album_stats, x='Number of Streams', y='Album',
                       title=f"Number of Streams per Album for {select_artist}",
                       labels={'Number of Streams': 'Number of Streams', 'Album': 'Album'},
                       template='plotly_white')
    
    # cleaning chart labels
    album_fig.update_layout(yaxis=dict(categoryorder='total ascending'))

    st.plotly_chart(album_fig)


    # user selects album by selected artist
    select_album = st.selectbox("Select an album", options=album_stats['Album'])
    album_data = artist_data[artist_data['Album'] == select_album]

    # bar graph for song listens per album
    song_stats = album_data.groupby('Song').size().reset_index(name='Number of Streams')
    # orders songs by most to least listened to 
    song_stats = song_stats.sort_values(by='Number of Streams', ascending=False) 

    # creating bar plot, organized by songs on album and number of streams 
    song_fig = px.bar(song_stats, x='Number of Streams', y='Song',
                      title=f"Number of Streams per Song on '{select_album}'",
                      labels={'Number of Streams': 'Number of Streams', 'Song': 'Song'},
                      template='plotly_white')
    
    # cleaning chart labels
    song_fig.update_layout(yaxis=dict(categoryorder='total ascending'))

    st.plotly_chart(song_fig)