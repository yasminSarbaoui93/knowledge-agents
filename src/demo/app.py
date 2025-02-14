import os
from io import StringIO
import dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureChatOpenAI

dotenv.load_dotenv()

llm: AzureChatOpenAI = None

from langchain_core.prompts import ChatPromptTemplate


system_prompt = """
You are an expert in ontology engineering. Generate an OWL ontology based on the following domain description:
Define classes, data properties, and object properties.
Include domain and range for each property.
Provide the output in OWL (XML) format."""


# Function to generate ontology
def generate_ontology(domain_description):
    prompt = f"Domain description: {domain_description}\nGenerate OWL ontology."
    response = llm.invoke([(
        "system", system_prompt

    ),
    ("human", prompt),])
    return respone.content