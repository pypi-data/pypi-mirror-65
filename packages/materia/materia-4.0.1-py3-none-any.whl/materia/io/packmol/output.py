from __future__ import annotations
import inspect
import materia
from typing import Tuple, TypeVar, Union

__all__ = ["PackmolOutput"]

T = TypeVar("T")


class PackmolOutput:
    def __init__(self, filepath: str) -> None:
        # raise NotImplementedError
        self.filepath = materia.expand(filepath)

    def get(self, *quantity_names: str) -> Union[T, Tuple[T]]:
        method_dict = dict(inspect.getmembers(self, predicate=inspect.isroutine))

        with open(self.filepath, "r") as f:
            lines = "".join(f.readlines())

        quantities = tuple(
            method_dict[name.lower()](lines=lines) for name in quantity_names
        )

        if len(quantities) == 1:
            return quantities[0]
        return quantities
