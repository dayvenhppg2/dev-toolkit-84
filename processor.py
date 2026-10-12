import hashlib
from typing import Dict, Any, List, Generator

class PipelineRegistry(type):
    """Metaclass maintaining ordered stage transformations."""
    stages: List[type] = []

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if name != "Stage":
            cls.stages.append(cls)

class Stage(metaclass=PipelineRegistry):
    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class SanitizerStage(Stage):
    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        addr = payload.get("address", "").strip().lower()
        payload["address"] = addr
        payload["is_valid"] = addr.startswith("0x") and len(addr) == 42
        return payload

class HashingStage(Stage):
    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raw = f"{payload.get('address')}:{payload.get('amount')}:{payload.get('nonce')}"
        payload["hash"] = "0x" + hashlib.sha256(raw.encode()).hexdigest()
        return payload

class GasCalculationStage(Stage):
    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload["gas_limit"] = 21000 if not payload.get("data") else 68000
        payload["max_priority_fee"] = 2.0 if payload.get("priority") else 1.0
        return payload

class TransactionProcessor:
    """Stream processor with implicit state cleanup via generator finalization."""
    def __init__(self, queue: List[Dict[str, Any]]):
        self._queue = queue

    def run(self) -> Generator[Dict[str, Any], None, None]:
        try:
            while self._queue:
                tx = self._queue.pop(0)
                for stage_cls in PipelineRegistry.stages:
                    tx = stage_cls().process(tx)
                yield tx
        finally:
            self._queue.clear()
