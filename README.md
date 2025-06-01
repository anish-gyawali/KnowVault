# KnowVault

KnowVault is a Retrieval-Augmented Generation (RAG) application in progress. This project sets up a local [Milvus](https://milvus.io) vector database using Docker and performs vector similarity search via Python (`pymilvus`).

## 🔧 Local Setup Instructions

### Prerequisites

- Python 3.9+
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- VS Code (recommended)

---

### 🚀 Getting Started

1. **Clone the repo** and open in VS Code:

```bash
git clone https://github.com/YOUR_USERNAME/KnowVault.git
cd KnowVault
````

2. **Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

4. **Start Milvus via Docker Compose:**

```bash
cd milvus
docker compose up -d
```

> This runs Milvus, Etcd, and MinIO with persistent volumes.

---

### ✅ Test the Connection

From the project root:

```bash
python milvus_test.py
```

You should see output like:

```
Connected to Milvus
Created collection: test_collection
Index created
Inserted vectors
Search results:
 - id: 0, distance: 0.0
 - id: 1, distance: ...
```

## 📁 Project Structure

```
KnowVault/
├── backend/
│   ├── __init__.py                
│   ├── main.py                # FastAPI backend entry point
│   └── milvus_client.py       # Reusable code to connect to Milvus and load embedding model
│
├── milvus/
│   ├── docker-compose.yml     # Milvus standalone setup with Docker
│   └── volumes/               # Persistent volumes for Milvus (etcd, minio, etc.)
│
├── venv/                      # Python virtual environment (should be in .gitignore)
│
├── doc_ingest.py              # Script to chunk, embed, and insert documents into Milvus
├── query_doc.py               # Script to query embedded vectors from Milvus
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
```
---

### 🔍 Inspecting Milvus Data with `milvus_cli`

To explore the data inside Milvus using the CLI:

#### ✅ Start the CLI

```bash
milvus_cli
```

#### ✅ Connect to your local Milvus instance

```bash
connect -uri tcp://127.0.0.1:19530
```

#### ✅ List all collections

```bash
list collections
```

#### ✅ Query data from a collection

```bash
query
```

Then follow the interactive prompts:

```
Collection name: doc_chunks
The query expression: chunk_id != ''
A list of fields to return (split by "," if multiple) []: chunk_id, content
timeout []:
Guarantee timestamp []:
Graceful time []:
```

> 🔹 Just press `Enter` for the optional fields unless you're using advanced consistency settings.
