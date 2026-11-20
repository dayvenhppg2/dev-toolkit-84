from typing import Callable, Any, Dict, List
import hashlib
import time

class CryptoStreamPipeline:
    """Creative pipeline for transforming real-time crypto stream events."""
    def __init__(self, *steps: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self._steps = list(steps)

    def __rshift__(self, next_step: Callable[[Dict[str, Any]], Dict[str, Any]]) -> 'CryptoStreamPipeline':
        """Enable shift operator (>>) for pipeline composition."""
        return CryptoStreamPipeline(*self._steps, next_step)

    def __call__(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        result = payload.copy()
        for step in self._steps:
            result = step(result)
        return result

def sanitize_ticker(data: Dict[str, Any]) -> Dict[str, Any]:
    if 'symbol' in data:
        data['symbol'] = str(data['symbol']).upper().replace('-', '_')
    return data

def attach_entropy_hash(data: Dict[str, Any]) -> Dict[str, Any]:
    raw_payload = f"{data.get('symbol', '')}:{data.get('price', 0.0)}:{time.time_ns()}"
    data['entropy_sha256'] = hashlib.sha256(raw_payload.encode()).hexdigest()
    return data

def normalize_volume_precision(data: Dict[str, Any]) -> Dict[str, Any]:
    if 'volume' in data:
        data['volume'] = round(float(data['volume']), 8)
    return data

market_tick_processor = (
    CryptoStreamPipeline(sanitize_ticker)
    >> normalize_volume_precision
    >> attach_entropy_hash
)

def batch_process_ticks(ticks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [market_tick_processor(tick) for tick in ticks if isinstance(tick, dict)]
