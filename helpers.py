from typing import List, Dict, Union, Callable, Any
import hashlib

def generate_crypto_hash(data: str, salt: str = 'dev-toolkit-84') -> str:
    """Generates a deterministic SHA-256 hash for crypto identifiers."""
    hasher = hashlib.sha256()
    hasher.update((data + salt).encode('utf-8'))
    return hasher.hexdigest()

def normalize_assets(assets: List[Union[str, Dict[str, Any]]]) -> List[str]:
    """Extracts canonical ticker symbols from mixed input formats."""
    normalized = []
    for asset in assets:
        if isinstance(asset, dict):
            normalized.append(str(asset.get('ticker', '')).upper())
        else:
            normalized.append(str(asset).upper())
    return [item for item in normalized if item]

def batch_process(items: List[Any], transform: Callable[[Any], Any]) -> List[Any]:
    """Applies transformation function to items with error suppression."""
    results = []
    for item in items:
        try:
            results.append(transform(item))
        except Exception:
            continue
    return results

class RateLimitGovernor:
    """Governor for enforcing request throughput limits."""
    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self.counter: int = 0

    def is_permitted(self) -> bool:
        """Checks if next request passes rate limit gate."""
        if self.counter < self.limit:
            self.counter += 1
            return True
        return False