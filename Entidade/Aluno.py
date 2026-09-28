from Entidade.Entidade import Entidade
from typing import List, Set

class Aluno(Entidade):
    def __init__(self, id_entidade: int = None, nome: str = "", matricula: str = ""):
        super().__init__(id_entidade)
        self.nome = nome
        self.matricula = matricula

    def __str__(self) -> str:
        return f"Aluno(id={self.id}, nome='{self.nome}', matricula='{self.matricula}')"

    @classmethod
    def getNameModel(cls) -> str:
        return "Aluno"