import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from hashlib import sha256

class Block:

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self._hash_block()

    def _hash_block(self):
        sha = sha256()
        sha.update( str(self.index).encode('ascii') +
                    str(self.timestamp).encode('ascii') +
                    self.data.encode('ascii') +
                    self.previous_hash.encode('ascii'))
        #print(sha.hexdigest())

        return sha.hexdigest()
