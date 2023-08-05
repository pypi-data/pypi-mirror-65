from __future__ import annotations
from typing import Any, Callable, Iterable, Optional, Tuple, Union

import cclib
import contextlib
import copy
import dlib
import functools
import materia as mtr
from materia.utils import memoize
from materia.workflow import Workflow
import numpy as np

# FIXME: replace os with pathlib where possible
import os
import re

# import scipy.optimize
import subprocess
import tempfile
import uuid

__all__ = [
    "ExternalTask",
    "FunctionTask",
    "InputTask",
    "MaxLIPOTR",
    "ShellCommand",
    "Task",
    "FragItFragmentStructure",
    "MultiwfnVolume",
    "PackmolSolvate",
    #    "ExecuteQChem",
    "QChemAIMD",
    "QChemKoopmanError",
    "QChemLRTDDFT",
    "QChemMinimizeKoopmanError",
    "QChemOptimize",
    "QChemPolarizability",
    #    "QChemRTTDDFT",
    "QChemSinglePoint",
    "QChemSinglePointFrontier",
    "WriteQChemInput",
    "WriteQChemInputGeometryRelaxation",
    "WriteQChemInputLRTDDFT",
    "WriteQChemInputPolarizability",
    "WriteQChemInputSinglePoint",
    #    "WriteQChemTDSCF",
]


