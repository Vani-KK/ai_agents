import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="chroma_db")

def index_pdf(pdf_path):
    # Step 1: Read the PDF
    print("Reading PDF...")
    reader = PdfReader(pdf_path)
    
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    
    print(f"Extracted {len(full_text)} characters from PDF")
    
    # Step 2: Split into chunks
    print("Splitting into chunks...")
    chunks = []
    chunk_size = 500  
    overlap = 50      
    
    for i in range(0, len(full_text), chunk_size - overlap):
        chunk = full_text[i:i + chunk_size]
        if len(chunk) > 100:  # ignore tiny leftover chunks
            chunks.append(chunk)
    
    print(f"Created {len(chunks)} chunks")
    
    # Step 3: Store in ChromaDB
    print("Creating embeddings and storing in ChromaDB...")
    
    # Delete existing collection if it exists (fresh start each time)
    try:
        client.delete_collection("pdf_collection")
    except:
        pass
    
    collection = client.create_collection("pdf_collection")
    
    # Convert chunks to embeddings and store
    embeddings = model.encode(chunks).tolist()
    
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    
    print(f"Successfully indexed {len(chunks)} chunks!")
    return len(chunks)