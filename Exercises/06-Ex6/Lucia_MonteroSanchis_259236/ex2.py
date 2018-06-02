# Lucia Montero Sanchis
# 259236

# I need to run this code three times

from cothority import Cothority
import hashlib
import os

url = 'ws://com402.epfl.ch:7003'
genesis_id = bytes.fromhex('0d8d8f2012b4905b90dd179c060bf56b36fffed4b285067898a642347a9c7621')

full_email = b'lucia.monterosanchis@epfl.ch'

for i in range(3):
    last_block = Cothority.getBlocks(url, genesis_id)[-1]
    last_hash = last_block.Hash
    while True:
        nonce = os.urandom(32)
        data = nonce + last_hash + full_email
        attempt = hashlib.sha256(data)
        if (attempt.hexdigest()[:6] == '000000'):
            print(':)')
            # Create block
            block = Cothority.createNextBlock(last_block, data)
            # Store block
            Cothority.storeBlock(url, block)
            break
