"""Check the specification and operand validation."""

from pathlib import Path
import unittest

from uvm.isa import parse, parse_row


EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


class ParserTests(unittest.TestCase):
    """Keep the published field examples independent of the encoder."""

    def test_fields(self):
        """Recover the exact fields in the four reference instructions."""
        program = parse((EXAMPLES / "spec.json").read_text())
        self.assertEqual([item.fields() for item in program], [
            "A=1, B=386", "A=0, B=526", "A=6, B=8", "A=4",
        ])

    def test_bad_operands(self):
        """Reject overflow, negative numbers, booleans and stray fields."""
        for row in [{"op": "read", "address": 1024},
                    {"op": "store", "offset": -1},
                    {"op": "const", "value": True},
                    {"op": "shl", "value": 1}]:
            with self.subTest(row=row), self.assertRaises(ValueError):
                parse_row(row)
