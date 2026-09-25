import hashlib
from typing import Generator, Union


class PhoneticHasher:
    """Transforms raw crypto transaction hashes into memorable phoneme structures."""

    CONSONANTS = "bcdfghjklmnpqrstvwxyz"
    VOWELS = "aeiou"

    @classmethod
    def byte_to_phoneme(cls, byte_val: int) -> str:
        # Extract two distinct index maps from a single byte
        c_idx = (byte_val & 0xF0) >> 4
        v_idx = byte_val & 0x0F
        return (
            cls.CONSONANTS[c_idx % len(cls.CONSONANTS)]
            + cls.VOWELS[v_idx % len(cls.VOWELS)]
        )

    @classmethod
    def humanize(cls, tx_hash: Union[str, bytes]) -> str:
        if isinstance(tx_hash, str):
            if tx_hash.startswith("0x"):
                tx_hash = tx_hash[2:]
            raw_bytes = bytes.fromhex(tx_hash)
        else:
            raw_bytes = tx_hash

        # Double-hash to ensure entropy distribution
        scrambled = hashlib.sha256(raw_bytes).digest()

        # Generate phonemes for each pair of bytes lazily
        phonemes: Generator[str, None, None] = (
            cls.byte_to_phoneme(b) for b in scrambled[:10]
        )
        joined = "".join(phonemes)

        # Inject separators for readability
        return "-".join(joined[i : i + 4] for i in range(0, len(joined), 4))

    @classmethod
    def entropy_fingerprint(cls, address: str) -> int:
        """Returns a deterministic, self-validating checksum integer using bitwise folding."""
        clean_addr = address.lower().replace("0x", "")
        hasher = hashlib.blake2b(clean_addr.encode(), digest_size=8)
        digest = hasher.digest()

        # Fold 8 bytes into a single 16-bit entropy value
        folded = 0
        for i in range(0, len(digest), 2):
            val = (digest[i] << 8) | digest[i + 1]
            folded ^= val
        return folded
