import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path="chroma_db")

def retrieve_relevant_chunks(question, n_results=5):
    # Convert the question to an embedding
    question_embedding = model.encode([question]).tolist()
    
    # Get the collection we created in indexer
    collection = client.get_collection("pdf_collection")
    
    # Find the most similar chunks
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=n_results
    )
    
    
    chunks = results['documents'][0]

    metadatas = results['metadatas'][0]
    sources = list(set([m['source'] for m in metadatas]))  # unique sources only
    
    return chunks , sources