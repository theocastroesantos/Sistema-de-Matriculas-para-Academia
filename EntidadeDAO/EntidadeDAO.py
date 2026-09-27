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
