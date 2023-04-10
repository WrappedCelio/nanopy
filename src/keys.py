import os
import pyblake2
from typing import List
import binascii
import nanolib

def check_seed(seed: str) -> bool:
    try:
        bytes.fromhex(seed)
        return True
    except ValueError:
        return False

def check_index(index: int) -> bool:
    return 0 <= index < 4294967296

def generateSeed() -> str:
    seed = os.urandom(32)
    return seed.hex()

def deriveSecretKey(seed: str, index: int) -> str:
    if not check_seed(seed):
        raise ValueError('Seed is not valid')
    if not check_index(index):
        raise ValueError('Index is not valid')

    seed_bytes = bytes.fromhex(seed)
    index_bytes = index.to_bytes(4, byteorder='little')

    context = pyblake2.blake2b(digest_size=32)
    context.update(seed_bytes)
    context.update(index_bytes)
    secret_key_bytes = context.digest()

    secret_key_bytes = bytearray(secret_key_bytes)

    return bytes(secret_key_bytes).hex().upper()

def derivePublicKey(private_keye: str) -> str: 
  return nanolib.get_account_public_key(private_key=private_keye).upper()

def deriveAddress(publicKey: str) -> str: 
  return nanolib.get_account_id(public_key=publicKey, prefix="nano_")
  

"""
seed = generateSeed()
pri = deriveSecretKey(seed, 0)
pub = derivePublicKey(pri)
addr = deriveAddress(pub)
print(addr, pub)
"""
