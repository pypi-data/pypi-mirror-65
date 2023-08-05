from __future__ import annotations
import materia
from typing import Dict, Iterable, Optional, Tuple, Union

__all__ = ["QChemFragments", "QChemInput", "QChemStructure"]


class QChemStructure:
    def __init__(
        self,
        structure: materia.Structure,
        charge: Optional[int] = 0,
        multiplicity: Optional[int] = 1,
        mm_parameters: Optional[Dict[materia.Atom, str]] = None,
        bonds: Optional[Dict[int, int]] = None,
    ) -> None:
        self.structure = structure
        self.charge = charge
        self.multiplicity = multiplicity
        self.mm_parameters = mm_parameters or {}
        self.bonds = bonds or {}

    def __str__(self) -> str:
        return f"  {self.charge} {self.multiplicity}\n" + "\n".join(
            (
                f"  {a.atomic_symbol}  "
                + "  ".join(str(p) for p in a.position.reshape(3,))
                + (f" {self.mm_parameters[a]}" if a in self.mm_parameters else "")
                + (
                    " "
                    + "  ".join(
                        str(j + 1)
                        for j in self.bonds[i] + (-1,) * (4 - len(self.bonds[i]))
                    )
                    if i in self.bonds
                    else ""
                )
                for i, a in enumerate(self.structure.atoms)
            )
        )


class QChemFragments:
    def __init__(
        self,
        structures: Iterable[materia.Structure],
        charges: Optional[Iterable[int]] = None,
        multiplicities: Optional[Iterable[int]] = None,
        total_charge: Optional[int] = 0,
        total_multiplicity: Optional[int] = 1,
    ) -> None:
        self.structures = structures
        self.charges = charges or (0,) * len(self.structures)
        self.multiplicities = multiplicities or (1,) * len(self.structures)
        self.total_charge = total_charge
        self.total_multiplicity = total_multiplicity

    def __str__(self) -> str:
        return f"  {self.total_charge} {self.total_multiplicity}\n--\n" + "\n--\n".join(
            str(QChemStructure(structure=s, charge=c, multiplicity=m))
            for c, m, s in zip(self.charges, self.multiplicities, self.structures)
        )
        # return (
        #     f"  {self.total_charge} {self.total_multiplicity}\n--\n"
        #     + "--\n".join(
        #         f"  {c} {m}\n"
        #         + "\n".join(
        #             f"  {a.atomic_symbol}  "
        #             + " ".join(str(p) for p in a.position.reshape(3,))
        #             for a in structure.atoms
        #         )
        #         + "\n"
        #         for c, m, structure in zip(
        #             self.charges, self.multiplicities, self.structures
        #         )
        #     )
        # )


class QChemInput:
    def __init__(
        self,
        molecule: Union[
            materia.QChemStructure, materia.QChemFragments, materia.Structure
        ],
        settings: materia.Settings,
    ) -> None:
        self.molecule = molecule
        self.settings = settings

    def write(self, filepath: str) -> None:
        with open(materia.expand(filepath), "w") as f:
            f.write(str(self))

    def __str__(self) -> str:
        molecule_block = (
            str(QChemStructure(self.molecule))
            if isinstance(self.molecule, materia.Structure)
            else str(self.molecule)
        )
        return f"$molecule\n{molecule_block}\n$end\n" + "\n".join(
            _block_to_str(block_name=block_name, block_params=block_params)
            for block_name, block_params in self.settings.d.items()
        )


def _block_to_str(block_name: str, block_params) -> str:
    if block_name == "xc_functional":
        return _xc_functional_str(*block_params)
    else:
        return _block_str(block_name=block_name, **block_params)


def _block_str(
    block_name, **block_params
) -> str:  # FIXME: not sure exactly how to annotate type hint for **block_params
    longest_key_length = max(len(k) for k in block_params)
    return (
        f"${block_name}\n"
        + "".join(
            f"  {k}" + " " * (longest_key_length - len(k) + 1) + f"{v}\n"
            for k, v in block_params.items()
        )
        + "$end\n"
    )


def _xc_functional_str(*functional_tuples: Tuple[str, str, str]) -> str:
    component_types, component_names, component_coefficients = zip(*functional_tuples)
    longest_component_name = max(len(cn) for cn in component_names)

    s = f"$xc_functional\n"
    for ct, cn, cc in zip(component_types, component_names, component_coefficients):
        if ct == "K":
            s += "  K " + " " * (longest_component_name + 1) + f" {cc}\n"
        else:
            s += (
                f"  {ct} {cn}"
                + " " * (longest_component_name - len(cn) + 1)
                + f" {cc}\n"
            )
    s += "$end\n"

    return s
