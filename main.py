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

    # combining all DataFrames into one
    streams_df = pd.concat(data_frames, ignore_index=True)
    
    # display
    st.write(streams_df)