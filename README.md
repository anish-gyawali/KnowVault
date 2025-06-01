# KnowVault

KnowVault is a Retrieval-Augmented Generation (RAG) application in progress. This project sets up a local [Milvus](https://milvus.io) vector database using Docker and performs vector similarity search via Python (`pymilvus`).

## ✅ Features (Completed So Far)

- [x] Local Milvus setup via Docker (Milvus, Etcd, MinIO)
- [x] Python connection using `pymilvus`
- [x] Created `test_collection` for storing float vectors
- [x] Inserted sample vectors and searched using similarity (L2)
- [x] Persistent volume storage

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
├── milvus/                 # Docker-compose setup for Milvus
│   └── volumes/            # Persisted Milvus data
├── venv/                   # Python virtual environment (ignored in Git)
├── milvus_test.py          # Milvus test script with dummy data
├── requirements.txt        # Python dependencies
├── .gitignore              # Git exclusions
└── README.md               # This file
```
