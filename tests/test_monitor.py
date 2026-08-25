import pytest

from src.monitor import (
    ChainObservation,
    MonitorError,
    assess_observation,
    explorer_contract,
)

HASH_A = "0x" + "a" * 64
HASH_B = "0x" + "b" * 64


def obs(height: int, block_hash: str = HASH_A, confirmations: int = 0) -> ChainObservation:
    return ChainObservation("sky-main", height, block_hash, confirmations)


def test_pending_and_confirmed_are_derived_from_supplied_confirmations():
    assert assess_observation(obs(10, confirmations=2), required_confirmations=3) == "pending"
    assert assess_observation(obs(10, confirmations=3), required_confirmations=3) == "confirmed"


def test_height_regression_or_hash_change_is_only_a_reorg_candidate():
    prior = obs(10, HASH_A, 5)
    assert assess_observation(obs(9, HASH_B, 1), required_confirmations=3, prior=prior) == "reorg_candidate"
    assert assess_observation(obs(10, HASH_B, 1), required_confirmations=3, prior=prior) == "reorg_candidate"


def test_rejects_invalid_observation_metadata():
    with pytest.raises(MonitorError):
        assess_observation(ChainObservation("../chain", 1, HASH_A, 1), required_confirmations=1)
    with pytest.raises(MonitorError):
        assess_observation(ChainObservation("sky", -1, HASH_A, 1), required_confirmations=1)
    with pytest.raises(MonitorError):
        assess_observation(ChainObservation("sky", 1, "0x1234", 1), required_confirmations=1)
    with pytest.raises(MonitorError):
        assess_observation(obs(1), required_confirmations=0)


def test_prior_chain_must_match():
    prior = ChainObservation("other", 10, HASH_A, 2)
    with pytest.raises(MonitorError, match="same chain"):
        assess_observation(obs(11, HASH_B, 2), required_confirmations=2, prior=prior)


def test_explorer_contract_is_stable_and_truthful():
    contract = explorer_contract(obs(42, HASH_A, 7), required_confirmations=6)
    assert contract == {
        "schema": "sky.chainmonitor.explorer.v1",
        "chain": "sky-main",
        "height": 42,
        "block_hash": HASH_A,
        "confirmations": 7,
        "required_confirmations": 6,
        "status": "confirmed",
    }
