# Contributing to Sky Chain Catalog

## Development setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pip-audit
```

## Verification

```bash
python -m compileall -q src tests
ruff check src tests
pytest -q
pip-audit -r requirements.txt
docker build -t sky-chain-catalog .
docker run --rm --entrypoint=id sky-chain-catalog -u
```

## Scope and correctness

- Keep the service network-independent unless a separately reviewed ingestion boundary is deliberately introduced.
- Add tests for hash/height validation, duplicate behavior, conflicts, reorganization policy, and capacity changes.
- Do not silently rewrite an indexed height when a different block is submitted.
- Do not claim consensus verification, finality, durable indexing, explorer completeness, HA, or production deployment without implementation and evidence.
- Never add node credentials or private RPC endpoints to committed configuration.

## Pull requests

1. Create a focused branch.
2. Make the smallest coherent change.
3. Run the verification commands above.
4. Document changes to chain/reorg/security boundaries.
5. Open a pull request with a truthful maturity status.

## License

See `LICENSE`.
