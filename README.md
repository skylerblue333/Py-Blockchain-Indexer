# Sky Chain Catalog — Python Engineering Beta

Sky Chain Catalog is a small FastAPI service for registering and querying validated blockchain block summaries supplied by a trusted upstream component. It is deliberately network-independent and does not pretend to verify a chain by itself.

## Status

**Engineering beta.** The service validates canonical 32-byte hexadecimal block hashes, bounded heights and transaction counts, enforces a 10,000-block in-memory capacity, makes duplicate indexing idempotent, rejects height/hash conflicts, and exposes health/readiness plus latest/by-height queries.

It does **not** connect to an RPC node, verify consensus or finality, automatically process reorganizations, persist history, index transactions/logs, provide explorer analytics, authenticate tenants, provide HA, or establish production deployment readiness.

## API

- `GET /healthz` — process liveness.
- `GET /readyz` — reports catalog capacity and indexed count.
- `POST /v1/blocks` — register a block summary.
- `GET /v1/blocks/latest` — highest indexed height.
- `GET /v1/blocks/{height}` — lookup by height.

Example block:

```json
{
  "block_hash": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "height": 100,
  "tx_count": 5,
  "timestamp": 1724450000
}
```

Submitting the exact same block twice is idempotent. Submitting a different block at an existing height returns HTTP 409 instead of silently rewriting history. Reorganization handling must be implemented explicitly by a future trusted ingestion layer.

## Run locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 127.0.0.1 --port 8000
```

## Verify

```bash
pip install pip-audit
python -m compileall -q src tests
ruff check src tests
pytest -q
pip-audit -r requirements.txt
docker build -t sky-chain-catalog .
docker run --rm --entrypoint=id sky-chain-catalog -u
```

The container is expected to run as UID `10001`. CI also starts the image and verifies `/healthz`.

## Architecture

`src/main.py` is the canonical service. Block summaries are stored in bounded process-local maps keyed by height and hash and protected by a lock so duplicate/conflict/capacity checks are atomic. State disappears when the process exits.

A real chain ingestion adapter should live behind a separately reviewed RPC/network boundary. That adapter is responsible for node authentication, transport security, chain identity, finality policy, reorganization handling, retry/backfill behavior, and independent validation before submitting summaries here.

## SKYCOIN4444 integration

SKYCOIN4444 can use this component as a stable normalized block-summary boundary for explorer, analytics, or monitoring prototypes. The catalog should consume already-validated upstream observations rather than embedding node credentials or network access into this reusable repository.

## Security and operational boundaries

This service does not verify that submitted blocks are authentic. It has no authentication, authorization, durable audit history, tenant isolation, rate limiting, persistent database, or consensus validation. Do not expose it as an authoritative chain index without a trusted ingestion and access-control layer.

## License

See `LICENSE`.
