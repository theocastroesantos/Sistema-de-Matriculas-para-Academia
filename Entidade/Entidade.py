from abc import ABC, abstractmethod
from typing import List, Set, Optional

class Entidade(ABC):
    def __init__(self, id_entidade: int):
        self.__id = id_entidade

    def __setstate__(self, state: dict) -> None:
        state = dict(state)
        tinha_id_legado = "id" in state
        id_legado = state.pop("id", None)
        self.__dict__.update(state)

        if "_Entidade__id" not in self.__dict__ and tinha_id_legado:
            if isinstance(id_legado, str):
                try:
                    id_legado = int(id_legado)
                except ValueError:
                    pass
            self.id = id_legado

    @property # 
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    def __eq__(self, outro) -> bool:
        if isinstance(outro, Entidade):
            if not hasattr(self, "_Entidade__id") or not hasattr(
                outro, "_Entidade__id"
            ):
                # O pickle pode comparar itens do set antes de restaurar o ID.
                return self is outro
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

    def __hash__(self) -> int:
        if not hasattr(self, "_Entidade__id"):
            # EntidadeDAO recria o set após a restauração dos IDs.
            return 0
        return hash(self.id)