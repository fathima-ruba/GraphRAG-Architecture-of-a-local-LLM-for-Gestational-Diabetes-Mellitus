# Commented out IPython magic to ensure Python compatibility.
!pip install langchain_core
!pip install langchain_community
!pip install langchain
!pip install langchain_openai
!pip install langchain_experimental
!pip install neo4j
!pip install yfiles_jupyter_graphs
!pip install PyPDF2
!pip install pypdf
# %pip install --upgrade openai --quiet

from langchain.graphs import Neo4jGraph

url = "ENTER YOUR NEO4J URL"
username = "ENTER YOUR NEO4J USERNAME"
password = "ENTER YOUR NEO4J PASSWORD"
graph = Neo4jGraph(
    url=url,
    username=username,
    password=password
)

import os
os.environ['OPENAI_API_KEY']='ENTER YOUR OPEN AI API KEY'
api_key = os.environ['OPENAI_API_KEY']

from langchain_community.graphs.graph_document import (
    Node as BaseNode,
    Relationship as BaseRelationship,
    GraphDocument,
)
from langchain.schema import Document
from typing import List, Dict, Any, Optional
from langchain.pydantic_v1 import Field, BaseModel

class Property(BaseModel):
  """A single property consisting of key and value"""
  key: str = Field(..., description="key")
  value: str = Field(..., description="value")

class Node(BaseNode):
    properties: Optional[List[Property]] = Field(
        None, description="List of node properties")

class Relationship(BaseRelationship):
    properties: Optional[List[Property]] = Field(
        None, description="List of relationship properties"
    )

# class Source(BaseSource):
#     properties: Optional[List[Property]] = Field(
#         None, description="List of sources"
#     )

class KnowledgeGraph(BaseModel):
    """Generate a knowledge graph with entities and relationships."""
    nodes: List[Node] = Field(
        ..., description="List of nodes in the knowledge graph")
    rels: List[Relationship] = Field(
        ..., description="List of relationships in the knowledge graph"
    )

def format_property_key(s: str) -> str:
    words = s.split()
    if not words:
        return s
    first_word = words[0].lower()
    capitalized_words = [word.capitalize() for word in words[1:]]
    return "".join([first_word] + capitalized_words)

def props_to_dict(props) -> dict:
    """Convert properties to a dictionary."""
    properties = {}
    if not props:
      return properties
    for p in props:
        properties[format_property_key(p.key)] = p.value
    return properties

def map_to_base_node(node: Node) -> BaseNode:
    """Map the KnowledgeGraph Node to the base Node."""
    properties = props_to_dict(node.properties) if node.properties else {}
    properties["name"] = node.id.title()
    return BaseNode(
        id=node.id.title(), type=node.type.capitalize(), properties=properties
    )

def map_to_base_relationship(rel: Relationship) -> BaseRelationship:
    """Map the KnowledgeGraph Relationship to the base Relationship."""
    source = map_to_base_node(rel.source)
    target = map_to_base_node(rel.target)
    properties = props_to_dict(rel.properties) if rel.properties else {}
    return BaseRelationship(
        source=source, target=target, type=rel.type, properties=properties
    )

import os
from langchain.chains.openai_functions import create_openai_fn_chain, create_structured_output_chain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import List, Optional

os.environ["OPENAI_API_KEY"] = "ENTER YOUR OPEN AI API KEY"
llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)

def get_extraction_chain(
    allowed_nodes: Optional[List[str]] = None,
    allowed_rels: Optional[List[str]] = None
):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""# Knowledge Graph Instructions for GPT-3.5
You are a medical expert specializing in Gestational Diabetes Mellitus helping us extract relevant information.
This is an excerpt of a research article from a medical journal. The task is to extract as many relevant interventions related to Gestational Diabetes Mellitus (GDM).
The interventions should be identified as entities using their names or descriptions, not numerical identifiers.
Additionally, extract all relevant relationships between identified interventions and other entities using descriptive labels.
The extracted entities and relationships are directly transferred to a Neo4j database without using numerical node IDs but using descriptive entity names.

## Entity Disambiguation
- When extracting entities, ensure that duplicate entities are not extracted.
- If an entity appears multiple times in different forms or with different names, consolidate them into a single entity.
- If no relevant interventions are mentioned, do not extract any entities.

