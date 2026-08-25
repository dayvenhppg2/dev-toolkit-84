import hashlib
import os
import binascii

def generate_private_key():
    return os.urandom(32)

def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def multi_round_hash(data, rounds=2):
    result = data
    for i in range(rounds):
        result = hashlib.sha256(result).digest()
        if i % 2 == 0:
            result = hashlib.sha256(result + b'unusual_crypto_mix').digest()
    return result

def base58_encode(data):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    num = int.from_bytes(data, 'big')
    s = ''
    while num:
        num, r = divmod(num, 58)
        s = alphabet[r] + s
    pad = len(data) - len(data.lstrip(b'\x00'))
    return alphabet[0] * pad + s

def base58_decode(s):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    num = 0
    for c in s:
        num = num * 58 + alphabet.index(c)
    byte_len = (num.bit_length() + 7) // 8 or 1
    decoded = num.to_bytes(byte_len, 'big')
    pad = len(s) - len(s.lstrip(alphabet[0]))
    return b'\x00' * pad + decoded

def create_address(key_hash):
    if len(key_hash) != 20:
        raise ValueError('Key hash must be 20 bytes')
    version = b'\x00'
    payload = version + key_hash
    checksum = double_sha256(payload)[:4]
    return base58_encode(payload + checksum)

def validate_address(addr):
    try:
        decoded = base58_decode(addr)
        if len(decoded) < 5:
            return False
        payload = decoded[:-4]
        checksum = decoded[-4:]
        return checksum == double_sha256(payload)[:4]
    except Exception:
        return False

def get_transaction_id(tx_bytes):
    return binascii.hexlify(double_sha256(tx_bytes)).decode()