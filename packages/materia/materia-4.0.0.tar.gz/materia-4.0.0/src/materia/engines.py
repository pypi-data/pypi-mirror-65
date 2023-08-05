from __future__ import annotations
from typing import Dict, Iterable, Optional, Tuple, Union

import ast
import materia as mtr
import pathlib
import re
import shlex
import subprocess

__all__ = [
    "Engine",
    "CCDC",
    "FragIt",
    "GPAW",
    "Multiwfn",
    "Openbabel",
    "Packmol",
    "QChem",
]


class Engine:
    def __init__(
        self,
        executable: str,
        num_processors: Optional[int] = None,
        num_threads: Optional[int] = None,
        arguments: Optional[Iterable[str]] = None,
    ) -> None:

        self.executable = executable
        self.num_processors = num_processors
        self.num_threads = num_threads
        self.arguments = arguments or []

    def env(self) -> Dict[str, str]:
        return {}

    def command(self, inp: str, out: str, work_dir: str) -> str:
        arg_str = " ".join(self.arguments)
        # FIXME: shlex.quote should be used but it doesn't work...
        return shlex.split(f"{self.executable} {arg_str}")

    def execute(self, io_params: materia.IO) -> str:
        with io_params() as io:
            cmd = self.command(io.inp, io.out, io.work_dir)
            with open(io.inp, "r") as inp:
                with open(io.out, "w") as out:
                    subprocess.call(cmd, stdin=inp, stdout=out, env=self.env())

            with open(io.out, "r") as f:
                return "".join(f.readlines())


class CCDC(Engine):
    def __init__(
        self,
        ccdc_root: str,
        num_processors: Optional[int] = None,
        num_threads: Optional[int] = None,
        arguments: Optional[Iterable[str]] = None,
    ) -> None:
        self.ccdc_root = mtr.expand(ccdc_root)
        # FIXME: generalize past 2019 version of CCDC code
        executable = mtr.expand(
            pathlib.Path(
                self.ccdc_root, "Python_API_2019", "miniconda", "bin", "python"
            )
        )
        super().__init__(executable, num_processors, num_threads, arguments)

    def env(self) -> Dict[str, str]:
        # FIXME: generalize past 2019 version of CCDC code
        return {"CSDHOME": mtr.expand(pathlib.Path(self.ccdc_root, "CSD_2019"))}


class FragIt(Engine):
    def __init__(
        self,
        executable: Optional[str] = "fragit",
        arguments: Optional[Iterable[str]] = None,
    ) -> None:

        super().__init__(executable=executable, arguments=arguments)

    def command(self, inp: str, out: str, work_dir: str) -> str:
        arg_str = " ".join(self.arguments)
        # FIXME: shlex.quote should be used but it doesn't work...
        return shlex.split(f"{self.executable} {inp} {arg_str}")


class GPAW(Engine):
    def __init__(
        self,
        executable: Optional[str] = "gpaw",
        num_processors: Optional[int] = None,
        num_threads: Optional[int] = None,
        arguments: Optional[Iterable[str]] = None,
    ) -> None:

        super().__init__(executable, num_processors, num_threads, arguments)

    def execute(self, structure_file):
        raise NotImplementedError


class Multiwfn(Engine):
    def __init__(
        self,
        executable: Optional[str] = "Multiwfn",
        num_processors: Optional[int] = None,
        num_threads: Optional[int] = None,
        arguments: Optional[Iterable[str]] = None,
    ) -> None:

        super().__init__(executable, num_processors, num_threads, arguments)

    def execute(self, io_params: materia.IO) -> str:
        env = self.env()

        with io_params() as io:
            cmd = self.command(io.inp, io.out, io.work_dir)

            with open(io.inp, "r") as inp:
                input_lines = "".join(inp.readlines())

            if self.num_processors is not None:
                input_lines = ["1000\n", "10\n", f"{self.num_processors}\n"]

            with open(io.out, "w") as out:
                # For Multiwfn 3.6
                # FIXME: printf is system-specific - is there any other way to pipe in input_lines?
                pipe_command_string = subprocess.Popen(
                    args=["printf", input_lines],
                    stdout=subprocess.PIPE,
                    encoding="utf-8",
                    env=env,
                )
                multiwfn = subprocess.Popen(
                    cmd,
                    stdin=pipe_command_string.stdout,
                    stdout=out,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    env=env,
                )
                pipe_command_string.stdout.close()
                multiwfn.communicate()


class Openbabel(Engine):
    def __init__(
        self,
        executable: Optional[str] = "obabel",
        arguments: Optional[Iterable[str]] = None,
    ) -> None:
        super().__init__(executable=executable, arguments=arguments)

    def command(self, inp: str, out: str, work_dir: str) -> str:
        arg_str = " ".join(self.arguments)
        # FIXME: shlex.quote should be used but it doesn't work...
        return shlex.split(f"{self.executable} {inp} {arg_str}")


class Packmol(Engine):
    def __init__(self, executable: Optional[str] = "packmol") -> None:
        super().__init__(executable=executable)


class QChem(Engine):
    def __init__(
        self,
        scratch_dir: Optional[str] = None,
        qcenv: Optional[str] = None,
        executable: Optional[str] = "qchem",
        num_processors: Optional[int] = None,
        num_threads: Optional[int] = None,
        arguments: Optional[Iterable[str]] = None,
    ) -> None:
        self.scratch_dir = mtr.expand(scratch_dir) if scratch_dir is not None else None
        self.qcenv = shlex.quote(mtr.expand(qcenv)) if qcenv is not None else None
        super().__init__(
            executable=executable,
            num_processors=num_processors,
            num_threads=num_threads,
            arguments=arguments,
        )

    def env(self) -> Dict[str, str]:
        if self.qcenv is not None:
            # FIXME: shell=True needs to be avoided!!
            d = ast.literal_eval(
                re.match(
                    r"environ\((.*)\)",
                    subprocess.check_output(
                        f". {self.qcenv}; python -c 'import os; print(os.environ)'",
                        shell=True,
                    )
                    .decode()
                    .strip(),
                ).group(1)
            )

        if self.scratch_dir is not None:
            d["QCSCRATCH"] = mtr.expand(self.scratch_dir)

        return d

    def command(self, inp: str, out: str, work_dir: str) -> str:
        cmd = [self.executable]
        if self.arguments is not None:
            cmd.extend(self.arguments)
        if self.num_processors is not None:
            cmd.append(f"-np {self.num_processors}")
        if self.num_threads is not None:
            cmd.append(f"-nt {self.num_threads}")

        # FIXME: shlex.quote should be used but it doesn't work...
        return shlex.split(" ".join(cmd + [inp, out]))
