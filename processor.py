import math
from typing import Annotated, Any, ByteString, Generator, List, TypeVar, Union

T = TypeVar("T")
ByteSequence = Union[bytes, bytearray]
EntropyScore = Annotated[float, "Shannon entropy value between 0.0 and 8.0"]

class DynamicBlockProcessor:
    """A dynamic stream processor designed for crypto block header analysis.

    Evaluates entropy vectors and nonce distributions across arbitrary
    cryptographic payloads using matrix-like generator transformations.
    """

    def __init__(self, window_size: int = 16) -> None:
        self.window_size: int = max(1, window_size)
        self._accumulator: List[bytes] = []

    def compute_entropy(self, payload: ByteSequence) -> EntropyScore:
        """Calculates normalized Shannon entropy for a given payload byte sequence.

        Args:
            payload: Raw byte payload from block headers or transactions.

        Returns:
            EntropyScore: Floating point scalar representing bits per byte.
        """
        if not payload:
            return 0.0

        length = len(payload)
        frequencies: dict[int, int] = {}
        for byte in payload:
            frequencies[byte] = frequencies.get(byte, 0) + 1

        entropy: float = 0.0
        for count in frequencies.values():
            p: float = count / length
            entropy -= p * math.log2(p)

        return round(entropy, 4)

    def process_stream(
        self, stream: Generator[ByteSequence, None, None]
    ) -> Generator[dict[str, Any], None, None]:
        """Consumes a stream of raw crypto chunks and yields analytical metrics.

        Args:
            stream: Generator yielding raw bytes or bytearrays.

        Yields:
            dict[str, Any]: Dictionary containing slice index, entropy, and anomaly flag.
        """
        for idx, chunk in enumerate(stream):
            self._accumulator.append(bytes(chunk))
            if len(self._accumulator) > self.window_size:
                self._accumulator.pop(0)

            composite: bytes = b"".join(self._accumulator)
            score: EntropyScore = self.compute_entropy(composite)

            yield {
                "sequence_id": idx,
                "window_bytes": len(composite),
                "entropy": score,
                "anomaly_flag": score < 3.5 or score > 7.95,
            }
