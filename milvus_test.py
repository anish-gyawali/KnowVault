from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
import random

# 1. Connect to Milvus
connections.connect("default", host="localhost", port="19530")
print("Connected to Milvus")

# 2. Define collection schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=5)
]
schema = CollectionSchema(fields, description="Test collection")

# 3. Create the collection
collection = Collection(name="test_collection", schema=schema)
print("Created collection: test_collection")

# 4. Create an index
index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 1024},
}
collection.create_index("embedding", index_params)
print("Index created")

# 5. Insert dummy vectors
ids = [i for i in range(5)]
vectors = [[random.random() for _ in range(5)] for _ in range(5)]
collection.insert([ids, vectors])
print("Inserted vectors")

# 6. Load and search
collection.load()
search_vector = [vectors[0]]
results = collection.search(
    search_vector, "embedding", param={"metric_type": "L2", "params": {"nprobe": 10}}, limit=2
)

print("Search results:")
for result in results[0]:
    print(f" - id: {result.id}, distance: {result.distance}")
