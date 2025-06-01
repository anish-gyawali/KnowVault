from sentence_transformers import SentenceTransformer
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
import hashlib

# Step 1: Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Step 2: Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 3: Prepare a sample document
document_text = """
Milvus is a high-performance vector database for embedding-based search and retrieval.
It enables storing, indexing, and searching over billions of vector embeddings.
This makes it useful in AI-powered apps like semantic search, recommendation engines, and RAG pipelines.
"""

# Step 4: Chunk the document
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

chunks = chunk_text(document_text)

# Step 5: Embed the chunks
embeddings = model.encode(chunks)

# Step 6: Define Milvus collection
collection_name = "doc_chunks"
fields = [
    FieldSchema(name="chunk_id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
    FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
]
schema = CollectionSchema(fields, description="Document chunks")
collection = Collection(name=collection_name, schema=schema)

# Step 7: Create index
collection.create_index("embedding", {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 1024}
})
print("Created doc_chunks collection and index")

# Step 8: Insert data
chunk_ids = [hashlib.md5(c.encode()).hexdigest()[:16] for c in chunks]
collection.insert([chunk_ids, chunks, embeddings])
collection.load()
print(f"Inserted {len(chunks)} chunks into Milvus")
