"""Fixed-length little-endian variant 19 instruction encoding."""

from .isa import ISA, Instruction


WORD_BYTES = 3
OP_BITS = 3
OP_MASK = (1 << OP_BITS) - 1
BY_OPCODE = {form.opcode: form for form in ISA.values()}


def encode(instruction):
    """Pack opcode into bits 0..2 and operand starting at bit 3."""
    word = instruction.form.opcode | instruction.operand << OP_BITS
    return word.to_bytes(WORD_BYTES, "little")


def byte_listing(data):
    """Format one instruction exactly as in the byte examples."""
    return ", ".join(f"0x{byte:02X}" for byte in data)


def decode(data):
    """Validate size, opcode and unused bits before unpacking a word."""
    if len(data) != WORD_BYTES:
        raise ValueError("incomplete instruction")
    word = int.from_bytes(data, "little")
    form = BY_OPCODE.get(word & OP_MASK)
    if form is None:
        raise ValueError("unknown opcode")
    operand = word >> OP_BITS
    if operand >= (1 << form.width):
        raise ValueError("nonzero reserved bits")
    return Instruction(form, operand)
