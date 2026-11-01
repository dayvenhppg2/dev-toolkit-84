"""Crypto state accumulator and payload obfuscator module."""

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Generator, List, Optional, Tuple, TypeVar

T = TypeVar("T", bound=bytes)


@dataclass
class CryptoStateEngine:
    """A deterministic byte-scrambling and state-accumulation pipeline.

    Utilizes sliding XOR windows combined with cascading SHA-256 state updates
    to generate pseudo-entropy streams for payload signatures.
    """

    seed: bytes
    rounds: int = 16
    _history: List[bytes] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if not self.seed:
            raise ValueError("Seed buffer cannot be empty.")
        self._history.append(sha256(self.seed).digest())

    def _cascade_hash(self, current: bytes, modifier: int) -> bytes:
        """Derive next state block using XOR shifts and SHA-256.

        :param current: Input bytes block to transform.
        :param modifier: Round index modifier for dynamic salt.
        :return: 32-byte hash digest representing state transition.
        """
        salt = modifier.to_bytes(4, byteorder="big")
        xor_block = bytes(b ^ salt[i % len(salt)] for i, b in enumerate(current))
        return sha256(xor_block + current).digest()

    def generate_entropy_stream(
        self, payload: bytes, count: int = 4
    ) -> Generator[Tuple[int, bytes], None, None]:
        """Yield a sequence of state-bound derived cryptographic blocks.

        :param payload: Data payload used to perturb entropy pool.
        :param count: Total number of iterations to yield.
        :return: Generator yielding tuple of (step_index, block_hash).
        """
        state = sha256(self.seed + payload).digest()
        for idx in range(count):
            for r in range(self.rounds):
                state = self._cascade_hash(state, r + idx)
            self._history.append(state)
            yield (idx, state)

    def extract_proof(self) -> Optional[bytes]:
        """Aggregate current history stack into a singular verification tag.

        :return: Final combined digest bytes or None if history is uninitialized.
        """
        if not self._history:
            return None
        acc = self._history[0]
        for item in self._history[1:]:
            acc = bytes(a ^ b for a, b in zip(acc, item))
        return sha256(acc).digest()
