"""Command-line entry point for the UVM tools."""

import argparse
from pathlib import Path
import sys

from .codec import byte_listing, encode
from .isa import parse
from .machine import Machine


def assemble(args):
    """Translate the JSON program into instruction fields."""
    program = parse(args.source.read_text(encoding="utf-8"))
    words = [encode(instruction) for instruction in program]
    data = b"".join(words)
    args.binary.write_bytes(data)
    print(f"Bytes: {len(data)}")
    if args.test:
        for instruction, word in zip(program, words):
            print(f"{instruction.fields()}: {byte_listing(word)}")


def interpret(args):
    """Execute a binary and save the requested inclusive range."""
    machine = Machine()
    machine.run(args.binary.read_bytes())
    machine.dump(args.dump, *args.span)


def parser():
    """Build subcommands and their required positional paths."""
    result = argparse.ArgumentParser(prog="uvm")
    commands = result.add_subparsers(dest="command", required=True)
    asm = commands.add_parser("asm", help="assemble a JSON program")
    asm.add_argument("source", type=Path)
    asm.add_argument("binary", type=Path)
    asm.add_argument("--test", action="store_true")
    asm.set_defaults(action=assemble)
    run = commands.add_parser("run", help="execute a binary and dump CSV")
    run.add_argument("binary", type=Path)
    run.add_argument("dump", type=Path)
    run.add_argument("--range", dest="span", nargs=2, type=int,
                     metavar=("FIRST", "LAST"), required=True)
    run.set_defaults(action=interpret)
    return result


def main():
    """Report file and program errors without a Python traceback."""
    args = parser().parse_args()
    try:
        args.action(args)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
