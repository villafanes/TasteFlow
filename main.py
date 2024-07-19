import json
import os
from data_fcts import *
import pandas as pd
import streamlit as st

st.title('Full Spotify Listening History')

files = st.file_uploader("Upload JSON listening files", type="json", accept_multiple_files=True)

