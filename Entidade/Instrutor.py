from Entidade import Entidade
from typing import List, Set

class Instrutor(Entidade):
    def __init__(self, id_entidade: int = None, nome: str = "", cref: str = ""):
        super().__init__(id_entidade)
        self.nome = nome
        self.cref = cref

    def __str__(self) -> str:
        return f"Instrutor(id={self.id}, nome='{self.nome}', cref='{self.cref}')"