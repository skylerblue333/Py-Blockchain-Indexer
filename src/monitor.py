"""Caller-supplied chain observation monitoring for SkyChainMonitor (#149)."""

import re
from dataclasses import dataclass
from typing import Literal

ObservationStatus = Literal["pending", "confirmed", "reorg_candidate"]
_HASH = re.compile(r"^0x[0-9a-f]{64}$")
_CHAIN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,31}$")
_MAX_HEIGHT = 2**63 - 1
_MAX_CONFIRMATIONS = 1_000_000


class MonitorError(ValueError):
    pass


@dataclass(frozen=True)
class ChainObservation:
    chain: str
    height: int
    block_hash: str
    confirmations: int


def validate_observation(observation: ChainObservation) -> ChainObservation:
    chain = observation.chain.strip().lower() if isinstance(observation.chain, str) else ""
    block_hash = observation.block_hash.strip().lower() if isinstance(observation.block_hash, str) else ""
    if not _CHAIN.fullmatch(chain):
        raise MonitorError("chain must be a bounded lowercase identifier")
    if not isinstance(observation.height, int) or isinstance(observation.height, bool) or not 0 <= observation.height <= _MAX_HEIGHT:
        raise MonitorError("height is outside the supported range")
    if not _HASH.fullmatch(block_hash):
        raise MonitorError("block_hash must be a canonical 32-byte hex hash")
    if (
        not isinstance(observation.confirmations, int)
        or isinstance(observation.confirmations, bool)
        or not 0 <= observation.confirmations <= _MAX_CONFIRMATIONS
    ):
        raise MonitorError("confirmations is outside the supported range")
    return ChainObservation(chain, observation.height, block_hash, observation.confirmations)


def assess_observation(
    observation: ChainObservation,
    *,
    required_confirmations: int,
    prior: ChainObservation | None = None,
) -> ObservationStatus:
    current = validate_observation(observation)
    if not isinstance(required_confirmations, int) or isinstance(required_confirmations, bool) or not 1 <= required_confirmations <= _MAX_CONFIRMATIONS:
        raise MonitorError("required_confirmations must be between 1 and 1000000")
    if prior is not None:
        previous = validate_observation(prior)
        if previous.chain != current.chain:
            raise MonitorError("prior observation must use the same chain")
        if current.height < previous.height:
            return "reorg_candidate"
        if current.height == previous.height and current.block_hash != previous.block_hash:
            return "reorg_candidate"
    return "confirmed" if current.confirmations >= required_confirmations else "pending"


def explorer_contract(
    observation: ChainObservation,
    *,
    required_confirmations: int,
    prior: ChainObservation | None = None,
) -> dict[str, object]:
    current = validate_observation(observation)
    status = assess_observation(current, required_confirmations=required_confirmations, prior=prior)
    return {
        "schema": "sky.chainmonitor.explorer.v1",
        "chain": current.chain,
        "height": current.height,
        "block_hash": current.block_hash,
        "confirmations": current.confirmations,
        "required_confirmations": required_confirmations,
        "status": status,
    }
