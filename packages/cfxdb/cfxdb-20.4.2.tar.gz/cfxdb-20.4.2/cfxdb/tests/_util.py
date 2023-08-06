##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

import hashlib
import os

import multihash


def _gen_ipfs_hash():
    # IPFS uses sha2-256 and B58 string encoding, eg "QmevbQAb6L7MsZUxqsspYREqMhMqaaV6arvF4UytgdsSfX"
    data = os.urandom(100)
    digest = hashlib.sha256(data).digest()
    hash = multihash.encode(digest, 'sha2-256')
    return multihash.to_b58_string(hash)
