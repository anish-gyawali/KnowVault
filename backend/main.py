from fastapi import FastAPI, File, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.milvus_client import get_or_create_collection, get_embedding_model
from backend.schemas import SearchRequest
from PyPDF2 import PdfReader
import hashlib
from typing import List

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

collection = get_or_create_collection()
model = get_embedding_model()

def chunk_text(text: str, max_chars: int = 200) -> List[str]:
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

@app.get("/")
def root():
    return {"message": "Our API is running"}

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

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type == "text/plain":
        contents = (await file.read()).decode("utf-8")
    elif file.content_type == "application/pdf":
        reader = PdfReader(file.file)
        contents = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        return {"error": "Unsupported file type. Please upload a .txt or .pdf file."}

    chunks = chunk_text(contents)
    embeddings = model.encode(chunks)
    chunk_ids = [hashlib.md5(c.encode()).hexdigest()[:16] for c in chunks]
    collection.insert([chunk_ids, chunks, embeddings])
    return {"status": "success", "chunks_inserted": len(chunks)}
