import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_and_chunk_documents

# 1. Initialize the embedding model (This translates text to numbers)
print("Loading embedding model (this might take a few seconds)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Initialize ChromaDB (This is the vault where we store the numbers)
# PersistentClient saves the database to a local folder so we don't rebuild it every time
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name="rmp_reviews",
    metadata={"hnsw:space": "cosine"}  # <-- This tells it to use Cosine Distance
)
def build_database():
    """Fetches chunks from ingest.py, embeds them, and stores them in ChromaDB."""
    print("Fetching chunks from ingest.py...")
    chunks = load_and_chunk_documents()
    
    # ChromaDB requires us to separate our data into specific lists
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    ids = [chunk["metadata"]["chunk_id"] for chunk in chunks]
    
    print(f"Translating {len(chunks)} chunks into math and saving to database...")
    embeddings = model.encode(documents).tolist()
    
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    print("✅ Database successfully built!")

def retrieve_chunks(query, top_k=5):
    """Takes a user query, embeds it, and finds the closest matching chunks."""
    # Convert the user's question into the same math format
    query_embedding = model.encode([query]).tolist()
    
    # Search the vault for the top_k closest matches
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    return results

if __name__ == "__main__":
    # Check if the database is empty. If it is, build it!
    if collection.count() == 0:
        build_database()
    else:
        print(f"Database already exists and contains {collection.count()} chunks.")
        
    # --- MILESTONE 4 MULTI-TEST ---
    # We put your evaluation questions into a list to test them all at once
    test_queries = [
        "Who is the highest rated professor in the Computer Science Department?",
        "Which Professor gives the most work?",
        "Numerical Methods professor Mitchell",
        "What are the main complaints students have about Simina Fluture?",
        "Are Matthew Fried's lectures mandatory to attend?"
    ]
    
    # Loop through each question
    for test_query in test_queries:
        print(f"\n" + "="*70)
        print(f"🔍 TEST QUERY: '{test_query}'")
        print("="*70)
        
        # Retrieving top 3 chunks to keep the terminal readable
        results = retrieve_chunks(test_query, top_k=3)
        
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            source = results['metadatas'][0][i]['source']
            distance = results['distances'][0][i]
            
            print(f"RESULT {i+1} (Source: {source} | Score: {distance:.4f})")
            print(f"{doc}\n")