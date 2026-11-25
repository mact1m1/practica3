"""Instruction set and human-readable JSON format."""

from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Format:
    """Describe the opcode and its one optional unsigned argument."""

    opcode: int
    field: str = ""
    width: int = 0


ISA = {
    "const": Format(1, "value", 20),
    "read": Format(0, "address", 10),
    "store": Format(6, "offset", 6),
    "shl": Format(4),
}


@dataclass(frozen=True)
class Instruction:
    """Validated intermediate representation of fields A and B."""

    form: Format
    operand: int = 0

    def fields(self):
        """Display the fields in specification order."""
        first = f"A={self.form.opcode}"
        return f"{first}, B={self.operand}" if self.form.field else first


def parse_row(row):
    """Validate the mnemonic, exact field set and unsigned operand."""
    if not isinstance(row, dict) or not isinstance(row.get("op"), str):
        raise ValueError("expected an object with a string op")
    form = ISA.get(row["op"])
    if form is None:
        raise ValueError(f"unknown operation: {row['op']}")
    keys = {"op", form.field} if form.field else {"op"}
    if set(row) != keys:
        raise ValueError(f"expected fields: {sorted(keys)}")
    operand = row.get(form.field, 0)
    if type(operand) is not int or not 0 <= operand < (1 << form.width):
        raise ValueError(f"invalid unsigned {form.width}-bit operand")
    return Instruction(form, operand)


def parse(source):
    """Read a JSON array and report instruction numbers starting at one."""
    rows = json.loads(source)
    if not isinstance(rows, list):
        raise ValueError("program must be a JSON array")
    result = []
    for number, row in enumerate(rows, 1):
        try:
            result.append(parse_row(row))
        except ValueError as error:
            raise ValueError(f"instruction {number}: {error}") from error
    return result
