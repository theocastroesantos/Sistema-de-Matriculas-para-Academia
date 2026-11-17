from Entidade.Entidade import Entidade
from Entidade.Instrutor import Instrutor
from typing import List, Set

class ItemFicha(Entidade):
    def __init__(
        self,
        id_entidade: int = None,
        exercicio=None,
        series: int = 0,
        repeticoes: int = 0,
        id_ficha: int = None,
    ):
        super().__init__(id_entidade)
        self.exercicio = exercicio
        self.series = series
        self.repeticoes = repeticoes
        self.id_ficha = id_ficha

    def __setstate__(self, state: dict) -> None:
        super().__setstate__(state)
        if not hasattr(self, "id_ficha"):
            self.id_ficha = None

    def __str__(self) -> str:
        # hassattr = "has atribute" - verifica se determinado objeto tem tal variável tem tal atributo. se sim, imprime o NOME e não a referência.
        return f"{self.exercicio.nome if hasattr(self.exercicio, 'nome') else self.exercicio} - {self.series} séries x {self.repeticoes} repetições"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def getNameModel(cls) -> str:
        return "Item Ficha"
