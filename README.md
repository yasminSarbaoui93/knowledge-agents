# Onthology generator

## Overview

## Quickstart & Infrastructure setup

The following lines of code will connect your Codespace az cli and azd cli to the right Azure subscription:

```
# log in with the provided credentials - OPEN A PRIVATE BROWSER SESSION
az login --use-device-code

# if you need to log into a specific tenant - use the --tenant 00000000-0000-0000-0000-000000000000 parameter
az login --use-device-code --tenant 00000000-0000-0000-0000-000000000000 

# "log into azure dev cli - only once" - OPEN A PRIVATE BROWSER SESSION
azd auth login --use-device-code

# press enter open up https://microsoft.com/devicelogin and enter the code

```

Now deploy the infrastructure components with azure cli

```
azd up
```

Get the values for some env variables
```
azd env get-values | grep AZURE_ENV_NAME
source <(azd env get-values | grep AZURE_ENV_NAME)
```

## (Alternative) Terraform Infrastructure Setup

To configure Terraform with your Azure subscription id from the `.env` file, run:

```bash
export TF_VAR_subscription_id=$(grep '^AZURE_SUBSCRIPTION_ID=' .env | cut -d '=' -f2- | tr -d '"')
```

Then run the following Terraform commands:

```bash
cd infra-terraform
terraform init
terraform plan
terraform apply
```
## KernelService


Kernelservice is used here as the ingestion pipeline:
https://github.com/microsoft/kernel-memory


Deploy kernelservice with the following command
```
bash ./azd-hooks/deploy-ks.sh $AZURE_ENV_NAME
```

Ingest documents via the src/ingestion/uploader.py
## Project Purpose and Detailed Explanation

This project provides an automated solution for generating ontologies from technical documents, specifically focused on materials and their properties. The primary goal is to enable organizations to transform unstructured documentation into structured, machine-readable knowledge graphs (ontologies) that can be easily accessed and queried by scientists and domain experts—potentially through conversational interfaces such as chatbots.

### Background and Motivation

The initial use case for this project arose from the need to create a comprehensive ontology based on a collection of technical documents related to materials. The ontology serves as a structured representation of domain knowledge, making it easier for scientists to discover, access, and utilize information about various materials and their characteristics.

### Key Features

- **Automated Ontology Generation:** The system ingests technical documents (such as standards, specifications, and research papers) and generates ontologies in standard formats (e.g., OWL/XML).
- **Infrastructure as Code:** The project leverages Azure infrastructure automation, allowing users to deploy all required resources, permissions, and models with a single command (`azd up`).
- **Document Ingestion Pipeline:** Using tools like KernelService, documents are processed and prepared for ontology extraction.
- **Scalability and Partitioning:** The solution addresses challenges with large documents by supporting semantic partitioning—splitting large sources into smaller, meaningful sections to ensure accurate and manageable ontology generation.
- **Visualization and Validation:** Generated ontologies can be visualized using tools such as WebVOWL, enabling users to inspect and validate the resulting knowledge graphs.

### Typical Workflow

1. **Infrastructure Deployment:** Set up all necessary Azure resources using the provided scripts and configuration files.
2. **Document Upload:** Ingest relevant technical documents via the uploader pipeline.
3. **Ontology Generation:** Process the documents to extract entities, relationships, and properties, producing an ontology file.
4. **Review and Validation:** Visualize and validate the ontology using external tools or integrate it into downstream applications (e.g., chatbots for scientific Q&A).

### Use Cases

- **Knowledge Discovery:** Scientists can query the ontology to find information about materials, standards, and their interrelations.
- **Conversational Access:** The structured knowledge can be exposed via chatbots or other interfaces, making it easier for users to interact with complex technical information.
- **Integration:** The ontologies can be integrated into broader knowledge management systems or used to enhance search and discovery capabilities.

### Technical Challenges Addressed

- **Handling Large Documents:** The project implements strategies for partitioning and processing large documents that exceed the capacity of language models, ensuring meaningful and complete ontology extraction.
- **Automation and Reproducibility:** By automating infrastructure and processing steps, the solution ensures consistency and ease of deployment across different environments.

---

This project is designed to accelerate the transformation of unstructured technical knowledge into actionable, structured data, supporting scientific research and innovation.