## Example Extractions
- "Intervention: Exercise"
  - "Frequency: 5 times a week"
  - "Duration: 30 minutes"
  - "Intensity: Moderate pace"
- "Intervention: Diet"
  - "Details: Low carbohydrate, high fiber"
- "Intervention: Insulin Therapy"
  - "Dosage: As prescribed by physician"

## Example Relationships
- "Insulin Therapy" -> "controls" -> "Gestational Diabetes Mellitus"
- "Smartphone-Based Lifestyle Interventions" -> "enhances" -> "Maternal Outcomes"
- "Gestational Diabetes Mellitus" -> "impacts" -> "Infant Outcomes"
"""
            ),
            ("system", "You are a medical expert specializing in Gestational Diabetes Mellitus interventions to prevent it from becoming type 2 diabetes"),
            ("human", "Now based on the examples given, extract only relevant interventions related to gestational diabetes and its relationships using descriptive labels and not numerical node IDs from the following: {doc}."),
        ]
    )
    return create_structured_output_chain(KnowledgeGraph, llm, prompt, verbose=False)

def extract_and_store_graph(
    document: Document,
    nodes: Optional[List[str]] = None,
    rels: Optional[List[str]] = None
) -> None:
    # Extract graph data using OpenAI functions
    extract_chain = get_extraction_chain(nodes, rels)
    response = extract_chain.invoke(document.page_content)
    data = response['function']

    # Ensure 'nodes' and 'rels' are present in the response
    if 'nodes' not in data or 'rels' not in data:
        raise ValueError("Missing 'nodes' or 'rels' in the response data")

    # Construct a graph document
    graph_document = GraphDocument(
        nodes=[map_to_base_node(node) for node in data['nodes']],
        relationships=[map_to_base_relationship(rel) for rel in data['rels']]
    )

    # Store information into a graph
    print(graph_document)
    graph.add_graph_documents([graph_document])
    return graph_document

def extract_and_store_graph(
    document: Document,
    nodes:Optional[List[str]] = None,
    rels:Optional[List[str]]=None) -> None:
    # Extract graph data using OpenAI functions
    extract_chain = get_extraction_chain(nodes, rels)
    data = extract_chain.invoke(document.page_content)['function']
    # Construct a graph document
    graph_document = GraphDocument(
      nodes = [map_to_base_node(node) for node in data.nodes],
      relationships = [map_to_base_relationship(rel) for rel in data.rels],
      source = document
    )
    # Store information into a graph
    print(graph_document)
    graph.add_graph_documents([graph_document])
    return graph_document

import openai
from packaging import version

required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)

if current_version < required_version:
    raise ValueError(f"Error: OpenAI version {openai.__version__}"
                     " is less than the required version 1.1.1")
else:
    print("OpenAI version is compatible.")

from openai import OpenAI
client = OpenAI(api_key="ENTER YOUR OPEN AI API KEY")

from openai import OpenAI
import os

MODEL="gpt-3.5-turbo-16k"

openai.api_key = "ENTER YOUR OPEN AI API KEY"

# Delete the graph
#graph.query("MATCH (n) DETACH DELETE n")

"""# 2000"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2000'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2001"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2001'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2002"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2002'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2003"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2003'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2004"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2004'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2005"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2005'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2006"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2006'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2007"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2007'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2008"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2008'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2009"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2009'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2010"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2010'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2011"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2011'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2012"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2012'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2013"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2013-Part1'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2013-Part2'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2013-Part3'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2013-Part4'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2014"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2014-Part1'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2014-Part2'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2014-Part3'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2014-Part4'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2014-Part5'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2015"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2015-Part1'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2015-Part2'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2015-Part3'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2015-Part4'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2016"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2016-Part1'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2016-Part2'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2016-Part3'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2016-Part4'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2016-Part5'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2017"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2017-Part1'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2017-Part2'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2017-Part3'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2017-Part4'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2017-Part5'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2018"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2018-Part2'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2018-Part3'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2018-Part4'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2018-Part5'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2019"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2019-Part1'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2019-Part2'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2019-Part3'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2019-Part4'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2019-Part5'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2020"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2020-Part1'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2020-Part2'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2020-Part3'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2020-Part4'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2020-Part5'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2021"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2021-Part1'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2021-Part2'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2021-Part3'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2021-Part4'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2021-Part5'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2022"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2022-Part1'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2022-Part2'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2022-Part3'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2022-Part4'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2022-Part5'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

