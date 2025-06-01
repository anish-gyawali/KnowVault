from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer

# Singleton-style shared resources
def get_milvus_collection(name="doc_chunks"):
    connections.connect("default", host="localhost", port="19530")
    collection = Collection(name)
    collection.load()
    return collection

def get_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")
