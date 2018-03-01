import datetime as date
from block.block import Block

class Chain:

    def __init__(self):
        self.chain = []

    def add_genesis_block(self, genesis_block):
        self.chain.append(genesis_block)

        last_block = self.chain[-1]
        return last_block

    def add_block(self, last_block, data):

        block = Block(last_block.index+1, date.datetime.now(), data, last_block.hash)

        self.chain.append(block)

        last_block = self.chain[-1]
        return last_block

    def print_chain_data(self):
        for block in self.chain:
            print('index={}, timestamp={}, data={}, prev_hash={}, hash={}'.format(
                            block.index,
                            block.timestamp,
                            block.data,
                            block.previous_hash,
                            block.hash))
    def validate(self):
        if len(self.chain) == 0:
            return 0

        if len(self.chain) == 1:
            return 0

        chain_len = len(self.chain)
        for i in range(0, chain_len-1):
            if self.chain[i].hash != self.chain[i+1].previous_hash:
                print('Invalid chain')
                return -1
        return 0
