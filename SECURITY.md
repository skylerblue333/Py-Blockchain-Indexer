# Security Policy

## Supported status

Sky Chain Catalog is an **engineering beta**. CI verifies Python compilation, linting, tests, dependency audit, container build, non-root execution, and a liveness smoke check. These checks do not establish production security or deployment readiness.

## Current boundaries

The service validates block-summary shape, hash format, numeric bounds, duplicate/conflict behavior, and in-memory capacity. It does not authenticate submitters, verify blockchain consensus/finality, connect to RPC nodes, validate signatures or proofs, persist history, enforce tenant isolation, or provide durable audit logs.

Treat submitted block summaries as untrusted observations unless a separately reviewed ingestion layer establishes chain identity and authenticity. Do not store node credentials, private RPC URLs, signing keys, wallet secrets, or customer data in this repository.

## Reporting

Report suspected vulnerabilities privately through GitHub security reporting when available. Do not include private node endpoints, credentials, wallet material, or sensitive chain-monitoring data in public issues.
