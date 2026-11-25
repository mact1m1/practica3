"""Stack machine with independent instruction and zeroed data memory."""

import csv

from .codec import WORD_BYTES, decode
from .isa import ISA


CELL_COUNT = 1 << ISA["read"].width


def address(index):
    """Validate an effective data address before using it."""
    if not 0 <= index < CELL_COUNT:
        raise ValueError(f"data address out of range: {index}")
    return index


class Machine:
    """Keep the data stack and data memory separate from program bytes."""

    def __init__(self):
        """Initialize an empty stack and zero all addressable data."""
        self.stack = []
        self.memory = [0] * CELL_COUNT

    def pop(self):
        """Remove one operand or report a stack underflow."""
        if not self.stack:
            raise ValueError("stack underflow")
        return self.stack.pop()

    def step(self, instruction):
        """Execute one decoded instruction in specification pop order."""
        form, operand = instruction.form, instruction.operand
        if form == ISA["const"]:
            self.stack.append(operand)
        elif form == ISA["read"]:
            self.stack.append(self.memory[address(operand)])
        elif form == ISA["store"]:
            value = self.pop()
            self.memory[address(self.pop() + operand)] = value
        else:
            raise ValueError("unsupported operation")

    def run(self, code):
        """Fetch one word at a time, decode, execute and advance the PC."""
        for pc in range(0, len(code), WORD_BYTES):
            try:
                self.step(decode(code[pc:pc + WORD_BYTES]))
            except ValueError as error:
                raise ValueError(f"byte {pc}: {error}") from error

    def dump(self, path, start, end):
        """Write both endpoints of a validated memory interval as CSV."""
        address(start)
        address(end)
        if start > end:
            raise ValueError("start must not exceed end")
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(("address", "value"))
            for index in range(start, end + 1):
                writer.writerow((index, self.memory[index]))
