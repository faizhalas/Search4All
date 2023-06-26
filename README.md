# Search4All
Web application for converting PDF to tabular data to aid in [Search4All](https://github.com/faizhalas/Search4All) processes.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)][share_link]
[![License](https://img.shields.io/github/license/faizhalas/library-tools?color=blue)](https://github.com/faizhalas/Search4All/blob/main/LICENSE)

### Create your own app

## Component Setup - Connection
- For security reason, you need to prepare sheet_id, sheet_name, sheet_journal, and sheet_info which are placed on Streamlit:
```
# URL of a Google Sheet
https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}

# Home
sheet_id = st.secrets.sheet_id
sheet_name = st.secrets.sheet_name

# Journal
sheet_name = st.secrets.sheet_journal

# Journal Info
sheet_name = st.secrets.sheet_info
```

## Component Setup - Home
- Changes to the interface
```
# Title on the browser tab.
page_title="Your Text"

# Icon on the browser tab.
page_icon="Your URL"

# Title on the web page.
st.title("Your Text")

# Sub-title on the web page.
st.caption("Your Text")

# How many cards appear in one row of search results.
N_cards_per_row = 4
```

- Changes to the variables
```
# Image component to match the collection type.
image_dict = {"Your Text": "Your URL"}

# If you want a full-text search, you can manipulate the dataframe created because Google Sheets limits 50,000 characters in a cell.
df["full-text"] = df[["type1", "type2", "type3", "type4", "....."]]

# Option to search for in the search field. Adjust and match with your Google Sheet columns.
list_opt = ["column1", "column2", "column3", "column4", "....."]

# List of owned collection types. "All" indicates that the search will be performed on all collection types.
format_options = ["All", "type1", "type2", "type3", "type4", "....."]
```

## Component Setup - Journal
- Changes to the variables
```
# Image component to match the collection type.
image_dict = {"Your Text": "Your URL"}

# If you want a full-text search, you can manipulate the dataframe created because Google Sheets limits 50,000 characters in a cell.
df["full-text"] = df[["type1", "type2", "type3", "type4", "....."]]

# Option to search for in the search field. Adjust and match with your Google Sheet columns.
part_opt = ["column1", "column2", "column3", "column4", "....."]

# List of journal titles. "All" indicates that the search will be performed on all journal.
s_titles = ["All", "type1", "type2", "type3", "type4", "....."]
```







[share_link]:https://search4all.streamlit.app
