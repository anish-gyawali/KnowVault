from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class QueryResponseChunk(BaseModel):
    chunk_id: str
    content: str
    score: float

class SearchRequest(BaseModel):
    query: str
    top_k: int = 2
