from andes.core.solver import Solver
from andes.core.config import Config
from collections import OrderedDict


class BaseRoutine(object):
    """
    Base routine class to provide instances for system, config, and solver.
    """

    def __init__(self, system=None, config=None):
        self.system = system
        self.config = Config(self.class_name)

        if config is not None:
            self.config.load(config)

        self.config.add(OrderedDict((('sparselib', 'klu'),
                                     )))

        self.solver = Solver(sparselib=self.config.sparselib)

    @property
    def class_name(self):
        return self.__class__.__name__
