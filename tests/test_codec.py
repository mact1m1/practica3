"""Independent reference bytes for the four instructions."""

from pathlib import Path
import unittest

from uvm.codec import encode
from uvm.isa import parse


class EncodingTests(unittest.TestCase):
    """Compare complete binary output with the reference program."""

    def test_reference_bytes(self):
        """Match all twelve reference bytes including padding."""
        root = Path(__file__).resolve().parents[1]
        program = parse((root / "examples/spec.json").read_text())
        self.assertEqual(b"".join(map(encode, program)), bytes.fromhex(
            "11 0C 00 70 10 00 46 00 00 04 00 00"
        ))
