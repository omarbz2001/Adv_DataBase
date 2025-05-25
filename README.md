# Neo4j Data Loading – Project Overview

##  Group Members
- Omar Bouaziz  
- Yassine Essokri

##  Project Description

This project loads a dataset of scientific articles into a Neo4j graph database. Each article may contain metadata such as title, authors, and references to other articles. The graph structure includes:

- `(:Article)` nodes for each article
- `(:Author)` nodes for each author
- `(:Author)-[:AUTHORED]->(:Article)` relationships
- `(:Article)-[:CITES]->(:Article)` relationships for references

## ⚙️ Loading Script: `load.py`

The script performs the following:

1. **Loads environment variables** using `dotenv`:
   - `NEO4J_URI`: URI of the Neo4j instance
   - `NEO4J_USER`: Username for Neo4j authentication
   - `NEO4J_PASSWORD`: Password for Neo4j authentication
   - `JSON_PATH`: Path to the JSON data file (one JSON object per line)

2. **Connects to Neo4j** using the official Neo4j Python driver (`neo4j` package).

3. **Reads and processes the JSON file** in batches of 500 articles (configurable via `BATCH_SIZE`).

4. **Creates nodes and relationships**:
   - `MERGE` statements ensure that no duplicates are created.
   - Articles are linked to authors via `AUTHORED` relationships.
   - References are linked via `CITES` relationships.


