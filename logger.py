import hashlib
import time
from collections import deque
from typing import Any, Dict, List, Optional

class CryptoTraceLogger:
    """Self-compacting trace logger for crypto operations."""

    COLORS = {
        "DEBUG": "\u001b[36m",
        "INFO": "\u001b[32m",
        "WARN": "\u001b[33m",
        "CRITICAL": "\u001b[35m",
        "RESET": "\u001b[0m",
    }

    def __init__(self, max_depth: int = 100) -> None:
        self._trace_ring: deque = deque(maxlen=max_depth)
        self._session_salt: bytes = hashlib.sha256(
            str(time.time_ns()).encode()
        ).digest()[:8]

    def _tag(self, level: str, topic: str) -> str:
        digest = hashlib.blake2b(
            f"{topic}:{level}".encode(), key=self._session_salt, digest_size=3
        ).hexdigest()
        color = self.COLORS.get(level, self.COLORS["RESET"])
        return f"{color}[{level}][#{digest}]{self.COLORS['RESET']}"

    def emit(self, level: str, topic: str, payload: Dict[str, Any]) -> str:
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        tag = self._tag(level.upper(), topic.lower())
        sanitized = {
            k: (v if "key" not in k.lower() and "secret" not in k.lower() else "<REDACTED>")
            for k, v in payload.items()
        }
        entry = f"{timestamp} {tag} ({topic}): {sanitized}"
        self._trace_ring.append((timestamp, level, topic, sanitized))
        return entry

    def flush_trace(self, topic_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        extracted = [
            {"time": ts, "level": lvl, "topic": top, "data": data}
            for ts, lvl, top, data in list(self._trace_ring)
            if topic_filter is None or top == topic_filter
        ]
        if topic_filter is None:
            self._trace_ring.clear()
        return extracted

default_logger = CryptoTraceLogger()
