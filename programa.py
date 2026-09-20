# o molde ainda nao implementa nenhuma logica, é só a implementação dos pré-requisitos mais básicos.
# decidir implementar as instâncias de 1:N na ficha de treino, que é composta por aluno, instrutor e um atributo array de listas de exercícios, uma vez que uma única instância da classe gerencia muitas outras.
# a biblioteca de tipo é para type hinting, instruir o python o tipo de dado esperado para a variável, sendo representado depois de ":"
# os valores depois de "->" indicam o retorno esperado do método

from abc import ABC, abstractmethod
from typing import List, Set

class Entidade(ABC):
    def __init__(self, id_entidade: int = None):
        self.id = id_entidade  # todos os filhos de entidade tem ID.

    @abstractmethod
    def __str__(self) -> str:
        pass


class Instrutor(Entidade):
    def __init__(self, id_entidade: int = None, nome: str = "", cref: str = ""):
        super().__init__(id_entidade)
        self.nome = nome
        self.cref = cref

    def __str__(self) -> str:
        return f"Instrutor(id={self.id}, nome='{self.nome}', cref='{self.cref}')"


class Aluno(Entidade):
    def __init__(self, id_entidade: int = None, nome: str = "", matricula: str = ""):
        super().__init__(id_entidade)
        self.nome = nome
        self.matricula = matricula

    def __str__(self) -> str:
        return f"Aluno(id={self.id}, nome='{self.nome}', matricula='{self.matricula}')"


class Exercicio(Entidade):
    def __init__(self, id_entidade: int = None, nome: str = "", grupo_muscular: str = ""):
        super().__init__(id_entidade)
        self.nome = nome
        self.grupo_muscular = grupo_muscular

    def __str__(self) -> str:
        return f"Exercicio(id={self.id}, nome='{self.nome}', grupo_muscular='{self.grupo_muscular}')"


class ItemFicha:
    def __init__(self, exercicio=None, series: int = 0, repeticoes: int = 0):
        self.exercicio = exercicio
        self.series = series
        self.repeticoes = repeticoes

    def __str__(self) -> str:
        return f"{self.exercicio}: {self.series} séries x {self.repeticoes} repetições"


class FichaTreino(Entidade):
    # entidade de transação que agrupa instrutores e alunos.
    def __init__(self, id_entidade: int = None, aluno: Aluno = None, instrutor: Instrutor = None):
        super().__init__(id_entidade)
        self.aluno = aluno
        self.instrutor = instrutor
        self.itens: List[ItemFicha] = []  # ficha é uma lista de exercícios.

    def adicionar_item(self, item: ItemFicha) -> None:
        self.itens.append(item)

    def remover_item(self, id_exercicio: int) -> None:
        for item in self.itens:
            if item.exercicio.id == id_exercicio:
                self.itens.remove(item)

    def __str__(self) -> str:
        linhas = []
        linhas.append(f"FICHA DE TREINO: {self.id}")
        linhas.append(f"ALUNO: {self.aluno if self.aluno else 'Não existe'}") # delega ao método da respectiva classe aluno para não quebrar encapsulamento. retorna não existe ao invez de nome se aluno não existir
        linhas.append(f"INSTRUTOR: {self.instrutor if self.instrutor else 'Não existe'}")
        linhas.append(f"EXERCÍCIOS:")

        if not self.itens:
            linhas.append("\tNenhum exercício cadastrado nesta ficha.")
        else:
            for item in self.itens:
                linhas.append(f"\t- {item}")

        return "\n".join(linhas) # mais eficiente que ficar concatenando com +=

class EntidadeDAO:
    def __init__(self):
        self._entidades: Set[Entidade] = set()

    def salvar(self, entidade: Entidade) -> bool:
        pass

    def atualizar(self, entidade: Entidade) -> bool:
        pass

    def apagar(self, id_entidade: int) -> None:
        pass

    def buscar(self, id_entidade: int) -> Entidade:
        pass

    def carregar(self) -> list:
        pass

    def persistir(self, nome_arquivo: str) -> None:
        pass

    def recuperar(self, nome_arquivo: str) -> None:
        pass
