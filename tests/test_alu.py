"""Verify operand order and data memory indirection."""

import unittest

from test_machine import execute_example


class ShiftTests(unittest.TestCase):
    """The count comes from memory; the value comes from the stack."""

    def test_shift(self):
        """Distinguish 5 << 2 from 2 << 5 and from 5 << address."""
        machine = execute_example("shift.json")
        self.assertEqual(machine.memory[30:32], [2, 20])
        self.assertEqual(machine.stack, [])
