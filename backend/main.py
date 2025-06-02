from fastapi import FastAPI, Query
from backend.milvus_client import get_or_create_collection, get_embedding_model
from backend.schemas import SearchRequest
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

@app.post("/search")
def search_docs(request: SearchRequest):
    query_vector = model.encode([request.query])
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

    results = collection.search(
        data=query_vector,
        anns_field="embedding",
        param=search_params,
        limit=request.top_k,
        output_fields=["content"]
    )

    matches = [{"score": hit.distance, "chunk": hit.entity.get("content")} for hit in results[0]]
    return {"query": request.query, "matches": matches}