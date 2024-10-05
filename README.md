# GraphRAG-Architecture-of-a-local-LLM-for-Gestational-Diabetes-Mellitus

## Overview

This project aims to build a Graph-RAG (Retrieval-Augmented Generation) architecture for a local language model focused on Gestational Diabetes Mellitus (GDM). It combines the latest advancements in natural language processing and knowledge graph construction to provide meaningful insights by querying medical research articles related to GDM.

## Project Structure

### 1. Data Collection

The `Data Collection.py` script is responsible for downloading the relevant data required to execute the project. It retrieves and extracts all articles from medical journals related to gestational diabetes mellitus using the **Semantic Scholar** API.

### 2. Entity Extraction and Knowledge Graph Construction

The `Entity Extraction and Construction of Knowledge Graph.py` script contains:

- **Entity extraction**: Uses few-shot learning to extract key entities from the articles.
- **Knowledge Graph Construction**: Builds a knowledge graph from these extracted entities using **Neo4j**.
- **GraphRAG Integration**: Implements the Graph-RAG method to prompt and query the model using the knowledge graph.

## How to Execute

### Prerequisites
- **Neo4j**: You will need to generate the following credentials:
  - Neo4j URL
  - Username
  - Password
- **OpenAI API Key**: Required for entity extraction using GPT 3.5 Turbo.

### Instructions
1. Clone the repository.
2. Ensure you have the necessary API keys and credentials.
3. Run `Data Collection.py` to download relevant articles.
4. Run `Entity Extraction and Construction of Knowledge Graph.py` to extract entities and build the knowledge graph on neo4j.
