from abc import ABC, abstractmethod
from typing import List, Set, Optional

class Entidade(ABC):
    def __init__(self, id_entidade: int):
        self.__id = id_entidade

    @property # 
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    def __eq__(self, outro) -> bool:
        if isinstance(outro, Entidade):
            return self.id == outro.id
        return False

    def __ne__(self, outro) -> bool:
        return not self.__eq__(outro)

    def __lt__(self, outro) -> bool:
        if isinstance(outro, Entidade):
            return self.id < outro.id
        return NotImplemented

    def __le__(self, outro) -> bool:
        if isinstance(outro, Entidade):
            return self.id <= outro.id
        return NotImplemented

    def __gt__(self, outro) -> bool:
        if isinstance(outro, Entidade):
            return self.id > outro.id
        return NotImplemented

    def __ge__(self, outro) -> bool:
        if isinstance(outro, Entidade):
            return self.id >= outro.id
        return NotImplemented

    def __hash__(self) -> int: # força o python a somente usar o id para calcular o endereço
        return hash(self.id)