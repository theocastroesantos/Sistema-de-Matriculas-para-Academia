from typing import Set, List, Optional
import pickle
from excecao  import PersistenceException
from typing import TypeVar, Generic
from Entidade.Entidade import Entidade

E = TypeVar("E", bound=Entidade)

class EntidadeDAO(Generic[E]):

    def __init__(self):
        self._entidades: set[E] = set()

    def buscar(self, id_entidade: int) -> E:
        for entidade in self._entidades:
            if str(entidade.id) == str(id_entidade):
                return entidade
        raise PersistenceException("buscar",id_entidade,"entidade nao encontrada")

    def salvar(self, entidade:E) -> bool:
        try:
            self.buscar(entidade.id)

        except PersistenceException:
            self._entidades.add(entidade)
            return True

        raise PersistenceException("salvar",entidade.id, "entidade ja existe" )
            

    def atualizar(self, entidade:E) -> bool:
        try:
            entidade_antiga = self.buscar(entidade.id)

        except PersistenceException:
            raise PersistenceException("atualizar", entidade.id, "entidade nao encontrada")
        
        else:
            self._entidades.remove(entidade_antiga)
            self._entidades.add(entidade)
            return True

    def apagar(self, id_entidade: int) -> E:
        try:    
            entidade_alvo = self.buscar(id_entidade)
        except PersistenceException: 
            raise PersistenceException("apagar", id_entidade, "entidade nao encontrada")
        else:        
            self._entidades.remove(entidade_alvo)
            return entidade_alvo
    
    def carregar(self) -> list[E]:

        if not self._entidades:
            raise PersistenceException("carregar",None,"conjunto vazio")
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
