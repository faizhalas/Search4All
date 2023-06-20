# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import re

st.set_page_config(page_title="Pencarian Terpadu", page_icon="https://digilib.polteknuklir.ac.id/perpus/images/default/logo.png", 
                layout="wide", initial_sidebar_state="expanded")

# Connect to the Google Sheet
sheet_id = st.secrets.sheet_id
sheet_name = st.secrets.sheet_name
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str, header=0)
df = df.sort_index(ascending=False).fillna('NaN')

# image dictionary
image_dict = {
  "Buku Ketenaganukliran": "https://github.com/faizhalas/Search4All/blob/main/images/bnuklir.png?raw=true",
  "Buku Non-ketenaganukliran": "https://github.com/faizhalas/Search4All/blob/main/images/bnonnuklir.png?raw=true",
  "Buku Pedoman": "https://github.com/faizhalas/Search4All/blob/main/images/pedoman.png?raw=true",
  "Direktori, annual, yearbook": "https://github.com/faizhalas/Search4All/blob/main/images/diranuyear.png?raw=true",
  "Ensiklopedia": "https://github.com/faizhalas/Search4All/blob/main/images/ensiklopedia.png?raw=true",
  "Handbook & manual": "https://github.com/faizhalas/Search4All/blob/main/images/hanmanu.png?raw=true",
  "Jurnal": "https://github.com/faizhalas/Search4All/blob/main/images/jurnal.png?raw=true",
  "Kamus": "https://github.com/faizhalas/Search4All/blob/main/images/kamus.png?raw=true",
  "Kerja Praktik": "https://github.com/faizhalas/Search4All/blob/main/images/kp.png?raw=true",
  "Prosiding": "https://github.com/faizhalas/Search4All/blob/main/images/pros.png?raw=true",
  "Terbitan Internal": "https://github.com/faizhalas/Search4All/blob/main/images/ti.png?raw=true",
  "Tugas Akhir": "https://github.com/faizhalas/Search4All/blob/main/images/ta.png?raw=true"
}

#Title
st.title('Search4All: Recorded materials')

# Intro text
st.caption(f"Discover and learn among the more than **{df.shape[0]}** sources available from Search4All.")
c1, c2, c3 = st.columns([5,2,3])

# The search bar
text_search = c1.text_input("Search by author, title, or full-text. Separate concepts by semicolons (;)")

# Get keywords from search bar
keyword_list = [keyword.strip() for keyword in text_search.split(";")]

# Add options
format_options = ["All", "Buku Ketenaganukliran", "Buku Non-ketenaganukliran", "Buku Pedoman", "Direktori, annual, yearbook", "Ensiklopedia", "Handbook & manual", "Jurnal", "Kamus", "Kerja Praktik", "Prosiding", "Terbitan Internal", "Tugas Akhir"]
type_for = c2.selectbox("Type", format_options)
search_opt = c3.multiselect(
        "Search fields",
        ["author", "title", "full-text"],
        ["author", "title"])

# filter
if keyword_list is not None:        
        key_df = pd.DataFrame(columns=['biblio_id', 'url', 'gmd_id', 'title', 'author', 'year', 'callnum', 'full-text'])
        patterns = [r'\b{}\b'.format(re.escape(word)) for word in keyword_list]

        for col in search_opt:
            conditions = [df[col].str.contains(pattern, regex=True, flags=re.IGNORECASE) for pattern in patterns]
            column_result = df[np.logical_and.reduce(conditions)]
            key_df = pd.concat([key_df, column_result])

        if type_for != format_options[0]:
            key_df = key_df[key_df['gmd_id'].str.contains(type_for)]

# creating card(s)
N_cards_per_row = 4
if text_search:
    for n_row, row in key_df.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        
        #get image
        link = row["url"].strip()
        gmd_id = row["gmd_id"].strip()
        image_link = image_dict[gmd_id]
        
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{row['gmd_id'].strip()} - {row['year'].strip()} ")
            markdown = f'<a href="{link}" target="_blank"><img src="{image_link}" alt="Click me" width="100%" /></a>'
            st.markdown(markdown, unsafe_allow_html=True)
            st.markdown(f"**{row['author'].strip()}**")
            st.markdown(f"*{row['title'].strip()}*")
