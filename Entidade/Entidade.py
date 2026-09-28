from abc import ABC, abstractmethod
from typing import List, Set, Optional

class Entidade(ABC):
    def __init__(self, id_entidade: int = None):
        self.id = id_entidade  # todos os filhos de entidade tem ID.

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def getNameModel(cls) -> str:
        pass