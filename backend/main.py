from fastapi import FastAPI, Query
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from pymilvus import connections, Collection

app = FastAPI()

# Connect to Milvus and load model
connections.connect("default", host="localhost", port="19530")
collection = Collection("doc_chunks")
collection.load()
model = SentenceTransformer("all-MiniLM-L6-v2")


@app.get("/search")
def search(query: str = Query(..., description="Search query")):
    query_vector = model.encode([query])
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

    results = collection.search(
        data=query_vector,
        anns_field="embedding",
        param=search_params,
        limit=2,
        output_fields=["content"]
    )

    matches = [{"score": hit.distance, "chunk": hit.entity.get("content")} for hit in results[0]]
    return {"query": query, "matches": matches}
