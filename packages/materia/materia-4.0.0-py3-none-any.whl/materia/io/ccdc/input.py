from __future__ import annotations
import materia

__all__ = ["CCDCInput"]


class CCDCInput:
    """
    Interface to write inputs which can be run with CCDC.

    Attributes:
        ccdc_script (str): String representation of CCDC input.
    """

    def __init__(self, ccdc_script: str) -> None:
        self.ccdc_script = ccdc_script

    def __str__(self) -> str:
        """
        Get string representation of CCDC input.
        """
        return self.ccdc_script

    def write(self, filepath: str) -> None:
        """
        Write CCDC input to a file.

        Args:
            filepath: Path to file to which the input will be written. Can be an absolute or a relative path.
        """
        with open(materia.expand(filepath), "w") as f:
            f.write(str(self))
