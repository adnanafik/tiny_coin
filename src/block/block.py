import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from hashlib import sha256

import json

class Block:

    def __init__(self, index, target_hash, nonce, timestamp, data, previous_hash, current_hash=None):
        self.index = index
        self.target_hash = target_hash
        self.nonce =  nonce
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        # Only hash if the hash of this block was not provided
        if (current_hash):
            self.hash = current_hash
        else:
            self.hash = self._hash_block()

    def _hash_block(self):
        sha = sha256()

        sha.update( str(self.index).encode('ascii') +
                    self.target_hash.encode('ascii') +
                    str(self.nonce).encode('ascii') +
                    str(self.timestamp).encode('ascii') +
                    str(self.data).encode('ascii') +
                    self.previous_hash.encode('ascii'))
        #print(sha.hexdigest())

        return sha.hexdigest()

    def to_json(self):
        return {
            "target_hash": self.target_hash,
            "hash": self.hash,
            "index": self.index,
            "timestamp": str(self.timestamp),
            "nonce": str(self.nonce),
            "data": self.data,
            "previous_hash": self.previous_hash
          }
