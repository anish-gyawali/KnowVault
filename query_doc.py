from backend.milvus_client import get_or_create_collection, get_embedding_model

collection = get_or_create_collection()
model = get_embedding_model()


# Step 3: Accept user question
query = input("Ask something: ")

# Step 4: Embed the query
query_vector = model.encode([query])

# Step 5: Search in Milvus
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = collection.search(
    data=query_vector,
    anns_field="embedding",
    param=search_params,
    limit=2,
    output_fields=["content"]
)

# Step 6: Display the results
print("\nTop Matches:")
for hit in results[0]:
    print(f"- Score: {hit.distance:.4f}")
    print(f"  Chunk: {hit.entity.get('content')}\n")
