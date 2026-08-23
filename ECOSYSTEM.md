# Ecosystem Integration

**Role:** blockchain read/indexing boundary.

**Foundation:** Web3.py and established chain SDK behavior. Do not implement custom cryptography or consensus logic here.

**Provides:** normalized block/transaction/token data to wallet, portfolio, analytics, and protocol services.

**Production requirements:** chain/network allowlists, RPC failover, reorg handling, cursor checkpoints, idempotent indexing, provenance, rate limits, and telemetry.
