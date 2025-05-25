# --- This was done by Omar Bouaziz and Yassine Essokri ---

import json
from neo4j import GraphDatabase
import os, dotenv
import time

dotenv.load_dotenv()

# --- Configuration ---
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
JSON_PATH = os.getenv("JSON_PATH")
BATCH_SIZE = 500  

# --- Neo4j Session ---
print(f"Connecting to Neo4j")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
print(f"Connected to Neo4j at {NEO4J_URI}")
start_time = time.time()
def load_articles_batch(tx, articles_batch):
    for article in articles_batch:
        article_id = article.get("id")
        if article_id is None:
            print("Skipping article with missing _id")
            return  
        title = article.get("title", "Unknown Title")

        tx.run(
            "MERGE (a:Article {_id: $id}) "
            "SET a.title = $title",
            id=article_id, title=title
        )

        for author in article.get("authors", []):
            author_id = author.get("_id", author.get("name"))
            name = author.get("name")
            if not name:
                continue
            tx.run(
                "MERGE (au:Author {_id: $aid}) "
                "SET au.name = $name "
                "WITH au "
                "MATCH (ar:Article {_id: $article_id}) "
                "MERGE (au)-[:AUTHORED]->(ar)",
                aid=author_id, name=name, article_id=article_id
            )

        for ref_id in article.get("references", []):
            tx.run(
                "MERGE (ref:Article {_id: $ref_id}) "
                "WITH ref "
                "MATCH (ar:Article {_id: $article_id}) "
                "MERGE (ar)-[:CITES]->(ref)",
                ref_id=ref_id, article_id=article_id
            )

# --- Main Execution ---
with driver.session() as session:
    
    with open(JSON_PATH, "r") as f:
        batch = []
        for line in f:
            if line.strip(): 
                article = json.loads(line)
                batch.append(article)
                if len(batch) >= BATCH_SIZE:
                    session.execute_write(load_articles_batch, batch)
                    batch = []

        
        if batch:
            session.write_transaction(load_articles_batch, batch)
            print(f"Loaded final batch of {len(batch)}")
end_time = time.time()
print(f"All articles loaded successfully.")
print(f"Total loading time: {end_time - start_time:.2f} seconds")
driver.close()

