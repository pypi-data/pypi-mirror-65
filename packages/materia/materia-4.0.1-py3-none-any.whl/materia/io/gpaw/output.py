from __future__ import annotations
import inspect
import materia
from typing import Any, Iterable, Union


class GPAWOutput:
    """
    Interface for outputs from tasks run with GPAW.

    Attributes:
        filepath (str): Absolute path to file from which output will be read.
    """

    def __init__(self, filepath: str) -> None:
        """
        Args:
            filepath: Path to file from which output will be read. Can be an absolute or a relative path.
        """
        raise NotImplementedError  # FIXME: implement
        self.filepath = materia.expand(filepath)

    def get(self, *quantity_names: str) -> Union[Any, Iterable[Any]]:
        """
        Get quantities from parsed GPAW output.

        Args:
            *args: Quantities to get from parsed output.
        """
        method_dict = dict(inspect.getmembers(self, predicate=inspect.isroutine))

        with open(self.filepath, "r") as f:
            lines = "".join(f.readlines())

        quantities = tuple(
            method_dict[name.lower()](lines=lines) for name in quantity_names
        )

        if len(quantities) == 1:
            return quantities[0]
        return quantities
