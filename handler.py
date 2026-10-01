import functools
import random
import time
from typing import Any, Callable, List

class NodeNetworkError(IOError):
    """Indicates an unstable connection to a blockchain gateway."""
    pass

class NodeGatewayHandler:
    """Manages RPC query dispatch with decentralized path rotation and golden-ratio backoff."""

    def __init__(self, rpc_nodes: List[str], retry_limit: int = 4):
        self.nodes = rpc_nodes
        self.retry_limit = retry_limit
        self._current_index = 0

    def _switch_endpoint(self) -> str:
        self._current_index = (self._current_index + 1) % len(self.nodes)
        return self.nodes[self._current_index]

    def execute_with_failover(self, task: Callable[..., Any], *args, **kwargs) -> Any:
        phi = 1.61803398875  # Golden ratio to avoid synchronized stampedes
        last_exception = None

        for attempt in range(1, self.retry_limit + 1):
            current_rpc = self.nodes[self._current_index]
            try:
                return task(current_rpc, *args, **kwargs)
            except NodeNetworkError as error:
                last_exception = error
                delay = (phi ** attempt) + random.uniform(0.1, 0.9)
                time.sleep(delay)
                self._switch_endpoint()

        raise ConnectionError(
            f"Execution exhausted all {self.retry_limit} retries. Final error: {last_exception}"
        )