class Task:
    def __init__(
        self,
        num_cores: Optional[int] = 1,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.num_cores = num_cores
        self.handlers = handlers or []
        self.name = (
            name
            or re.match("<class '(?P<cls>.*)'>", str(self.__class__))
            .group("cls")
            .rsplit(".")[-1]
        )

        self.requirements = []
        self.named_requirements = {}

    def requires(self, *args: Task, **kwargs: Task) -> None:
        self.requirements += [a if isinstance(a, Task) else InputTask(a) for a in args]
        self.named_requirements = dict(
            **self.named_requirements,
            **{
                k: v if isinstance(v, Task) else InputTask(v) for k, v in kwargs.items()
            },
        )

    def run(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.name


class ExternalTask(Task):
    def __init__(
        self,
        engine: mtr.Engine,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.engine = engine
        self.io = io
        super().__init__(self.engine.num_processors or 1, handlers=handlers, name=name)


class FunctionTask(Task):
    def __init__(
        self,
        f: Callable,
        handlers: Optional[Iterable[Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.f = f

    def run(self, **kwargs) -> None:
        return self.f(**kwargs)


class InputTask(Task):
    def __init__(
        self,
        value: Any,
        handlers: Optional[Iterable[Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(1, handlers=handlers, name=name)
        self.value = value

    def run(self) -> Any:
        return self.value


class ShellCommand(Task):
    def __init__(
        self,
        command: str,
        handlers: Optional[Iterable[Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.command = command

    def run(self) -> None:
        subprocess.call(self.command.split())


def task(
    f: Callable = None,
    handlers: Optional[Iterable[Handler]] = None,
    name: Optional[str] = None,
) -> FunctionTask:
    # FIXME: this is incomptabile with mtr.Workflow.run(thread=False) (i.e. with multiprocessing) because FunctionTask cannot be serialized!
    if f is None:
        return functools.partial(task, handlers=handlers, name=name)

    return FunctionTask(f=f, handlers=handlers, name=name)


# class GoldenSectionSearch:
#     def __init__(self, objective_function):
#         self.objective_function = objective_function

#     @memoize
#     def evaluate_objective(self, x):
#         return self.objective_function(x)

#     def optimize(self, delta, tolerance):
#         bracket = self._find_gss_bracket(delta=delta)

#         return scipy.optimize.minimize_scalar(
#             fun=self.evaluate_objective, bracket=bracket, method="Golden", tol=tolerance
#         )

#     def _find_gss_bracket(self, delta):
#         # FIXME: ugly but it works...
#         phi = (1 + math.sqrt(5)) / 2

#         self.evaluate_objective(x=1e-3)
#         self.evaluate_objective(x=delta)

#         while self.evaluate_objective.cache.last_result(
#             n=1
#         ) <= self.evaluate_objective.cache.last_result(n=2):
#             _, last1 = self.evaluate_objective.cache.last_args(n=1)
#             _, last2 = self.evaluate_objective.cache.last_args(n=2)

#             self.evaluate_objective(x=last1["x"] + phi * (last1["x"] - last2["x"]))

#         if len(self.evaluate_objective.cache) > 2:
#             _, last3 = self.evaluate_objective.cache.last_args(n=3)
#             _, last1 = self.evaluate_objective.cache.last_args(n=1)
#             return (last3["x"], last1["x"])
#         else:
#             _, last2 = self.evaluate_objective.cache.last_args(n=2)
#             _, last1 = self.evaluate_objective.cache.last_args(n=1)
#             return (last2["x"], last1["x"])

#         return bracket

#     # def plot_results(self):
#     #     x, y = zip(*sorted(self.evaluate_objective.cache.items()))
#     #     plt.plot(x, y)
#     #     plt.show()


T = Union[int, float]


class MaxLIPOTR(Task):
    def __init__(
        self,
        objective_function: Callable[T, T],
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(1, handlers, name)
        self.objective_function = objective_function

    @memoize
    def _evaluate_objective(self, *args: T) -> T:
        return self.objective_function(*args)

    def run(
        self,
        x_min: Union[T, Iterable[T]],
        x_max: Union[T, Iterable[T]],
        num_evals: int,
        epsilon: Optional[float] = 0,
    ) -> Tuple[T, Union[int, float]]:

        return dlib.find_min_global(
            self._evaluate_objective,
            x_min if isinstance(x_min, list) else [x_min],
            x_max if isinstance(x_max, list) else [x_max],
            num_evals,
            solver_epsilon=epsilon,
        )

    # def plot_results(self):
    #     x, y = zip(*sorted(self.evaluate_objective.cache.items()))
    #     plt.plot(x, y)
    #     plt.show()


# -------------------------- CCDC -------------------------- #

# from __future__ import annotations
# import os
# import mtr
# import textwrap
# from typing import Iterable, Optional

# from ...workflow.tasks.task import Task

# __all__ = ["CCDCUnitCellStructure"]


# class CCDCUnitCellStructure(Task):
#     def __init__(
#         self,
#         input_name: str,
#         molecule_name: str,
#         engine: mtr.CCDCEngine,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         self.input_name = input_name
#         self.engine = engine
#         name = "'" + molecule_name + "'"
#         self.input_string = textwrap.dedent(
#             f"""\
#                     import numpy as np
#                     import ccdc.search
#                     tns = ccdc.search.TextNumericSearch()
#                     tns.add_compound_name({name})
#                     try:
#                         hit = next(hit for hit in tns.search() if hit.entry.chemical_name == {name})
#                         print('atomic_symbols: {{0}}\\n'.format(tuple(a.atomic_symbol for a in hit.molecule.atoms)))
#                         print('coordinates: {{0}}\\n'.format(np.vstack([a.coordinates for a in hit.molecule.atoms])))
#                         print('spacegroup_number_and_setting: {{0}}\\n'.format(hit.crystal.spacegroup_number_and_setting))
#                         print('cell_lengths: {{0}}\\n'.format(np.array(hit.crystal.cell_lengths)))
#                         print('cell_angles: {{0}}\\n'.format(np.array(hit.crystal.cell_angles)))
#                     except StopIteration:
#                         pass
#                     """
#         )

#     def run(self):
#         # FIXME: catch StopIteration in CCDC code
#         # FIXME: generalize past 2019 version of CCDC code
#         # FIXME: add more rigorous/better checking for CCDC crystal matches

#         # FIXME: where does input_path come from? must include self.input_name but also must include engine.work_dir...
#         mtr.CCDCInput(ccdc_script=self.input_string).write(self.input_path)

#         self.engine.execute(input_path=self.input_path)

# -------------------------- FRAGIT -------------------------- #


class FragItFragmentStructure(ExternalTask):
    """
    Task to fragment a structure using FragIt.

    Attributes:
        engine (mtr.FragItEngine): Engine which will be used to fragment structure.
    """

    def run(
        self, structure: Union[str, mtr.Structure]
    ) -> Tuple[str, Iterable[mtr.Structure]]:
        with self.io() as io:
            if isinstance(structure, str):
                filepath = mtr.expand(structure)
            else:
                while isinstance(structure, mtr.Structure):
                    filepath = mtr.expand(
                        os.path.join(io.work_dir, f"{uuid.uuid4().hex}.xyz")
                    )
                    try:
                        structure.write(filepath)
                        break
                    except FileExistsError:
                        continue

            self.engine.execute(
                structure_filepath=filepath, log_filepath=io.out, work_dir=io.work_dir,
            )

            name, _ = os.path.splitext(os.path.basename(filepath))
            pat = re.compile(rf"(?P<file_name>{name}_fragment_\d*\.xyz)")
            matches = (pat.match(s) for s in os.listdir(io.work_dir))

            return tuple(
                mtr.Structure.read(os.path.join(io.work_dir, m.group("file_name")))
                for m in matches
                if m is not None
            )


# -------------------------- MULTIWFN -------------------------- #


class MultiwfnBaseTask(ExternalTask):
    def commands(self) -> Iterable[Union[str, int, float]]:
        raise NotImplementedError

    def parse(self, output: str) -> Any:
        raise NotImplementedError

    def run(self, filepath: str) -> Any:
        inp = mtr.MultiwfnInput(mtr.expand(filepath), *self.commands(), -10,)

        with self.io() as io:
            inp.write(io.inp)

            self.engine.execute(self.io)

            return self.parse(io.out)


# class ExecuteMultiwfn(Task):
#     def __init__(
#         self,
#         input_path: str,
#         engine: mtr.MultiwfnEngine,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(handlers=handlers, name=name)
#         self.input_path = input_path
#         self.engine = engine

#     def run(self) -> None:
#         self.engine.execute(input_path=self.input_path)


class MultiwfnVolume(MultiwfnBaseTask):
    def commands(self):
        integration_mesh_exp = 9  #: int = 9,
        density_isosurface = 1e-3  #: float = 0.001,
        box_size_factor = 1.7  #: float = 1.7
        return (
            100,
            3,
            f"{integration_mesh_exp},{density_isosurface},{box_size_factor}",
            "0,0,0",
            0,
        )

    def parse(self, output: str) -> mtr.Qty:
        return mtr.MultiwfnOutput(output).get("volume")


# class WriteMultiwfnInput(Task):
#     def __init__(
#         self,
#         input_name: str,
#         in_filepath: str,  # FIXME: awful name for this variable, fix here and analogous issues throughout this file
#         commands: Iterable[str],
#         work_directory: str = ".",
#         handlers: Iterable[Handler] = None,
#         name: str = None,
#     ):
#         super().__init__(handlers=handlers, name=name)
#         self.input_path = mtr.expand(os.path.join(work_directory, input_name))
#         self.in_filepath = mtr.expand(in_filepath)
#         self.commands = commands

#         try:
#             os.makedirs(mtr.expand(work_directory))
#         except FileExistsError:
#             pass

#     def run(self):
#         mtr.MultiwfnInput(self.in_filepath, *self.commands).write(self.input_path)


# -------------------------- OPENBABEL -------------------------- #

# from __future__ import annotations
# import contextlib
# import os
# import mtr
# import re
# import tempfile
# from typing import Iterable, Optional, Union

# from ...workflow.tasks.task import Task

# __all__ = [
#     "OpenbabelConvertToFile",
#     "OpenbabelConvertToMol",
#     "OpenbabelConvertToPDB",
#     "OpenbabelConvertToSMILES",
#     "OpenbabelConvertToSDF",
# ]


# class OpenbabelConvertToFile(Task):
#     def __init__(
#         self,
#         engine: mtr.OpenbabelEngine,
#         filetype: str,
#         output_name: Optional[str] = None,
#         log_name: Optional[str] = "obabel.log",
#         work_dir: Optional[str] = ".",
#         keep_logs: bool = True,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(handlers=handlers, name=name)
#         self.engine = engine
#         self.filetype = filetype
#         self.output_name = output_name
#         self.log_name = log_name
#         self.work_dir = work_dir
#         self.keep_logs = keep_logs

#     def run(self, structure: Union[str, mtr.Structure]) -> str:
#         with mtr.work_dir(self.work_dir) as wd:
#             arguments = [f"-o{self.filetype}"]

#             if self.output_name is not None:
#                 output_path = (
#                     f"{mtr.expand(self.output_name,dir=wd)}.{self.filetype}"
#                 )
#                 arguments.append(f"-O{output_path}")

#             with contextlib.nullcontext(structure) if isinstance(
#                 structure, str
#             ) else structure.tempfile(suffix=".xyz") as fp:
#                 input_filepath = mtr.expand(
#                     path=fp.name if hasattr(fp, "name") else fp, dir=wd
#                 )
#                 self.engine.execute(
#                     input_filepath=input_filepath,
#                     log_filepath=mtr.expand(path=self.log_name, dir=wd),
#                     arguments=arguments,
#                 )

#             if self.output_name is not None:
#                 with open(output_path, "r") as f:
#                     return "".join(f.readlines())


# class OpenbabelConvertToMol(OpenbabelConvertToFile):
#     def __init__(
#         self,
#         engine: mtr.OpenbabelEngine,
#         output_name: str,
#         log_name: Optional[str] = "obabel.log",
#         work_dir: Optional[str] = ".",
#         keep_logs: bool = True,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(
#             engine=engine,
#             filetype="mol",
#             output_name=output_name,
#             log_name=log_name,
#             work_dir=work_dir,
#             keep_logs=keep_logs,
#             handlers=handlers,
#             name=name,
#         )


# class OpenbabelConvertToPDB(OpenbabelConvertToFile):
#     def __init__(
#         self,
#         engine: mtr.OpenbabelEngine,
#         output_name: str,
#         log_name: Optional[str] = "obabel.log",
#         work_dir: Optional[str] = ".",
#         keep_logs: bool = True,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(
#             engine=engine,
#             filetype="pdb",
#             output_name=output_name,
#             log_name=log_name,
#             work_dir=work_dir,
#             keep_logs=keep_logs,
#             handlers=handlers,
#             name=name,
#         )


# class OpenbabelConvertToSDF(OpenbabelConvertToFile):
#     def __init__(
#         self,
#         engine: mtr.OpenbabelEngine,
#         output_name: str,
#         log_name: Optional[str] = "obabel.log",
#         work_dir: Optional[str] = ".",
#         keep_logs: bool = True,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(
#             engine=engine,
#             filetype="sdf",
#             output_name=output_name,
#             log_name=log_name,
#             work_dir=work_dir,
#             keep_logs=keep_logs,
#             handlers=handlers,
#             name=name,
#         )


# class OpenbabelConvertToSMILES(OpenbabelConvertToFile):
#     def __init__(
#         self,
#         engine: mtr.OpenbabelEngine,
#         output_name: str,
#         log_name: Optional[str] = "obabel.log",
#         work_dir: Optional[str] = ".",
#         keep_logs: bool = True,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__(
#             engine=engine,
#             filetype="smi",
#             output_name=output_name,
#             log_name=log_name,
#             work_dir=work_dir,
#             keep_logs=keep_logs,
#             handlers=handlers,
#             name=name,
#         )

#     def run(self, structure: Union[str, mtr.Structure]) -> str:
#         super().run(structure=structure)

#         with open(
#             f"{mtr.expand(self.output_name,dir=self.work_dir)}.smi", "r"
#         ) as f:
#             smiles, *_ = re.search(r"([^\s]*).*", "".join(f.readlines())).groups()

#         return smiles


# -------------------------- PACKMOL -------------------------- #


class PackmolSolvate(ExternalTask):
    def __init__(
        self,
        shells: int,
        tolerance: float,
        engine: mtr.PackmolEngine,
        io: mtr.IO,
        number_density: Optional[mtr.Qty] = None,
        mass_density: Optional[mtr.Qty] = None,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(engine=engine, io=io, handlers=handlers, name=name)

        self.shells = shells
        self.number_density = number_density
        self.mass_density = mass_density

        self.tolerance = tolerance

    def _packing_params(self, solvent: mtr.Structure) -> Tuple[int, mtr.Qty]:
        if self.number_density is None:
            if self.mass_density is None:
                raise ValueError(
                    "Either mass density or number density required to pack shells."
                )
            if isinstance(solvent, str):
                solvent = mtr.Structure.read(solvent)
            number_density = self.mass_density / solvent.mass
        else:
            number_density = self.number_density

        # these are the ideal gas packing values:
        n = int((2 / 3) * self.shells ** 3)
        sphere_radius = self.shells * (2 * np.pi * number_density) ** (-1 / 3)

        return n, sphere_radius

    def run(
        self, solute: Union[mtr.Structure, str], solvent: Union[mtr.Structure, str],
    ) -> mtr.Structure:
        n, sphere_radius = self._packing_params(solvent=solvent)
        with self.io() as io:
            inp = mtr.PackmolInput(
                tolerance=self.tolerance,
                filetype="xyz",
                output_name=mtr.expand(path="packed", dir=io.work_dir),
            )

            if isinstance(solute, str):
                solute_cm = contextlib.nullcontext(solute)
            else:
                solute_cm = solute.tempfile(suffix=".xyz", dir=io.work_dir)

            if isinstance(solvent, str):
                solvent_cm = contextlib.nullcontext(solvent)
            else:
                solvent_cm = solvent.tempfile(suffix=".xyz", dir=io.work_dir)

            with solute_cm as f, solvent_cm as g:
                inp.add_structure(
                    structure_filepath=mtr.expand(
                        path=f.name if hasattr(f, "name") else f, dir=io.work_dir
                    ),
                    number=1,
                    instructions=["fixed 0. 0. 0. 0. 0. 0."],
                )

                inp.add_structure(
                    structure_filepath=mtr.expand(
                        path=g.name if hasattr(g, "name") else g, dir=io.work_dir
                    ),
                    number=n - 1,
                    instructions=[
                        f"inside sphere 0. 0. 0. {sphere_radius.convert(mtr.angstrom).value}"
                    ],
                )

                inp.write(io.inp)

                self.engine.execute(self.io)

                return mtr.Structure.read(
                    mtr.expand(path="packed.xyz", dir=io.work_dir)
                )


# -------------------------- QCHEM -------------------------- #


class QChemBaseTask(ExternalTask):
    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        raise NotImplementedError

    def parse(self, output: str) -> Any:
        raise NotImplementedError

    def run(
        self,
        structure: Union[mtr.QChemStructure, mtr.QChemFragments, mtr.Structure],
        settings: Optional[mtr.Settings] = None,
    ) -> Any:
        s = mtr.Settings() if settings is None else copy.deepcopy(settings)

        # FIXME: this is essentially a hotpatch to handle fragments - come up with something more elegant/sensible ASAP
        inp = mtr.QChemInput(
            molecule=structure
            if isinstance(structure, mtr.Structure)
            or isinstance(structure, mtr.QChemStructure)
            else mtr.QChemFragments(structures=structure),
            settings=self.defaults(s),
        )

        with self.io() as io:
            inp.write(io.inp)

            self.engine.execute(self.io)

            return self.parse(io.out)


# class ExecuteQChem(QChemBaseTask):
#     def run(self) -> Any:
#         with self.io() as io:
#             self.engine.execute(io.inp, io.out)


class QChemAIMD(QChemBaseTask):
    def parse(self, output: str) -> Any:
        with open(output, "r") as f:
            return "".join(f.readlines())

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "aimd"
        if ("rem", "time_step") not in settings:
            settings["rem", "time_step"] = 1
        if ("rem", "aimd_steps") not in settings:
            settings["rem", "aimd_steps"] = 10
        if ("velocity",) not in settings and (
            "rem",
            "aimd_init_veloc",
        ) not in settings:
            settings["rem", "aimd_init_veloc"] = "thermal"
        if (
            ("rem", "aimd_init_veloc") in settings
            and settings["rem", "aimd_init_veloc"].lower().strip() == "thermal"
            and ("rem", "aimd_temp") not in settings
        ):
            settings["rem", "aimd_temp"] = 300

        return settings


class QChemKoopmanError(Task):
    def __init__(
        self,
        engine: mtr.Engine,
        gs_io: mtr.IO,
        cation_io: mtr.IO,
        anion_io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(
            (engine.num_threads or 1) * (engine.num_processors or 1),
            handlers=handlers,
            name=name,
        )
        self.engine = engine
        self.gs_io = gs_io
        self.cation_io = cation_io
        self.anion_io = anion_io

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method") not in settings:
            settings["rem", "exchange"] = "hf"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "sp"

        return settings

    def run(
        self,
        structure: Union[mtr.QChemStructure, mtr.QChemFragments, mtr.Structure],
        settings: Optional[mtr.Settings] = None,
        num_consumers: Optional[int] = 1,
    ) -> float:
        s = mtr.Settings() if settings is None else copy.deepcopy(settings)

        # if ("structure", "charge") not in settings:
        #     settings["structure", "charge"] = 0
        #     # FIXME: rather than guessing 0, use rdkit.Chem.rdmolops.GetFormalCharge?
        # if ("structure", "multiplicity") not in settings:
        #     settings["structure", "multiplicity"] = 1

        input_settings = InputTask(self.defaults(s))

        gs = QChemSinglePointFrontier(self.engine, self.gs_io)
        gs_structure = InputTask(
            mtr.QChemStructure(structure, charge=0, multiplicity=1)
        )
        gs.requires(structure=gs_structure, settings=input_settings)

        cation = QChemSinglePoint(self.engine, self.cation_io)
        cation_structure = InputTask(
            mtr.QChemStructure(structure, charge=1, multiplicity=2)
        )
        cation.requires(structure=cation_structure, settings=input_settings)

        anion = QChemSinglePoint(self.engine, self.anion_io)
        anion_structure = InputTask(
            mtr.QChemStructure(structure, charge=-1, multiplicity=2)
        )
        anion.requires(structure=anion_structure, settings=input_settings)

        wf = Workflow(
            gs,
            cation,
            anion,
            input_settings,
            gs_structure,
            cation_structure,
            anion_structure,
        )

        out = wf.run(available_cores=self.num_cores, num_consumers=num_consumers)

        energy, homo, lumo = out[0]
        cation = out[1]
        anion = out[2]

        ea = energy - anion
        ip = cation - energy

        J_squared = (ea + lumo) ** 2 + (ip + homo) ** 2

        return np.sqrt(J_squared.convert(mtr.eV ** 2).value.item())


class QChemLRTDDFT(QChemBaseTask):
    def parse(self, output: str) -> Any:
        # FIXME: implement using cclib
        raise NotImplementedError

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "cis_n_roots") not in settings:
            settings["rem", "cis_n_roots"] = 1
        if ("rem", "cis_singlets") not in settings:
            settings["rem", "cis_singlets"] = True
        if ("rem", "cis_triplets") not in settings:
            settings["rem", "cis_triplets"] = False
        if ("rem", "rpa") not in settings:
            settings["rem", "rpa"] = False

        return settings


class QChemMinimizeKoopmanError(Task):
    def __init__(
        self,
        engine: mtr.Engine,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(
            (engine.num_threads or 1) * (engine.num_processors or 1),
            handlers=handlers,
            name=name,
        )
        self.engine = engine
        self.io = io

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "sp"
        if ("rem", "exchange") not in settings:
            settings["rem", "exchange"] = "gen"
        if ("rem", "lrc_dft") not in settings:
            settings["rem", "lrc_dft"] = True
        if ("rem", "src_dft") not in settings:
            settings["rem", "src_dft"] = 2

        return settings

    def run(
        self,
        structure: Union[mtr.QChemStructure, mtr.QChemFragments, mtr.Structure],
        settings: Optional[mtr.Settings] = None,
        epsilon: Optional[Union[int, float]] = 1.0,
        alpha: Optional[float] = 0.2,
        num_evals: Optional[int] = 5,
    ) -> float:
        beta = 1 / epsilon - alpha

        s = self.defaults(settings)
        s["rem", "hf_sr"] = int(round(1000 * alpha))
        s["rem", "hf_lr"] = int(round(1000 * (alpha + beta)))
        s["xc_functional"] = (
            ("X", "HF", alpha),
            ("X", "wPBE", beta),
            ("X", "PBE", 1 - alpha - beta),
            ("C", "PBE", 1.0),
        )

        with self.io() as io:

            def f(omega):
                omega = int(round(1000 * omega))
                s["rem", "omega"] = s["rem", "omega2"] = omega

                wd = mtr.expand(f"{io.work_dir}/{omega}")

                gs_io = mtr.IO("gs.in", "gs.out", wd)
                cation_io = mtr.IO("cation.in", "cation.out", wd)
                anion_io = mtr.IO("anion.in", "anion.out", wd)

                ke = mtr.QChemKoopmanError(self.engine, gs_io, cation_io, anion_io)
                # FIXME: not sure the best way to handle num_consumers here...
                return ke.run(structure, s, num_consumers=3)

            return mtr.MaxLIPOTR(f).run(x_min=1e-3, x_max=1, num_evals=num_evals)


class QChemOptimize(QChemBaseTask):
    def parse(self, output: str) -> Any:
        try:
            parsed = cclib.io.ccread(output)
            # FIXME: is this the correct unit?
            coords = parsed.atomcoords[-1, :, :] * mtr.angstrom
            zs = parsed.atomnos
        except AttributeError:
            return None
        # FIXME: is this the correct unit?
        atoms = (
            mtr.Atom(element=Z, position=p * mtr.angstrom) for Z, p in zip(zs, coords)
        )
        return mtr.Structure(*atoms)

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "opt"

        return settings


class QChemPolarizability(QChemBaseTask):
    def parse(self, output: str) -> Any:
        try:
            polarizability = (
                cclib.io.ccread(output).polarizabilities[-1] * mtr.au_volume
            )
        except AttributeError:
            polarizability = None

        return polarizability

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "polarizability"

        return settings

    def run(
        self,
        structure: Union[mtr.QChemStructure, mtr.QChemFragments, mtr.Structure],
        settings: Optional[mtr.Settings] = None,
    ) -> Any:
        # NOTE: bug workaround for parallel polarizability calculation in Q-Chem 5.2.1
        os.environ["QCINFILEBASE"] = "0"
        return super().run(structure, settings)


# class QChemRTTDDFT(Task):
#     def __init__(
#         self,
#         structure,
#         input_name,
#         output_name,
#         scratch_directory,
#         settings=None,
#         tdscf_settings=None,
#         executable="qchem",
#         work_directory=".",
#         num_cores=1,
#         parallel=False,
#         handlers=None,
#         name=None,
#     ):
#         super().__init__(handlers=handlers, name=name)
#         self.work_directory = mtr.expand(work_directory)
#         self.input_path = mtr.expand(os.path.join(work_directory, input_name))
#         self.output_path = mtr.expand(os.path.join(work_directory, output_name))
#         self.scratch_directory = mtr.expand(scratch_directory)
#         self.executable = executable
#         self.num_cores = num_cores
#         self.parallel = parallel
#         try:
#             os.makedirs(mtr.expand(work_directory))
#         except FileExistsError:
#             pass
#         settings = settings or mtr.Settings()
#         settings["molecule", "structure"] = structure
#         if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
#             settings["rem", "exchange"] = "HF"
#         if ("rem", "basis") not in settings:
#             settings["rem", "basis"] = "3-21G"
#         if ("rem", "rttddft") not in settings:
#             settings["rem", "rttddft"] = 1
#         self.tdscf_settings = tdscf_settings or mtr.Settings()

#     def run(self):
#         tdscf_input_path = mtr.expand(os.path.join(self.work_directory, "TDSCF.prm"))
#         keys = tuple(str(next(iter(k))) for k in self.tdscf_settings)
#         max_length = max(len(k) for k in keys)
#         with open(mtr.expand(tdscf_input_path), "w") as f:
#             f.write(
#                 "\n".join(
#                     k + " " * (max_length - len(k) + 1) + str(self.tdscf_settings[k])
#                     for k in keys
#                 )
#             )
#         mtr.QChemInput(settings=settings).write(filepath=self.input_path)
#         try:
#             os.makedirs(mtr.expand(os.path.join(self.work_directory, "logs")))
#         except FileExistsError:
#             pass
#         os.environ["QCSCRATCH"] = self.scratch_directory
#         with open(self.output_path, "w") as f:
#             if self.parallel:
#                 subprocess.call(
#                     [self.executable, "-nt", str(self.num_cores), self.input_path],
#                     stdout=f,
#                     stderr=subprocess.STDOUT,
#                 )
#             else:
#                 subprocess.call([self.executable, self.input_path], stdout=f)

#         # FIXME: finish with output


class QChemSinglePoint(QChemBaseTask):
    def parse(self, output: str) -> Any:
        try:
            energy = cclib.io.ccread(output).scfenergies * mtr.eV
        except AttributeError:
            energy = None

        return energy

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "sp"

        return settings


class QChemSinglePointFrontier(QChemBaseTask):
    def parse(self, output: str) -> Any:
        try:
            out = cclib.io.ccread(output)
            energy = out.scfenergies * mtr.eV
            moenergies = out.moenergies
            homo_indices = out.homos

            homos = []
            lumos = []

            for moe, h in zip(moenergies, homo_indices):
                homo, lumo = moe[h : h + 2]
                homos.append(homo)
                lumos.append(lumo)

            homo = max(homos) * mtr.eV
            lumo = min(lumos) * mtr.eV
        except AttributeError:
            energy = None
            homo = None
            lumo = None

        return energy, homo, lumo

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method") not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "sp"

        return settings


class WriteQChemInput(Task):
    def __init__(
        self,
        io: mtr.IO,
        handlers: Optional[Iterable[mtr.Handler]] = None,
        name: str = None,
    ) -> None:
        super().__init__(handlers=handlers, name=name)
        self.io = io

    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        return settings

    def run(
        self,
        structure: Union[mtr.QChemStructure, mtr.QChemFragments, mtr.Structure],
        settings: Optional[mtr.Settings] = None,
    ) -> None:
        s = mtr.Settings() if settings is None else copy.deepcopy(settings)
        # FIXME: this is essentially a hotpatch to handle fragments - come up with something more elegant/sensible ASAP
        inp = mtr.QChemInput(
            molecule=structure
            if isinstance(structure, mtr.Structure)
            or isinstance(structure, mtr.QChemStructure)
            else mtr.QChemFragments(structures=structure),
            settings=self.defaults(s),
        )

        with self.io() as io:
            inp.write(io.inp)


class WriteQChemInputGeometryRelaxation(WriteQChemInput):
    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "opt"

        return settings


class WriteQChemInputLRTDDFT(WriteQChemInput):
    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "cis_n_roots") not in settings:
            settings["rem", "cis_n_roots"] = 1
        if ("rem", "cis_singlets") not in settings:
            settings["rem", "cis_singlets"] = True
        if ("rem", "cis_triplets") not in settings:
            settings["rem", "cis_triplets"] = False
        if ("rem", "rpa") not in settings:
            settings["rem", "rpa"] = False

        return settings


class WriteQChemInputPolarizability(WriteQChemInput):
    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"
        if ("rem", "jobtype") not in settings:
            settings["rem", "jobtype"] = "polarizability"

        return settings


class WriteQChemInputSinglePoint(WriteQChemInput):
    def defaults(self, settings: mtr.Settings) -> mtr.Settings:
        if ("rem", "exchange") not in settings and ("rem", "method",) not in settings:
            settings["rem", "exchange"] = "HF"
        if ("rem", "basis") not in settings:
            settings["rem", "basis"] = "3-21G"

        return settings


# class WriteQChemTDSCF(Task):
#     def __init__(
#         self,
#         settings: Optional[mtr.Settings] = None,
#         work_directory: str = ".",
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: str = None,
#     ):
#         super().__init__(handlers=handlers, name=name)
#         self.work_directory = mtr.expand(work_directory)
#         settings = settings

#         try:
#             os.makedirs(mtr.expand(work_directory))
#         except FileExistsError:
#             pass

#     def run(self) -> None:
#         input_path = mtr.expand(os.path.join(self.work_directory, "TDSCF.prm"))

#         keys = tuple(str(next(iter(k))) for k in settings)
#         max_length = max(len(k) for k in keys)

#         with open(mtr.expand(input_path), "w") as f:
#             f.write(
#                 "\n".join(
#                     k + " " * (max_length - len(k) + 1) + str(settings[k]) for k in keys
#                 )
#             )

# -------------------------- QCHEM -------------------------- #

# from __future__ import annotations
# import cclib
# import os
# import mtr
# import subprocess
# from typing import Any, Iterable, Optional

# from ...workflow.tasks.task import Task

# __all__ = ["ExecuteVASP"]


# class ExecuteVASP(Task):
#     def __init__(
#         self,
#         output_name: str,
#         executable: str = "vasp_std",
#         work_directory: str = ".",
#         num_cores: int = 1,
#         parallel: bool = False,
#         handlers: Optional[Iterable[mtr.Handler]] = None,
#         name: Optional[str] = None,
#     ) -> None:
#         super().__init__()
#         self.settings["executable"] = executable
#         self.settings["output_path"] = os.path.join(
#             work_directory, mtr.expand(output_name)
#         )
#         self.settings["work_directory"] = mtr.expand(work_directory)

#         self.settings["num_cores"] = num_cores
#         self.settings["parallel"] = parallel

#         try:
#             os.makedirs(self.settings["work_directory"])
#         except FileExistsError:
#             pass

#     def run(self, **kwargs: Any) -> Any:
#         with open(self.settings["output_path"], "w") as f:
#             if self.settings["parallel"]:
#                 subprocess.call(
#                     [
#                         "mpirun",
#                         "np",
#                         str(self.settings["num_cores"]),
#                         self.settings["executable"],
#                     ],
#                     stdout=f,
#                     stderr=subprocess.STDOUT,
#                 )
#             else:
#                 subprocess.call([self.settings["executable"]], stdout=f)
