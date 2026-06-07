import os
import random

DOCS_DIR = "docs"

def load_and_chunk_documents():
    """Loads text files and chunks them by paragraph (individual reviews)."""
    all_chunks = []
    
    for filename in os.listdir(DOCS_DIR):
        if not filename.endswith(".txt"):
            continue
            
        filepath = os.path.join(DOCS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().strip()
            
        professor_id = filename.replace(".txt", "")
        
        # Slicer 2.0: Split the text wherever there is a blank line!
        reviews = text.split('\n\n')
        
        for i, review_text in enumerate(reviews):
            review_text = review_text.strip()
            
            # Only keep it if it's an actual review, not a random blank space
            if len(review_text) > 20:
                all_chunks.append({
                    "text": review_text,
                    "metadata": {
                        "source": filename,
                        "professor": professor_id,
                        "chunk_id": f"{professor_id}_{i}"
                    }
                })
            
    return all_chunks

if __name__ == "__main__":
    chunks = load_and_chunk_documents()
    print(f"✅ Successfully created {len(chunks)} total chunks.")
    print("-" * 50)
    
    # Grab 5 random chunks from the pile instead of the first 5
    sample_chunks = random.sample(chunks, 5)
    
    for i, chunk in enumerate(sample_chunks):
        print(f"RANDOM CHUNK {i+1} (Source: {chunk['metadata']['source']}):")
        print(chunk['text'])
        print("-" * 50)