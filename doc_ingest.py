import os
import hashlib
import fitz 
from sentence_transformers import SentenceTransformer
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from backend.milvus_client import get_or_create_collection, get_embedding_model


# Read .txt and .pdf files
def read_txt_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf_file(path):
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def read_document(path):
    if path.endswith(".txt"):
        return read_txt_file(path)
    elif path.endswith(".pdf"):
        return read_pdf_file(path)
    else:
        raise ValueError(f"Unsupported file type: {path}")


# Chunk long text into smaller pieces
def chunk_text(text, max_chars=200):
    sentences = text.strip().split('.')
    chunks = []
    current = ''
    for s in sentences:
        if len(current + s) > max_chars:
            chunks.append(current.strip())
            current = s + '.'
        else:
            current += s + '.'
    if current.strip():
        chunks.append(current.strip())
    return chunks


# Setup
collection_name = "doc_chunks"
collection = get_or_create_collection()
model = get_embedding_model()

# Process documents in `documents/` folder
doc_folder = "documents"
all_chunks = []
all_ids = []

for filename in os.listdir(doc_folder):
    path = os.path.join(doc_folder, filename)
    try:
        content = read_document(path)
        chunks = chunk_text(content)
        embeddings = model.encode(chunks)

        # Hash each chunk as ID
        chunk_ids = [hashlib.md5((filename + c).encode()).hexdigest()[:16] for c in chunks]

        collection.insert([chunk_ids, chunks, embeddings])
        all_chunks.extend(chunks)
        all_ids.extend(chunk_ids)
        print(f"Ingested {len(chunks)} chunks from {filename}")
    except Exception as e:
        print(f"Failed to process {filename}: {e}")

collection.load()
print(f"Finished ingesting {len(all_chunks)} chunks total.")