"""# 2023-2024"""

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2023-Part1'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2023-Part2'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2023-Part3'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2023-Part4'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2023-Part5'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2023-Part6'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2023-Part7'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2023-Part8'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2023-Part9'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
import os
from google.colab import drive
from tqdm import tqdm

drive.mount('/content/drive')
folder_path = '/content/drive/MyDrive/2023-Part10'

text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=20)

all_chunks = []

pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
for file_name in tqdm(pdf_files, desc="Processing PDFs"):
    file_path = os.path.join(folder_path, file_name)

    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        documents = text_splitter.split_documents(pages)
        all_chunks.extend(documents)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Processing chunks with tqdm progress bar
distinct_nodes = set()
relations = []

for i, d in tqdm(enumerate(all_chunks), total=len(all_chunks), desc="Processing Chunks"):
    graph_document = extract_and_store_graph(d)

    # Get distinct nodes
    for node in graph_document.nodes:
        distinct_nodes.add(node.id)

    # Get all relations
    for relation in graph_document.relationships:
        relations.append(relation.type)

# ditectly show the graph resulting from  the given cypher query
default_cypher = "MATCH (s)-[r:!MENTIONS]->(t) RETURN s,r,t LIMIT 500"

from google.colab import output
output.enable_custom_widget_manager()

from neo4j import GraphDatabase
from yfiles_jupyter_graphs import GraphWidget
from google.colab import output

def showGraph(cypher:str = default_cypher):
    # Directly specify the URL, username, and password
    url = "ENTER YOUR NEO4J URL"
    username = "ENTER YOUR NEO4J USERNAME"
    password = "ENTER YOUR NEO4J PASSWORD"

    # create a neo4j session to run queries
    driver = GraphDatabase.driver(
        uri = url,
        auth = (username, password))
    session = driver.session()
    widget = GraphWidget(graph = session.run(cypher).graph())
    widget.node_label_mapping = "id"
    # display(widget)
    return widget

showGraph()

# Query the knowledge graph in a RAG application
from langchain.chains import GraphCypherQAChain

graph.refresh_schema()

cypher_chain = GraphCypherQAChain.from_llm(
    graph=graph,
    cypher_llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613"),
    qa_llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613"),
    validate_cypher=True, # Validate relationship directions
    verbose=True
)

from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Tuple, List, Optional
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_community.graphs import Neo4jGraph
from langchain.document_loaders import WikipediaLoader
from langchain.text_splitter import TokenTextSplitter
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from neo4j import GraphDatabase
from yfiles_jupyter_graphs import GraphWidget
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars
from langchain_core.runnables import ConfigurableField, RunnableParallel, RunnablePassthrough

# Specify the Neo4j connection details
neo4j_url = "ENTER YOUR NEO4J URL"
neo4j_username = "ENTER YOUR NEO4J USERNAME"
neo4j_password = "ENTER YOUR NEO4J PASSWORD"

# Create a vector index from the existing graph
vector_index = Neo4jVector.from_existing_graph(
    OpenAIEmbeddings(),
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"],
    embedding_node_property="embedding",
    url=neo4j_url,
    username=neo4j_username,
    password=neo4j_password
)

print("Vector index created successfully")

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

vector_qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    chain_type="stuff",
    retriever=vector_index.as_retriever()
)
vector_qa.run(
    "Are there promising stem-cell or epi-genetic treatments in the horizon that could reassure the hesitation of my patient to start a family?"
)

# Retriever
graph.query(
    "CREATE FULLTEXT INDEX entity IF NOT EXISTS FOR (e:__Entity__) ON EACH [e.id]")

# Extract entities from text
class Entities(BaseModel):
    """Identifying information about entities."""

    names: List[str] = Field(
        ...,
        description="All the interventions related to gestationial diabetes that "
        "appear in the text",
    )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a medical expert specializing in Gestational Diabetes Mellitus interventions.",),
        ("human","Use the given format to extract information from the following input: {question}",),
    ]
)

entity_chain = prompt | llm.with_structured_output(Entities)

entity_chain.invoke({"question": "Name three interventions that reduce the risk of Gestationial Diabetes?"}).names

entity_chain.invoke({"question": "What enhances glucose metabolism?"}).names

