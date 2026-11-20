from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar
from DAO.EntidadeDAO import EntidadeDAO
from Entidade.Entidade import Entidade
 
class PersistenceException(Exception):
    def __init__(
        self,
        operacao: str,
        problema: str,
        valor: Optional[Entidade | Any] = None,
    ):
        self.operacao = operacao
        self.problema = problema
        self.valor = valor
        mensagem = f"[{operacao}] {problema}"
        if valor is not None:
            mensagem += f" Valor: {valor}"
        super().__init__(mensagem)
 
 
E = TypeVar("E", bound=Entidade) # E está limitado por entidade ou subclasses entidade. 
 
 
class ControladorDAO:
    _instancia: Optional["ControladorDAO"] = None  # opcionalmente a instancia deve ser entidade ou none.
    _daos: Dict[Type[Entidade], EntidadeDAO]
    _inicializado: bool = False # em primeira análise o sistema não está inicializado
 
    def __new__(cls, tipos_DAO: Optional[Iterable[Type[Entidade]]] = None) -> "ControladorDAO":
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._daos = {}
        return cls._instancia # se já existe, retorna a referencia.
 
    def __init__(self, tipos_DAO: Optional[Iterable[Type[Entidade]]] = None) -> None:
        if not self._inicializado:
            if tipos_DAO is not None:
                for tipo_DAO in tipos_DAO:
                    self._registrar_dao(tipo_DAO)
            self._inicializado = True
        elif tipos_DAO is not None:
            for tipo_DAO in tipos_DAO:
                self._registrar_dao(tipo_DAO)
 
    def _registrar_dao(self, tipo_DAO: Type[Entidade]) -> None:
        if not isinstance(tipo_DAO, type) or not issubclass(tipo_DAO, Entidade) or tipo_DAO is Entidade:
            raise PersistenceException(
                "inicializar DAO",
                "Tipo inválido ou não é subclasse de Entidade",
                tipo_DAO,
            )
        if tipo_DAO not in self._daos:
            self._daos[tipo_DAO] = EntidadeDAO()
 
    @property # cria um atributo somente de leitura para evitar modificações erradas.
    def DAOS(self) -> Dict[Type[Entidade], EntidadeDAO]:
        return dict(self._daos)
 
    def gerenciaDAO(self, tipo_DAO: Type[E]) -> EntidadeDAO:
        if not isinstance(tipo_DAO, type) or not issubclass(tipo_DAO, Entidade) or tipo_DAO not in self._daos:
            raise PersistenceException(
                "gerenciar DAO",
                "Entidade não gerenciada pelo controlador",
                tipo_DAO,
            )
        return self._daos[tipo_DAO]
 
    def salvar(self, entidade: E) -> None:
        if not isinstance(entidade, Entidade):
            raise PersistenceException("salvar", "objeto não é uma instância de Entidade", entidade)
        self.gerenciaDAO(type(entidade)).salvar(entidade)
 
    def atualizar(self, entidade: E) -> None:
        if not isinstance(entidade, Entidade):
            raise PersistenceException("atualizar", "Objeto não é uma instância de Entidade", entidade)
        self.gerenciaDAO(type(entidade)).atualizar(entidade)
 
    def apagar(self, tipo_DAO: Type[E], id_entidade: Any) -> E:
        return self.gerenciaDAO(tipo_DAO).apagar(id_entidade)
 
    def buscar(self, tipo_DAO: Type[E], id_entidade: Any) -> E:
        return self.gerenciaDAO(tipo_DAO).buscar(id_entidade)
 
    def carregar(self, tipo_DAO: Type[E]) -> List[E]:
        return self.gerenciaDAO(tipo_DAO).carregar()
 
    def persistir(self, tipo_DAO: Type[E], nome_arquivo: Optional[str] = None) -> None:
        arquivo = nome_arquivo if nome_arquivo is not None else tipo_DAO.__name__
        self.gerenciaDAO(tipo_DAO).persistir(arquivo)
 
    def recuperar(self, tipo_DAO: Type[E], nome_arquivo: Optional[str] = None) -> None:
        arquivo = nome_arquivo if nome_arquivo is not None else tipo_DAO.__name__
        self.gerenciaDAO(tipo_DAO).recuperar(arquivo)