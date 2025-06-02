from fastapi import FastAPI, Query
from backend.milvus_client import get_or_create_collection, get_embedding_model
from backend.schemas import QueryRequest, QueryResponseChunk
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

collection = get_or_create_collection()
model = get_embedding_model()


@app.get("/")
def root():
    return {"message":"Our API is running"}

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

@app.post("/search", response_model=list[QueryResponseChunk])
def search_docs(req: QueryRequest):
    embedding = model.encode([req.query])[0]

    search_params = {
        "data": [embedding],
        "anns_field": "embedding",
        "param": {"metric_type": "L2", "params": {"nprobe": 10}},
        "limit": 3,
        "output_fields": ["chunk_id", "content"]
    }

    results = collection.search(**search_params)

    matches = results[0]
    return [
        {
            "chunk_id": match.entity.get("chunk_id"),
            "content": match.entity.get("content"),
            "score": match.distance
        }
        for match in matches
    ]