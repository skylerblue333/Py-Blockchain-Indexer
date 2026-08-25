# Changelog

## 0.1.0 — Engineering beta

- replace conflicting live-RPC and local-list paths with one deterministic block catalog service
- validate canonical 32-byte block hashes, heights, transaction counts and optional timestamps
- add bounded in-memory capacity and atomic indexing
- make exact duplicate submissions idempotent
- reject height/hash conflicts instead of silently rewriting chain history
- add latest and by-height queries plus health/readiness endpoints
- replace generic fake Node build/test scaffolding with Python compile, Ruff, pytest and dependency-audit gates
- add non-root container packaging and runtime liveness smoke verification
- document explicit reorganization, consensus, persistence and integration boundaries

No RPC connectivity, consensus/finality verification, automatic reorg handling, durable indexing, HA, or production deployment is claimed.
