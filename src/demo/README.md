# Demo Folder Guide

This folder contains several scripts and notebooks that demonstrate how to work with ontologies, knowledge graphs, and document processing using AI. This guide explains, step by step, what each script does and how you can use them—even if you are not a developer.

---

## 1. `app.py` — Chat with an AI Agent Using Ontologies

**Purpose:**  
This script launches a web-based chat interface where you can ask questions about specific domains. The AI agent uses both its own knowledge and a provided ontology (a structured set of terms and relationships) to answer your questions.

**How it works:**
- Loads necessary settings and credentials.
- Sets up a web page using Streamlit.
- Loads an ontology file to help the AI understand domain-specific terms.
- Configures an AI model (from Azure OpenAI) and tools (including the ability to ask a human for help if needed).
- Displays a chat interface where you can type questions.
- The AI agent uses the ontology and its tools to answer your questions, showing the conversation history.

**Who should use it:**  
Anyone who wants to interact with an AI assistant that understands specialized terminology.

---

## 2. `generate_owl.ipynb` — Automatically Generate or Extend Ontologies

**Purpose:**  
This notebook helps you create or improve an ontology (in OWL XML format) using AI, based on a domain description and existing ontology.

**How it works:**
- Loads environment settings and credentials.
- Reads a markdown file with domain terms and an existing ontology file.
- Prepares a detailed prompt for the AI, instructing it to generate a well-structured ontology.
- Sends the prompt, domain content, and existing ontology to the AI model.
- Receives a new or extended ontology from the AI and saves it back to the file.

**Who should use it:**  
Anyone who needs to build or update an ontology for a specific domain, without writing complex code.

---

## 3. `knowledge_graphs.ipynb` — Create and Visualize Knowledge Graphs from Text

**Purpose:**  
This notebook turns natural language descriptions into visual knowledge graphs, making it easier to understand complex relationships.

**How it works:**
- Sets up an AI client.
- Defines how nodes (concepts) and edges (relationships) are represented.
- Provides a function to generate a knowledge graph from a text prompt using the AI.
- Visualizes the generated graph using Graphviz.
- Includes examples, such as relationships between cars, wheels, and trains, or financial industry terms.

**Who should use it:**  
Anyone who wants to visualize and explore relationships between concepts described in plain language.

---

## 4. `split_files.ipynb` — Convert PDF Documents into Images

**Purpose:**  
This notebook splits a PDF file into individual page images (PNG format).

**How it works:**
- Specifies the PDF file and where to find it.
- Creates a new folder named after the PDF.
- Converts each page of the PDF into a PNG image (up to 150 pages).
- Saves the images in the new folder.

**Who should use it:**  
Anyone who needs to turn a PDF into images for further analysis or processing.

---

## 5. `validate_content.ipynb` — Validate and Extend Ontologies Using Document Images

**Purpose:**  
This notebook uses images of document pages and AI to validate and extend an ontology.

**How it works:**
- Loads images (created from a PDF) and an existing ontology file.
- Converts images to a format the AI can understand.
- Prepares a prompt for the AI to generate or extend an ontology based on the images and existing ontology.
- Sends the images and ontology to the AI, receives an updated ontology, and saves it.
- Processes all images in a folder, one by one.

**Who should use it:**  
Anyone who wants to use document images to help build or improve an ontology.

---

## 6. `requirements.txt` — Required Python Packages

**Purpose:**  
Lists all the Python packages you need to install to run the scripts and notebooks in this folder.

**How to use:**  
Install the requirements by running:
```
pip install -r requirements.txt
```

---

## Ontology Files (`.xml`)

Files like `onthology_bolts.xml`, `onthology_efsa_listeria.xml`, etc., are ontology files in XML format. They are used as input or output by the scripts and notebooks above.

---

## Typical Workflow

1. **Convert a PDF to images:**  
   Use `split_files.ipynb` to turn a PDF into page images.

2. **Validate or extend an ontology using images:**  
   Use `validate_content.ipynb` to process the images and update your ontology.

3. **Generate or restructure an ontology from text:**  
   Use `generate_owl.ipynb` to create or improve an ontology based on domain descriptions.

4. **Visualize relationships:**  
   Use `knowledge_graphs.ipynb` to turn text descriptions into visual knowledge graphs.

5. **Chat with the AI agent:**  
   Use `app.py` to ask questions and get answers using your ontology.

---

**Note:**  
You do not need to be a developer to use these scripts and notebooks. Follow the steps above, and refer to each section for what the script does and how to use it.