def generate_full_text_query(input: str) -> str:
    """
    Generate a full-text search query for a given input string.

    This function constructs a query string suitable for a full-text search.
    It processes the input string by splitting it into words and appending a
    similarity threshold (~2 changed characters) to each word, then combines
    them using the AND operator. Useful for mapping entities from user questions
    to database values, and allows for some misspelings.
    """
    full_text_query = ""
    words = [el for el in remove_lucene_chars(input).split() if el]
    for word in words[:-1]:
        full_text_query += f" {word}~2 AND"
    full_text_query += f" {words[-1]}~2"
    return full_text_query.strip()

# Fulltext index query
def structured_retriever(question: str) -> str:
    """
    Collects the neighborhood of entities mentioned
    in the question
    """
    result = ""
    entities = entity_chain.invoke({"question": question})
    for entity in entities.names:
        response = graph.query(
            """CALL db.index.fulltext.queryNodes('entity', $query, {limit:2})
            YIELD node,score
            CALL {
              MATCH (node)-[r:!MENTIONS]->(neighbor)
              RETURN node.id + ' - ' + type(r) + ' -> ' + neighbor.id AS output
              UNION
              MATCH (node)<-[r:!MENTIONS]-(neighbor)
              RETURN neighbor.id + ' - ' + type(r) + ' -> ' +  node.id AS output
            }
            RETURN output LIMIT 50
            """,
            {"query": generate_full_text_query(entity)},
        )
        result += "\n".join([el['output'] for el in response])
    return result

print(structured_retriever("what are the top three factors that determine the risk of Gestationial Diabetes?"))

print(structured_retriever("Does Smartphone-Based Lifestyle Interventions have an impact on infant birth weight?"))

def retriever(question: str):
    print(f"Search query: {question}")
    structured_data = structured_retriever(question)
    unstructured_data = [el.page_content for el in vector_index.similarity_search(question)]
    final_data = f"""Structured data:
    {structured_data}
    Unstructured data:
    {"#Document ". join(unstructured_data)}
    """
    return final_data

# Condense a chat history and follow-up question into a standalone question
_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question,
in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""  # noqa: E501
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

def _format_chat_history(chat_history: List[Tuple[str, str]]) -> List:
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer

_search_query = RunnableBranch(
    # If input includes chat_history, we condense it with the follow-up question
    (
        RunnableLambda(lambda x: bool(x.get("chat_history"))).with_config(
            run_name="HasChatHistoryCheck"
        ),  # Condense follow-up question and chat into a standalone_question
        RunnablePassthrough.assign(
            chat_history=lambda x: _format_chat_history(x["chat_history"])
        )
        | CONDENSE_QUESTION_PROMPT
        | ChatOpenAI(temperature=0)
        | StrOutputParser(),
    ),
    # Else, we have no chat history, so just pass through the question
    RunnableLambda(lambda x : x["question"]),
)# Condense a chat history and follow-up question into a standalone question
_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question,
in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""  # noqa: E501
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

def _format_chat_history(chat_history: List[Tuple[str, str]]) -> List:
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer

_search_query = RunnableBranch(
    # If input includes chat_history, we condense it with the follow-up question
    (
        RunnableLambda(lambda x: bool(x.get("chat_history"))).with_config(
            run_name="HasChatHistoryCheck"
        ),  # Condense follow-up question and chat into a standalone_question
        RunnablePassthrough.assign(
            chat_history=lambda x: _format_chat_history(x["chat_history"])
        )
        | CONDENSE_QUESTION_PROMPT
        | ChatOpenAI(temperature=0)
        | StrOutputParser(),
    ),
    # Else, we have no chat history, so just pass through the question
    RunnableLambda(lambda x : x["question"]),
)

template = """Answer the question based only on the following context:
{context}

Question: {question}
Use natural language and be concise.
Answer:"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    RunnableParallel(
        {
            "context": _search_query | retriever,
            "question": RunnablePassthrough(),
        }
    )
    | prompt
    | llm
    | StrOutputParser()
)

chain.invoke({"question": "Which intervention enhances glucose metabolism?"})

chain.invoke({"question": "What is a factor of psychological stress?"})

chain.invoke(
    {
        "question": "What is gestationial diabetes?",
        "chat_history": [("What is large language model?", "A large language model is an artificial neural network used for general-purpose language generation.")],
    }
)
