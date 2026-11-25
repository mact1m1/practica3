"""Exercise execution independently of CLI formatting."""

from pathlib import Path
import unittest

from uvm.codec import encode
from uvm.isa import parse
from uvm.machine import Machine


def execute_example(name):
    """Assemble and execute a checked-in JSON example in a fresh VM."""
    root = Path(__file__).resolve().parents[1]
    program = parse((root / "examples" / name).read_text())
    machine = Machine()
    machine.run(b"".join(map(encode, program)))
    return machine


class MemoryTests(unittest.TestCase):
    """Check memory operations and malformed machine code."""

    def test_copy(self):
        """Copy distinct cells without changing the source or neighbors."""
        machine = execute_example("copy.json")
        self.assertEqual(machine.memory[10:13], [3, 7, 11])
        self.assertEqual(machine.memory[19:24], [0, 3, 7, 11, 0])
        self.assertEqual(machine.stack, [])

    def test_bad_words(self):
        """Reject incomplete instructions, unused bits and bad opcodes."""
        for data in [b"\x01", bytes.fromhex("01 00 80"), b"\x07\0\0"]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                Machine().run(data)

    def test_stack_underflow(self):
        """Report the failing instruction address on an empty stack."""
        with self.assertRaisesRegex(ValueError, "byte 0: stack underflow"):
            Machine().run(bytes.fromhex("06 00 00"))
