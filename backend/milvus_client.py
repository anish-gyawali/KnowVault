from pymilvus import connections, Collection, utility, CollectionSchema, FieldSchema, DataType
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "doc_chunks"

# Connect to Milvus once
def connect_milvus():
    connections.connect("default", host="localhost", port="19530")

# Get or create the collection
def get_or_create_collection():
    connect_milvus()

    if utility.has_collection(COLLECTION_NAME):
        collection = Collection(COLLECTION_NAME)
    else:
        fields = [
            FieldSchema(name="chunk_id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
        ]
        schema = CollectionSchema(fields, description="Document chunks")
        collection = Collection(name=COLLECTION_NAME, schema=schema)
        collection.create_index("embedding", {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 1024}
        })
    collection.load()
    return collection

# Reuse model instance
_model = None
def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model
