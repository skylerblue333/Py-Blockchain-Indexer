import re
import threading
from typing import Literal

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Sky Chain Catalog", version="0.1.0")

MAX_BLOCKS = 10_000
MAX_HEIGHT = 2**63 - 1
MAX_TX_COUNT = 1_000_000
BLOCK_HASH = re.compile(r"^0x[0-9a-fA-F]{64}$")


class BlockRecord(BaseModel):
    block_hash: str
    height: int = Field(ge=0, le=MAX_HEIGHT)
    tx_count: int = Field(ge=0, le=MAX_TX_COUNT)
    timestamp: int | None = Field(default=None, ge=0, le=MAX_HEIGHT)

    @field_validator("block_hash")
    @classmethod
    def validate_hash(cls, value: str) -> str:
        value = value.strip().lower()
        if not BLOCK_HASH.fullmatch(value):
            raise ValueError("block_hash must be 0x followed by 64 hexadecimal characters")
        return value


class IndexResult(BaseModel):
    status: Literal["indexed", "existing"]
    height: int
    block_hash: str


blocks_by_height: dict[int, BlockRecord] = {}
height_by_hash: dict[str, int] = {}
catalog_lock = threading.Lock()


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "sky-chain-catalog"}


@app.get("/readyz")
def readyz() -> dict[str, int | str]:
    with catalog_lock:
        indexed = len(blocks_by_height)
    return {"status": "ready", "capacity": MAX_BLOCKS, "indexed": indexed}


@app.post("/v1/blocks", response_model=IndexResult, status_code=201)
def index_block(block: BlockRecord, response: Response) -> IndexResult:
    with catalog_lock:
        existing = blocks_by_height.get(block.height)
        if existing is not None:
            if existing == block:
                response.status_code = 200
                return IndexResult(
                    status="existing", height=block.height, block_hash=block.block_hash
                )
            raise HTTPException(
                status_code=409,
                detail="height already contains a different block; reorg handling is explicit",
            )
        other_height = height_by_hash.get(block.block_hash)
        if other_height is not None:
            raise HTTPException(
                status_code=409,
                detail=f"block hash is already indexed at height {other_height}",
            )
        if len(blocks_by_height) >= MAX_BLOCKS:
            raise HTTPException(status_code=503, detail="in-memory block capacity reached")
        blocks_by_height[block.height] = block
        height_by_hash[block.block_hash] = block.height
    return IndexResult(status="indexed", height=block.height, block_hash=block.block_hash)


@app.get("/v1/blocks/latest", response_model=BlockRecord)
def latest_block() -> BlockRecord:
    with catalog_lock:
        if not blocks_by_height:
            raise HTTPException(status_code=404, detail="no blocks indexed")
        return blocks_by_height[max(blocks_by_height)]


@app.get("/v1/blocks/{height}", response_model=BlockRecord)
def get_block(height: int) -> BlockRecord:
    if height < 0 or height > MAX_HEIGHT:
        raise HTTPException(status_code=422, detail="height is outside the supported range")
    with catalog_lock:
        block = blocks_by_height.get(height)
    if block is None:
        raise HTTPException(status_code=404, detail="block not found")
    return block
