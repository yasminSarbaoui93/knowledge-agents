import os
import pytz
from datetime import datetime
import dotenv
import streamlit as st
from langchain_openai import AzureChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain.agents import AgentExecutor, create_structured_chat_agent, create_react_agent
from langchain.globals import set_verbose
from langchain_core.tools import tool

from langchain_community.agent_toolkits.load_tools import load_tools

from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.core.credentials import AzureKeyCredential
set_verbose(True)

dotenv.load_dotenv()

llm: AzureChatOpenAI = None
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

credential = AzureKeyCredential(os.environ["AZURE_AI_SEARCH_KEY"]) if len(os.environ["AZURE_AI_SEARCH_KEY"]) > 0 else DefaultAzureCredential()
 
st.set_page_config(
    page_title="AI agent that can use onthologies"
)

st.title("💬 AI agent that can use onthologies")
st.caption("🚀 A Bot that can use a vector store, humans and tools to answer questions about specific domains")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)


llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME"),
    openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
    temperature=0,
    streaming=True
)
 
tools = load_tools(
    ["human"], 
    llm=llm,
)

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

onthology_file_path="onthology_bolts.xml"
with open(onthology_file_path, "r") as f:
    onthologyXML = f.read()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant and have the following tools at your disposal: {tools}"),
        ("system", "You can ask a human for guidance when you think you got stuck or you are not sure what to do next."),
        ("system", "The input should be a question for the human."),
        ("system", "You also have access to an onthology to clearify domain specific terms. {onthologyXML}"),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

human_query = st.chat_input()

if human_query is not None and human_query != "":

    st.session_state.chat_history.append(HumanMessage(human_query))

    with st.chat_message("Human"):
        st.markdown(human_query)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke(
            {"input": human_query, "chat_history": st.session_state.chat_history, "tools": tools, "onthologyXML": onthologyXML}, {"callbacks": [st_callback]}, 
        )

        ai_response = st.write(response["output"])