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
  sheet_name = st.secrets.sheet_journal
  url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
  df = pd.read_csv(url, dtype=str, header=0)
  df = df.sort_index(ascending=False).fillna('NaN')
  df["full-text"] = df[["abstract", "introduction", "methods", "discussion", "conclusion"]].agg(" - ".join, axis=1)
  return df

df = connect_gsheet()

# image dictionary
image_dict = {
  "Atom Indonesia": "https://github.com/faizhalas/Search4All/blob/main/images/journal/atom.png?raw=true",
  "EKSPLORIUM": "https://github.com/faizhalas/Search4All/blob/main/images/journal/eksplorium.jpg?raw=true",
  "GANENDRA": "https://github.com/faizhalas/Search4All/blob/main/images/journal/ganendra.png?raw=true",
  "Jurnal Pengembangan Energi Nuklir": "https://github.com/faizhalas/Search4All/blob/main/images/journal/jpen.jpg?raw=true",  
  "Jurnal Sains dan Teknologi Nuklir Indonesia": "https://github.com/faizhalas/Search4All/blob/main/images/journal/jstni.jpg?raw=true",
  "Jurnal Teknologi Reaktor Nuklir Tri Dasa Mega": "https://github.com/faizhalas/Search4All/blob/main/images/journal/tridasa.jpg?raw=true",
  "URANIA": "https://github.com/faizhalas/Search4All/blob/main/images/journal/urania.jpg?raw=true"
}

#Title
st.title('Search4All: Journal')

# Intro text
st.caption(f"Discover and learn among the more than **{df.shape[0]}** sources available from Search4All.")
c1, c2, c3 = st.columns([5,2,3])

# The search bar
text_search = c1.text_input("Search by author, title, or full-text. Separate concepts by semicolons (;)")

# Get keywords from search bar
keyword_list_j = [keyword.strip() for keyword in text_search.split(";")]

# option to choose
part_opt = ["author", "title", "abstract", "introduction", "methods", "discussion", "conclusion", "full-text"]

# Add options
s_titles = ["All", "Atom Indonesia", "EKSPLORIUM", "GANENDRA", "Jurnal Pengembangan Energi Nuklir", "Jurnal Sains dan Teknologi Nuklir Indonesia", "Jurnal Teknologi Reaktor Nuklir Tri Dasa Mega", "URANIA"]
journalname = c2.selectbox("Source Titles", s_titles)
search_opt = c3.multiselect(
     "Search fields",
     part_opt,
     ["author", "title"])


# filter
if keyword_list_j is not None:        
        key_df_j = pd.DataFrame(columns=['id', 'url', 'journal_title', 'title', 'author', 'year', 'volis'])
        patterns = [r'\b{}\b'.format(re.escape(word)) for word in keyword_list_j]

        for col in search_opt:
            conditions = [df[col].str.contains(pattern, regex=True, flags=re.IGNORECASE) for pattern in patterns]
            column_result = df[np.logical_and.reduce(conditions)]
            key_df_j = pd.concat([key_df_j, column_result]).drop_duplicates()

        if journalname != s_titles[0]:
            key_df_j = key_df_j[key_df_j['journal_title'].str.contains(journalname)]

# creating card(s)
N_cards_per_row = 5
if text_search:
    for n_row, row in key_df_j.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        
        #get image
        link = row["url"].strip()
        journal_title = row["journal_title"].strip()
        image_link = image_dict[journal_title]
        
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{row['year'].strip()} - {row['volis'].strip()} ")
            markdown = f'<a href="{link}" target="_blank"><img src="{image_link}" alt="Click me" width="100%" /></a>'
            st.markdown(markdown, unsafe_allow_html=True)
            st.markdown(f"**{row['author'].strip()}**")
            st.markdown(f"**Title:** *{row['title'].strip()}*")
