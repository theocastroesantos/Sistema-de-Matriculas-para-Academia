from Entidade.Entidade import Entidade
from typing import List, Set

class Exercicio(Entidade):
    def __init__(self, id_entidade: int = None, nome: str = "", grupo_muscular: str = ""):
        super().__init__(id_entidade)
        self.nome = nome
        self.grupo_muscular = grupo_muscular

    def __str__(self) -> str:
        return f"Exercicio(id={self.id}, nome='{self.nome}', grupo_muscular='{self.grupo_muscular}')"

    @classmethod
    def getNameModel(cls) -> str:
        return "Exercício"