# SkyChainMonitor (#149)

Status: **engineering beta / caller-supplied observation monitor**.

SkyChainMonitor extends the network-independent Sky Chain Catalog with deterministic assessment of chain observations supplied by a caller. It does not query nodes or infer blockchain truth independently.

## Implemented behavior

- bounded chain identifier, height, canonical block hash, and confirmation count validation
- `pending` versus `confirmed` classification against a caller-selected confirmation threshold
- `reorg_candidate` classification when a supplied observation moves below the prior height or changes the block hash at the same height
- same-chain validation for comparison observations
- stable `sky.chainmonitor.explorer.v1` contract for explorer-style consumers

## SKYCOIN4444 integration

`explorer_contract()` provides a narrow read contract for a future SkyExplorerAPI or integration layer. It contains only validated caller-supplied observation metadata and the deterministic assessment result.

## Security and truth boundary

The module does **not** connect to RPC endpoints, verify consensus, verify signatures, establish finality, discover reorgs, fetch transactions/logs, submit transactions, hold keys, or execute blockchain actions. A `confirmed` result means only that the supplied confirmation count meets the configured threshold; it is not independent proof of chain finality. A `reorg_candidate` result is a comparison signal, not automatic reorg handling.
