# import dlib
# import numpy as np
# import scipy.interpolate
import re

#
import materia

#
from materia.workflow import Handler
from materia.workflow import (
    QChemModifyRSHParameter,
    QChemIncreaseResponseIterations,
    QChemIncreaseSCFIterations,
    Rerun,
)

#
__all__ = [
    "MinimizeKoopmanError",
    "QChemResponseDIISConvergence",
    "QChemSCFConvergence",
]

# import materia, numpy as np, scipy
#
# def minimize_m_n(m, n, x_min, x_max, num_xs, round=3):
#     xs = np.linspace(x_min,x_max,num_xs)
#     ms = [Power(x=x,p=m) for x in xs]
#     ns = [Power(x=x,p=n) for x in xs]
#     subs = [Subtract() for x in xs]
#     for a,b,sub in zip(ms,ns,subs):
#         sub.requires(a=a,b=b)
#     min = Minimum()
#     min.requires(**{f'f{i}': sub for i,sub in enumerate(subs)})
#     f0,x0 = materia.Workflow(*ms,*ns,*subs,min).run()[3*num_xs]
#     return x0,f0,np.round(x0,round) == np.power(n/m,1/(m-n)).round(round)
#
# class Power(materia.Task):
#     def __init__(self, x, p, handlers=None, name=None):
#         super().__init__(handlers=handlers,name=name)
#         self.x = x
#         self.p = p
#     def run(self):
#         return self.x, self.x**self.p
#
# class Subtract(materia.Task):
#     def run(self, a, b):
#         x,a = a
#         x,b = b
#         return x, a - b
#
# class Minimum(materia.Task):
#     def run(self, **kwargs):
#         xs,fs = zip(*kwargs.values())
#         spline = scipy.interpolate.CubicSpline(xs,fs)
#         candidates = spline.derivative().roots()
#         return min(zip(spline(candidates),candidates))


class MinimizeKoopmanError(Handler):
    def __init__(
        self, omega_min, omega_max, squared_error_threshold=None, input_ids=None
    ):  # FIXME: squared_error -> 1e-9?
        self.omega_min = omega_min
        self.omega_max = omega_max
        self.squared_error_threshold = (
            squared_error_threshold
            if squared_error_threshold is not None
            else materia.Qty(value=1e-3, unit=materia.eV)
        )
        self.koopman_errors = {}

        self.input_ids = (
            tuple(input_ids) if input_ids is not None else ("omega", "koopman_error")
        )

    def check(self, result, task):
        omega, koopman_error = (task_outputs[k] for k in self.input_ids)
        self.koopman_errors[omega] = koopman_error
        return koopman_error > self.squared_error_threshold

    def _get_next_omega(self):
        def _proxy(x):
            try:
                return self.koopman_errors[x].value
            except KeyError:
                raise ValueError(f"{x}")

        try:
            dlib.find_min_global(
                _proxy,
                [self.omega_min,],
                [self.omega_max,],
                len(self.koopman_errors) + 1,
            )
        except ValueError as e:
            return float(str(e))

    def handle(self, result, task):
        raise NotImplementedError
        # create five tasks: omega, gs, cation, anion, koopman_error
        ke = ComputeKoopmanError()
        # links tasks: gs.requires(omega=omega),cation.requires(omega=omega),anion.requires(omega=omega),koopman_error.requires(gs=gs,cation=cation,anion=anion)
        return [InsertTasks(tasks=(omega, gs, cation, anion, koopman_error))]
        # return [QChemModifyRSHParameter(omega=self._get_next_omega()),Rerun()]
        # error_curve_spline = scipy.interpolate.CubicSpline
        # def find_min(f,bounds):
        # x_min,x_max = bounds
        # y = np.linspace(x_min,x_max,5)
        # [x0,],_ = dlib.find_min_global(lambda a: scipy.interpolate.CubicSpline(y,f(y))(a),[min(y),],[max(y),],100)
        # delta = (x_max - x_min)/100
        # z = np.linspace(x0-delta,x0+delta,5)
        # return np.hstack([y,z]),np.hstack([f(y),f(z)]),dlib.find_min_global(lambda a: scipy.interpolate.CubicSpline(z,f(z))(a),[min(z),],[max(z),],100)[0][0]#scipy.optimize.minimize_scalar(scipy.interpolate.CubicSpline(z,f(z)),(min(z),max(z)),method='golden')['x']


class QChemResponseDIISConvergence(Handler):
    def __init__(self, increase_factor=2):
        self.increase_factor = increase_factor

    def check(self, result, task):
        with open(task.io.out, "r") as f:
            if re.search(
                r"DIIS\s*failed\s*to\s*converge\s*within\s*the\s*given\s*number\s*of\s*iterations",
                "".join(f.readlines()),
            ):
                return True

        return False

    def handle(self, result, task):
        return [
            QChemIncreaseResponseIterations(increase_factor=self.increase_factor),
            Rerun(),
        ]


class QChemSCFConvergence(Handler):
    def __init__(self, increase_factor=2):
        self.increase_factor = increase_factor

    def check(self, result, task):
        with open(task.output_path, "r") as f:
            if re.search(
                r"gen_scfman_exception:\s*SCF\s*failed\s*to\s*converge",
                "".join(f.readlines()),
            ):
                return True

        return False

    def handle(self, result, task):
        return [
            QChemIncreaseSCFIterations(increase_factor=self.increase_factor),
            Rerun(),
        ]
