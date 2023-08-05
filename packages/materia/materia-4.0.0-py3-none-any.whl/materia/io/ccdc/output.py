from __future__ import annotations
import inspect
import materia
from typing import Any, Iterable, Union

__all__ = ["CCDCOutput"]


class CCDCOutput:
    """
    Interface for outputs from tasks run with CCDC.

    Attributes:
        filepath (str): Absolute path to file from which output will be read.
    """

    def __init__(self, filepath: str) -> None:
        """
        Args:
            filepath: Path to file from which output will be read. Can be an absolute or a relative path.
        """
        self.filepath = materia.expand(filepath)

        raise NotImplementedError

    def get(self, *args: str) -> Union[Any, Iterable[Any]]:
        """
        Get quantities from parsed CCDC output.

        Args:
            *args: Quantities to get from parsed output.
        """
        method_dict = dict(inspect.getmembers(self, predicate=inspect.isroutine))

        with open(self.filepath, "r") as f:
            lines = "".join(f.readlines())

        quantities = tuple(method_dict[name.lower()](lines=lines) for name in args)

        if len(quantities) == 1:
            return quantities[0]
        return quantities
