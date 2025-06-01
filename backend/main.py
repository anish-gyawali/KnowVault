from fastapi import FastAPI, Query
from backend.milvus_client import get_milvus_collection, get_embedding_model

app = FastAPI()
collection = get_milvus_collection()
model = get_embedding_model()


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
