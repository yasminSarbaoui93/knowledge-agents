import os
import sys
import uuid
import time
import random
from typing import List, Tuple
from typing_extensions import Annotated, TypedDict
from io import StringIO
from IPython.display import Image
import streamlit as st
import pandas as pd
import dotenv

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain import hub
from langchain_core.documents import Document
from langchain_openai import AzureChatOpenAI
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)

dotenv.load_dotenv()

prompt = hub.pull("rlm/rag-prompt")

# Desired schema for response
class AnswerWithSources(TypedDict):
    """An answer to the question, with sources."""

    answer: str
    sources: Annotated[
        List[str],
        ...,
        "List of sources (author + year) used to answer the question",
    ]

st.set_page_config(
    page_title="AI onthology generator",
)

st.title("💬 AI onthology export")
st.caption("🚀 A Bot that can use documents to generate onthologies")

def get_session_id() -> str:
    id = random.randint(0, 1000000)
    return "00000000-0000-0000-0000-" + str(id).zfill(12)

@st.cache_resource
def create_session(st: st) -> None:
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = get_session_id()
        print("started new session: " + st.session_state["session_id"])
        st.write("You are running in session: " + st.session_state["session_id"])

create_session(st)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
session_id = st.session_state.session_id

# Use session state to store conversation
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.write(message["message"])

# Load documents only once
# if 'docs' not in st.session_state:
    # st.session_state.docs = 

llm: AzureChatOpenAI = None
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

model = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider = token_provider,
        azure_deployment=os.getenv("AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME"),
        openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
        temperature=0
    )

from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings

embeddings_model : AzureOpenAIEmbeddings  = AzureOpenAIEmbeddings(    
        azure_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"),
        openai_api_version = os.getenv("AZURE_OPENAI_VERSION"),
        model= os.getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
        azure_ad_token_provider = token_provider
    )

vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
    azure_search_key=None,
    azure_ad_access_token=None,
    index_name=os.getenv("AZURE_AI_SEARCH_INDEX"),
    embedding_function=embeddings_model.embed_query,
    additional_search_client_options={"retry_total": 4},
)

current_directory = os.path.dirname(os.path.abspath(__file__))
sessions_folder = os.path.join(current_directory, "helpers/sessions")
data_folder = os.path.join(current_directory, "data")

with st.sidebar:
    st.title("Onthology Generator")
    with st.container():
        st.header("File Upload")

        # Check if 'uploaded_files' is already in session state
        if 'uploaded_files' not in st.session_state:
            st.session_state.uploaded_files = None
        
        uploaded_files = st.file_uploader(
            "Upload your documents from here:", accept_multiple_files=True, key="file_uploader"
        )
        
        if uploaded_files is not None and uploaded_files != st.session_state.uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            with st.spinner("Loading..."):
                # Iterate over the uploaded files and save them to the data folder
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(data_folder, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                time.sleep(3)
            
            st.success("Files uploaded and saved successfully!")

        # Start a new conversation
        if st.button("New Conversation"):
            st.session_state.session_id = str(uuid.uuid4())
            session_id = st.session_state.session_id
            st.session_state.conversation = []
            st.success("New conversation started!")

st.write("""Look at the image below and use it as input. Generate a response based on the image.
You are an expert in ontology engineering. Generate an OWL ontology based on the following domain description:
Define classes, data properties, and object properties.
Include domain and range for each property.
Provide the output in OWL (XML) format and only output the ontology and nothing else""")

def retrieve(query: str) -> List[Tuple[Document, float]]:
    retrieved_docs = vector_store.similarity_search_with_relevance_scores(
        query=query,
        k=4,
        score_threshold=0.80,
    )
    print(retrieved_docs)

    return retrieved_docs

def generate(docs: List[Tuple[Document, float]], query: str) -> str:
    docs_content = "\n\n".join(doc.page_content for doc in docs)
    messages = prompt.invoke({"question": query, "context": docs_content})
    structured_llm = model.with_structured_output(AnswerWithSources)
    response = structured_llm.invoke(messages)
    return response.content

query = st.chat_input("Insert your prompt here")

if query:
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st.write("Generating response...")
        docs = retrieve(query)
        response = generate(docs, query)
        st.write(response)