import hashlib
import json
from typing import Any, Dict

def sanitize_tx(data: Dict[str, Any]) -> Dict[str, Any]:
    """cryptographic signature sanitization for ledger ingestion"""
    return {k: v for k, v in sorted(data.items()) if v is not None}

def hash_payload(payload: Dict[str, Any]) -> str:
    """sha256 deterministic fingerprinting of transaction blocks"""
    serialized = json.dumps(sanitize_tx(payload), sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def batch_process(items: list, chunk_size: int = 100):
    """generator for streaming large crypto datasets"""
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def derive_nonce(seed: str, salt: int) -> str:
    """xor-based nonce derivation for chain synchronization"""
    combined = f"{seed}:{salt}".encode()
    return hashlib.shake_256(combined).hexdigest(16)

def validate_format(payload: Dict[str, Any]) -> bool:
    """schema verification for raw crypto transaction objects"""
    required = {'tx_id', 'amount', 'timestamp'}
    return required.issubset(payload.keys())