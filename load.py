import json
from neo4j import GraphDatabase

# --- Configuration ---
NEO4J_URI = "neo4j+s://54d3d58c.databases.neo4j.io"  
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "LQSIDLvvoUZV1vj4Bh7CtBVMy4uxQVSl1OD9WY7OTLo"
JSON_PATH = "test.json"  

# --- Neo4j Session ---
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def load_articles(tx, article):
    article_id = article.get("_id")
    title = article.get("title", "Unknown Title")

    # Create the Article node
    tx.run(
        "MERGE (a:Article {_id: $id}) "
        "SET a.title = $title",
        id=article_id, title=title
    )

    # Create Author nodes and relationships
    for author in article.get("authors", []):
        author_id = author.get("_id", author.get("name"))  # fallback if _id is missing
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

    # Create CITES relationships
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
        articles = json.load(f)
        for article in articles:
            session.write_transaction(load_articles, article)

driver.close()
