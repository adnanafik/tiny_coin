import datetime as date
from block.block import Block

import json

class Chain:

    def __init__(self):
        self.chain = []

    def add_genesis_block(self, genesis_block):
        self.chain.append(genesis_block)

        last_block = self.chain[-1]
        return last_block

    def add_block(self, last_block, target_hash, nonce, data):

        block = Block(
            last_block.index+1,
            target_hash,
            nonce,
            date.datetime.now(),
            data,
            last_block.hash)

        self.chain.append(block)

        # Return last block in the chain
        return self.chain[-1]

    def block_from_other_node(self,
                              prev_block,
                              index,
                              timestamp,
                              target_hash,
                              nonce,
                              data,
                              block_hash):

        block = Block(
            index,
            target_hash,
            nonce,
            timestamp,
            data,
            prev_block.hash,
            block_hash)

        self.chain.append(block)

        last_block = self.chain[-1]

        return last_block

    def get_last_block(self):

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
    def to_json(self):
        chain_in_json = self.chain
        blocklist = []

        for i in range(len(self.chain)):
            block = chain_in_json[i]

            #print(json.dumps(block))

            # Get the block in json fotmat
            block_in_json = block.to_json()

            blocklist.append(block_in_json)

        return blocklist

    def find_block(self, previous_hash):

        chain_len = len(self.chain)
        for i in range(0, chain_len):
            if self.chain[i].hash == previous_hash:
                print('Found the previous hash for this new block')
                return self.chain[i]
        return None

    def _validate(self, block_chain):
        if len(block_chain) == 0:
            return True

        if len(block_chain) == 1:
            return True

        chain_len = len(block_chain)
        for i in range(0, chain_len-1):
            if block_chain[i].hash != block_chain[i+1].previous_hash:
                print('Invalid chain')
                return False
        return True

    def load_chain_from_list(self, block_chain_list):
        # Empty existing chain
        self.chain[:] = []

        chain_len = len(block_chain_list)
        #print(block_chain_list)

        for i in range(0, chain_len):
            block = Block(
                block_chain_list[i]['index'],
                block_chain_list[i]['target_hash'],
                block_chain_list[i]['nonce'],
                block_chain_list[i]['timestamp'],
                block_chain_list[i]['data'],
                block_chain_list[i]['previous_hash'],
                block_chain_list[i]['hash'])

            #print(block_chain_list[i]['hash'])
            self.chain.append(block)

    def _load(self, block_chain):

        # Empty existing chain
        self.chain = block_chain

    def is_valid(self):
        return self._validate(self.chain)

    def accept_existing_chain(self, existing_chain):
        # Convert the JSON object to a Python dictionary
        #tmp_block_chain  = json.loads(existing_chain)

        # First validate the chain before accepting it
        if(self._validate(existing_chain.chain)):

            self._load(existing_chain.chain)

            return True
        else:
            return False
