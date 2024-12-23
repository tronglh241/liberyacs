from abc import ABC, abstractmethod, abstractproperty

from liberyacs import CfgNode


class Case(ABC):
    @abstractproperty
    def config_file(self) -> str:
        pass

    @abstractproperty
    def evaluate(self) -> bool:
        pass

    @abstractmethod
    def check(self) -> None:
        pass

    def load_config(self) -> CfgNode:
        config = CfgNode.load(self.config_file, self.evaluate)
        return config
