from Entidade import Entidade

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