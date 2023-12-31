# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import re


#===config===
st.set_page_config(
     page_title="Pencarian Terpadu",
     page_icon="https://github.com/faizhalas/Search4All/blob/main/images/logo.png?raw=true",
     layout="wide"
)

# Connect to the Google Sheet
st.cache_resource(ttl=3600*3)
def connect_gsheet():
  sheet_id = st.secrets.sheet_id
  sheet_name = st.secrets.sheet_info
  url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
  ji = pd.read_csv(url, dtype=str, header=0)
  ji = ji.sort_index(ascending=True) 
  return ji

ji = connect_gsheet()

#Title
st.title('Search4All: Information')

# Intro text
st.caption("Journals that are available through Search4All")

# Display an interactive table
st.dataframe(ji, use_container_width=True)
