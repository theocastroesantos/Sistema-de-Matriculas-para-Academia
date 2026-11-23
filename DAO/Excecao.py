from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar
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