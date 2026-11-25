"""Command-line entry point for the UVM tools."""

import argparse
from pathlib import Path
import sys

from .isa import parse


def assemble(args):
    """Translate the JSON program into instruction fields."""
    program = parse(args.source.read_text(encoding="utf-8"))
    if args.test:
        for instruction in program:
            print(instruction.fields())


def parser():
    """Build subcommands and their required positional paths."""
    result = argparse.ArgumentParser(prog="uvm")
    commands = result.add_subparsers(dest="command", required=True)
    asm = commands.add_parser("asm", help="assemble a JSON program")
    asm.add_argument("source", type=Path)
    asm.add_argument("binary", type=Path)
    asm.add_argument("--test", action="store_true")
    asm.set_defaults(action=assemble)
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
