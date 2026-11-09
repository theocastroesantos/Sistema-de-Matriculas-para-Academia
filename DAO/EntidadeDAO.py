from typing import Set, List, Optional
import pickle

class EntidadeDAO:
    def __init__(self):
        self._entidades = set()

    def buscar(self, id_entidade: int):
        for entidade in self._entidades:
            if str(entidade.id) == str(id_entidade):
                return entidade
        return None

    def salvar(self, entidade) -> bool:
        if self.buscar(entidade.id) is not None:
            return False
        self._entidades.add(entidade)
        return True

    def atualizar(self, entidade) -> bool:
        entidade_antiga = self.buscar(entidade.id)
        if entidade_antiga is None:
            return False
        self._entidades.remove(entidade_antiga)
        self._entidades.add(entidade)
        return True

    def apagar(self, id_entidade: int):
        entidade_alvo = self.buscar(id_entidade)
        if entidade_alvo is None:
            return None
        self._entidades.remove(entidade_alvo)
        return entidade_alvo
    
    def carregar(self):
        return sorted(list(self._entidades), key=lambda e: e.id) # sorted() recebe a lista criada e a reordena. o parâmetro key utiliza uma função anônima (lambda) que faz o algoritmo olhar o atributo id de cada objeto e para determinar a sua posição final

    def persistir(self, nome_arquivo: str) -> None:
        with open(nome_arquivo, "wb") as arquivo: # abre em formato de escrever 
            pickle.dump(self._entidades, arquivo)

    def recuperar(self, nome_arquivo: str) -> None: # tratamento de exceção se o arquivo não existe
        try:
            with open(nome_arquivo, "rb") as arquivo:
                self._entidades = pickle.load(arquivo)
        except FileNotFoundError:
            self._entidades = set() #se o arquivo não existe ainda inicia com set vazio
