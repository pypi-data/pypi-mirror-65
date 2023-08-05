from __future__ import annotations
import materia

__all__ = ["MultiwfnInput"]


class MultiwfnInput:
    """
    Interface for inputting commands to Multiwfn.

    Attributes:
        commands (str): Iterable of commands which will be fed sequentially to Multiwfn.
    """

    def __init__(self, filepath: str, *commands: str) -> None:
        self.commands = tuple((materia.expand(filepath), *commands))

    def write(self, filepath: str) -> None:
        """
        Write Multiwfn input to a file.

        Args:
            filepath: Path to file to which the input will be written. Can be an absolute or a relative path.
        """
        with open(materia.expand(filepath), "w") as f:
            f.write(str(self))

    def __str__(self) -> str:
        return "\n".join(str(c) for c in self.commands) + "\n"
