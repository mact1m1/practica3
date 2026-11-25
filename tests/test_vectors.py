"""End-to-end assembler and interpreter checks through the public CLI."""

from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]


class VectorTests(unittest.TestCase):
    """Use independent expected dumps and verify unchanged source cells."""

    def test_examples(self):
        """Assemble three programs and compare their actual CSV output."""
        sources = [[1, 2, 3, 4, 5, 6], [0, 1, 15, 16, 31, 32],
                   [7, 9, 11, 13, 15, 17]]
        with TemporaryDirectory() as temp:
            for number, values in enumerate(sources, 1):
                with self.subTest(example=number):
                    self.check_program(Path(temp), number, values)

    def check_program(self, directory, number, values):
        """Check that the second vector is replaced and the first survives."""
        name = f"vector{number}"
        binary, dump = directory / "vm.bin", directory / "memory.csv"
        source = ROOT / "examples" / f"{name}.json"
        expected = ROOT / "examples" / "expected" / f"{name}.csv"
        cli = ["sh", str(ROOT / "run.sh")]
        run([*cli, "asm", source, binary], check=True, capture_output=True)
        execute = [*cli, "run", binary, dump, "--range"]
        run([*execute, "20", "25"], check=True)
        self.assertEqual(dump.read_bytes(), expected.read_bytes())
        run([*execute, "10", "15"], check=True)
        rows = dump.read_text().splitlines()[1:]
        self.assertEqual(rows, [f"{10+i},{v}" for i, v in enumerate(values)])
