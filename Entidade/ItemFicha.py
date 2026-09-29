from Entidade.Entidade import Entidade
from Entidade.Instrutor import Instrutor
from typing import List, Set

class ItemFicha(Entidade):
    def __init__(self, id_entidade: int = None, exercicio=None, series: int = 0, repeticoes: int = 0):
        super().__init__(id_entidade)
        self.exercicio = exercicio
        self.series = series
        self.repeticoes = repeticoes

    def __str__(self) -> str:
        return f"{self.exercicio}: {self.series} séries x {self.repeticoes} repetições"

    @classmethod
    def getNameModel(cls) -> str:
        return "Item Ficha"