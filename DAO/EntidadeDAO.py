import pickle
from typing import Any, Generic, Set, Tuple, TypeVar
from ControladorDAO import PersistenceException
from Entidade.Entidade import Entidade

E = TypeVar("E", bound=Entidade)


class EntidadeDAO(Generic[E]):
    def __init__(self) -> None:
        self._entidades: Set[E] = set()

    def buscar(self, id_entidade: Any) -> E:
        for entidade in self._entidades:
            if entidade.id == id_entidade or str(entidade.id) == str(id_entidade):
                return entidade
        raise PersistenceException("buscar", "entidade não encontrada", id_entidade)

    def salvar(self, entidade: E) -> None:
        if not isinstance(entidade, Entidade):
            raise PersistenceException("salvar", "objeto não instanciado em entidade", entidade)

        if entidade in self._entidades:
            raise PersistenceException("salvar", "entidade já existe no conjunto", entidade.id)

        try:
            self._entidades.add(entidade)
        except Exception as erro:
            raise PersistenceException("salvar", f"erro ao adicionar entidade: {erro}", entidade)

    def atualizar(self, entidade: E) -> None:
        if not isinstance(entidade, Entidade):
            raise PersistenceException("atualizar", "objeto não instanciado em entidade", entidade)

        entidade_antiga = self.buscar(entidade.id)
        self._entidades.remove(entidade_antiga)
        self._entidades.add(entidade)

    def apagar(self, id_entidade: Any) -> E:
        entidade_alvo = self.buscar(id_entidade)
        self._entidades.remove(entidade_alvo)
        return entidade_alvo

    def carregar(self) -> Tuple[E, ...]:
        if not self._entidades:
            raise PersistenceException("carregar", "conjunto vazio")
        return tuple(sorted(self._entidades))

    def persistir(self, nome_arquivo: str) -> None:
        try:
            with open(nome_arquivo, "wb") as arquivo:
                pickle.dump(self._entidades, arquivo)
        except (OSError, pickle.PickleError) as erro:
            raise PersistenceException("persistir", f"falha ao gravar arquivo: {erro}", nome_arquivo)

    def recuperar(self, nome_arquivo: str) -> None:
        try:
            with open(nome_arquivo, "rb") as arquivo:
                dados = pickle.load(arquivo)
                if not isinstance(dados, set):
                    raise PersistenceException("recuperar", "formatação de dados inválida no arquivo", nome_arquivo)
                self._entidades = set(dados)
        except FileNotFoundError:
            self._entidades = set()
        except (OSError, pickle.UnpicklingError, EOFError) as erro:
            raise PersistenceException("recuperar", f"arquivo corrompido: {erro}", nome_arquivo)
