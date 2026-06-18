import logging
import hashlib
import time

logging.basicConfig(level=logging.INFO)

class MockBlockchainNode:
    def get_latest_block(self):
        # Simulate fetching a block
        block_data = f"BlockData-{time.time()}"
        block_hash = hashlib.sha256(block_data.encode()).hexdigest()
        return {"height": int(time.time() % 1000000), "hash": block_hash, "tx_count": 42}

class Indexer:
    def __init__(self):
        self.node = MockBlockchainNode()
        self.db = {}

    def sync(self, count=3):
        logging.info("Starting blockchain sync...")
        for _ in range(count):
            block = self.node.get_latest_block()
            self.db[block['height']] = block
            logging.info(f"Indexed Block #{block['height']} - Hash: {block['hash'][:10]}... - TXs: {block['tx_count']}")
            time.sleep(0.5)
        logging.info(f"Sync complete. DB size: {len(self.db)} blocks.")

if __name__ == "__main__":
    indexer = Indexer()
    indexer.sync(5)