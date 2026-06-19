"""
Py-Blockchain-Indexer: Indexes and queries blockchain block data
"""
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Py-Blockchain-Indexer", version="3.0.0")

blocks = []
class Block(BaseModel):
    hash: str
    height: int
    tx_count: int

@app.post("/api/v1/blocks")
def index_block(b: Block):
    blocks.append(b.dict())
    blocks.sort(key=lambda x: x["height"])
    return {"status": "indexed", "height": b.height}

@app.get("/api/v1/blocks/latest")
def get_latest():
    if not blocks:
        raise HTTPException(status_code=404, detail="No blocks")
    return blocks[-1]


@app.get("/health")
def health():
    return {"status": "healthy", "service": "Py-Blockchain-Indexer", "timestamp": int(time.time())}
