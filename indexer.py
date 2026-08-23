"""Web3.py blockchain indexing foundation; network writes are intentionally absent."""
import os
from web3 import Web3

RPC_URL = os.getenv("RPC_URL", "http://localhost:8545")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def block_summary(block_number: int | None = None) -> dict:
    number = block_number if block_number is not None else w3.eth.block_number
    block = w3.eth.get_block(number)
    return {"number": block.number, "hash": block.hash.hex(), "timestamp": block.timestamp, "transactions": len(block.transactions)}

if __name__ == "__main__":
    print(block_summary())
