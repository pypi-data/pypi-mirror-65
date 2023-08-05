import abc
import functools

import materia as mtr

__all__ = ["Handler"]


class Handler(abc.ABC):
    def run(self, result, task):
        if self.check(result=result, task=task):
            raise mtr.ActionSignal(
                result=result, actions=self.handle(result=result, task=task)
            )

    @abc.abstractmethod
    def check(self, result, task):
        # input: result of task to be checked and the task object itself
        # output: True if output indicates that self.handle should be called, else False
        pass

    @abc.abstractmethod
    def handle(self, result, task):
        # input: result of task to be checked and the task object itself
        # output: Actions object containing actions to be performed in order to repair task
        return []
