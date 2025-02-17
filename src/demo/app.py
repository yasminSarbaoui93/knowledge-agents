import os
import time
from io import StringIO
import dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureChatOpenAI
import streamlit as st
import pandas as pd

dotenv.load_dotenv()

llm: AzureChatOpenAI = None

st.title("Chat with Onthology Expert")


with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.write("Filename:", uploaded_file.name)
        # To read file as bytes:
        # bytes_data = uploaded_file.getvalue()
        # st.write(bytes_data)

        if uploaded_file.name.endswith('.csv'):
            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            st.write(df)
        elif uploaded_file.name.endswith('.txt'):
            # Read the TXT file
            text = uploaded_file.read().decode("utf-8")
            st.text_area("File Content", text, height=300)
        elif uploaded_file.name.endswith('.xlsx'):
            # Read the Excel file
            df = pd.read_excel(uploaded_file)
            st.write(df)
