import hashlib
import json
import os
from datetime import datetime


class Blockchain:

    def __init__(self):
        self.chain = []
        self.load_chain()

    def load_chain(self):

        if os.path.exists("blockchain.json"):

            with open("blockchain.json", "r") as file:

                try:
                    self.chain = json.load(file)

                except json.JSONDecodeError:
                    self.chain = []

        if len(self.chain) == 0:
            self.create_genesis_block()

    def save_chain(self):

        with open("blockchain.json", "w") as file:
            json.dump(self.chain, file, indent=4)

    def create_genesis_block(self):

        block = {
            "index": 0,
            "timestamp": str(datetime.now()),
            "filename": "Genesis Block",
            "file_hash": "0",
            "previous_hash": "0"
        }

        block["current_hash"] = self.calculate_hash(block)

        self.chain.append(block)
        self.save_chain()

    def calculate_hash(self, block):

        block_copy = block.copy()

        if "current_hash" in block_copy:
            del block_copy["current_hash"]

        block_string = json.dumps(block_copy, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, filename, file_hash):

        previous_block = self.chain[-1]

        block = {
            "index": len(self.chain),
            "timestamp": str(datetime.now()),
            "filename": filename,
            "file_hash": file_hash,
            "previous_hash": previous_block["current_hash"]
        }

        block["current_hash"] = self.calculate_hash(block)

        self.chain.append(block)

        self.save_chain()

    def verify_file(self, filename, file_hash):

        for block in self.chain:

            if block["filename"] == filename:

                if block["file_hash"] == file_hash:
                    return True
                else:
                    return False

        return False

    def display_chain(self):

        return self.chain