import streamlit as st
import pdfplumber
import pandas as pd

@st.cache_data(experimental_allow_widgets=True)
def convert(uploaded_files):
    data = []
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        data.append({"File Name": file.name, "Text": text})
    return data

st.title("PDF to Text Converter")
st.header("Upload PDF Files")

uploaded_files = st.file_uploader("Choose files", type=['pdf'], accept_multiple_files=True)

if uploaded_files is not None:
    extracted_data = convert(uploaded_files)
    df = pd.DataFrame(extracted_data)
    if not df.empty:
        st.subheader("Extracted Text")
        st.data_editor(df)
