import hashlib
import json
import time
import os


class Blockchain:

    def __init__(self):
        self.chain = []
        self.load_chain()

    def create_genesis_block(self):
        return {
            "index": 0,
            "timestamp": time.time(),
            "data": "Genesis Block",
            "previous_hash": "0",
            "hash": self.hash_block(0, time.time(), "Genesis Block", "0")
        }

    def add_block(self, data):
        previous_block = self.chain[-1] if self.chain else self.create_genesis_block()
        index = len(self.chain)
        timestamp = time.time()
        previous_hash = previous_block["hash"]

        block = {
            "index": index,
            "timestamp": timestamp,
            "data": data,
            "previous_hash": previous_hash,
            "hash": self.hash_block(index, timestamp, data, previous_hash)
        }

        self.chain.append(block)
        self.save_chain()

    def hash_block(self, index, timestamp, data, previous_hash):
        block_string = f"{index}{timestamp}{data}{previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def save_chain(self, filename="blockchain.json"):
        with open(filename, "w") as f:
            json.dump(self.chain, f, indent=4)

    def load_chain(self, filename="blockchain.json"):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                self.chain = json.load(f)
        else:
            self.chain = [self.create_genesis_block()]
            self.save_chain(filename)

    # ✅ FIXED: Now inside class
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current["previous_hash"] != previous["hash"]:
                return False

            recalculated_hash = self.hash_block(
                current["index"],
                current["timestamp"],
                current["data"],
                current["previous_hash"]
            )

            if current["hash"] != recalculated_hash:
                return False

        return True

    # ✅ FIXED: Now inside class
    def delete_block(self, index):
        if index == 0:
            return  # Don't delete genesis

        self.chain = [block for block in self.chain if block["index"] != index]

        # Recalculate full chain
        for i in range(1, len(self.chain)):
            self.chain[i]["index"] = i
            self.chain[i]["previous_hash"] = self.chain[i - 1]["hash"]
            self.chain[i]["hash"] = self.hash_block(
                self.chain[i]["index"],
                self.chain[i]["timestamp"],
                self.chain[i]["data"],
                self.chain[i]["previous_hash"]
            )

        self.save_chain()