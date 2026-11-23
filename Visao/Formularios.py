from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from tkinter import ttk

from DAO.Excecao import PersistenceException


@dataclass(frozen=True)
class CampoFormulario:
    chave: str
    rotulo: str
    conversor: Callable[[str], object] = str
    opcoes: Callable[[], Sequence[object]] | None = None
    exibir_opcao: Callable[[object], str] = str
    mensagem_sem_opcoes: str | None = None


ColunaTabela = tuple[str, Callable[[object], object]]
CriadorEntidade = Callable[[int, Mapping[str, object]], object]
SalvarEntidade = Callable[[object, Mapping[str, object]], None]


def listar_registros(dao) -> list[object]:
    try:
        return dao.carregar()
    except PersistenceException:
        return []


class FormularioCadastro(ttk.Frame):
    def __init__(
        self,
        parent,
        titulo: str,
        descricao: str,
        dao,
        campos: Sequence[CampoFormulario],
        colunas: Sequence[ColunaTabela],
        criar_entidade: CriadorEntidade,
        salvar_entidade: SalvarEntidade | None = None,
    ):
        super().__init__(parent, style="App.TFrame")
        self.dao = dao
        self.campos = campos
        self.colunas = colunas
        self.criar_entidade = criar_entidade
        self.salvar_entidade = salvar_entidade or self._salvar_no_dao
        self.entradas: dict[str, ttk.Widget] = {}
        self.opcoes_por_campo: dict[str, dict[str, object]] = {}

        self.columnconfigure(0, weight=1)

        ttk.Label(self, text=titulo, style="PageTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            self,
            text=descricao,
            style="Body.TLabel",
            wraplength=800,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 20))

        self._criar_campos()
        self.status = ttk.Label(self, text="", style="Body.TLabel")
        self.status.grid(row=3, column=0, sticky="w", pady=(8, 12))

        ttk.Separator(self).grid(row=4, column=0, sticky="ew", pady=(0, 14))
        ttk.Label(self, text="Registros cadastrados", style="CardTitle.TLabel").grid(
            row=5, column=0, sticky="nw"
        )
        self._criar_tabela()
        self.refresh()

    def _criar_campos(self) -> None:
        formulario = ttk.Frame(self, style="App.TFrame")
        formulario.grid(row=2, column=0, sticky="ew")
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        for index, campo in enumerate(self.campos):
            coluna = (index % 2) * 2
            linha = (index // 2) * 2
            ttk.Label(formulario, text=campo.rotulo).grid(
                row=linha, column=coluna, sticky="w", padx=(0, 12), pady=(0, 5)
            )

            if campo.opcoes is None:
                entrada = ttk.Entry(formulario)
            else:
                entrada = ttk.Combobox(formulario, state="readonly")
                self.opcoes_por_campo[campo.chave] = {}

            entrada.grid(
                row=linha + 1,
                column=coluna,
                columnspan=2,
                sticky="ew",
                padx=(0, 18),
                pady=(0, 12),
            )
            self.entradas[campo.chave] = entrada

        botoes = ttk.Frame(formulario, style="App.TFrame")
        botoes.grid(
            row=((len(self.campos) + 1) // 2) * 2,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(2, 0),
        )
        ttk.Button(
            botoes,
            text="Cadastrar",
            command=self._cadastrar,
        ).pack(side="left")
        ttk.Button(
            botoes,
            text="Limpar",
            command=self._limpar,
        ).pack(side="left", padx=(8, 0))

    def _criar_tabela(self) -> None:
        tabela_frame = ttk.Frame(self, style="App.TFrame")
        tabela_frame.grid(row=6, column=0, sticky="nsew", pady=(10, 0))
        self.rowconfigure(6, weight=1)
        tabela_frame.columnconfigure(0, weight=1)
        tabela_frame.rowconfigure(0, weight=1)

        self.tabela = ttk.Treeview(
            tabela_frame,
            columns=tuple(f"coluna_{i}" for i in range(len(self.colunas))),
            show="headings",
            height=8,
        )
        for index, (rotulo, _) in enumerate(self.colunas):
            coluna = f"coluna_{index}"
            self.tabela.heading(coluna, text=rotulo)
            self.tabela.column(coluna, width=140, anchor="w")

        barra = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tabela.yview,
        )
        self.tabela.configure(yscrollcommand=barra.set)
        self.tabela.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")

    def refresh(self) -> None:
        registros = self._carregar_registros()
        sem_opcoes = False
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for registro in registros:
            valores = tuple(str(obter(registro)) for _, obter in self.colunas)
            self.tabela.insert("", "end", values=valores)

        for campo in self.campos:
            if campo.opcoes is None:
                continue
            valores = campo.opcoes()
            exibicoes = [campo.exibir_opcao(valor) for valor in valores]
            self.opcoes_por_campo[campo.chave] = dict(zip(exibicoes, valores))
            entrada = self.entradas[campo.chave]
            entrada.configure(values=exibicoes)
            if entrada.get() not in exibicoes:
                entrada.set("")

            if not valores and campo.mensagem_sem_opcoes:
                self._mostrar_status(campo.mensagem_sem_opcoes, erro=True)
                sem_opcoes = True

        if not registros and not sem_opcoes:
            self._mostrar_status("Nenhum registro cadastrado.")

    def _carregar_registros(self) -> list[object]:
        return listar_registros(self.dao)

    def _salvar_no_dao(self, entidade: object, valores: Mapping[str, object]) -> None:
        self.dao.salvar(entidade)
        self.dao.persistir(entidade.getNameModel())

    def _cadastrar(self) -> None:
        try:
            valores = self._ler_valores()
            registros = self._carregar_registros()
            proximo_id = (
                max(
                    (
                        registro.id
                        for registro in registros
                        if isinstance(registro.id, int)
                    ),
                    default=0,
                )
                + 1
            )
            entidade = self.criar_entidade(proximo_id, valores)
            self.salvar_entidade(entidade, valores)
        except (ValueError, PersistenceException, OSError) as erro:
            mensagem = getattr(erro, "erros", None) or str(erro)
            self._mostrar_status(
                mensagem or "Não foi possível cadastrar o registro.",
                erro=True,
            )
            return

        self._limpar()
        self.refresh()
        self._mostrar_status("Cadastro realizado com sucesso.")

    def _ler_valores(self) -> dict[str, object]:
        valores: dict[str, object] = {}
        for campo in self.campos:
            entrada = self.entradas[campo.chave]
            texto = entrada.get().strip()
            if not texto:
                raise ValueError(f"Preencha o campo {campo.rotulo}.")

            if campo.opcoes is None:
                try:
                    valores[campo.chave] = campo.conversor(texto)
                except ValueError as erro:
                    raise ValueError(f"Valor inválido para {campo.rotulo}.") from erro
                continue

            opcao = self.opcoes_por_campo[campo.chave].get(texto)
            if opcao is None:
                raise ValueError(f"Selecione uma opção válida para {campo.rotulo}.")
            valores[campo.chave] = opcao

        return valores

    def _limpar(self) -> None:
        for entrada in self.entradas.values():
            if isinstance(entrada, ttk.Combobox):
                entrada.set("")
            else:
                entrada.delete(0, "end")

    def _mostrar_status(self, texto: str, erro: bool = False) -> None:
        self.status.configure(
            text=texto,
            foreground="#b42318" if erro else "#52627a",
        )


def texto_positivo(texto: str) -> int:
    valor = int(texto)
    if valor <= 0:
        raise ValueError("O valor precisa ser maior que zero.")
    return valor


def construir_formularios(dao_controller) -> dict[str, Callable]:
    from Entidade.Aluno import Aluno
    from Entidade.Exercicio import Exercicio
    from Entidade.FichaTreino import FichaTreino
    from Entidade.Instrutor import Instrutor
    from Entidade.ItemFicha import ItemFicha

    dao_aluno = dao_controller.gerenciaDAO(Aluno)
    dao_exercicio = dao_controller.gerenciaDAO(Exercicio)
    dao_ficha = dao_controller.gerenciaDAO(FichaTreino)
    dao_instrutor = dao_controller.gerenciaDAO(Instrutor)
    dao_item_ficha = dao_controller.gerenciaDAO(ItemFicha)

    def criar_formulario(
        titulo: str,
        descricao: str,
        dao,
        campos: Sequence[CampoFormulario],
        colunas: Sequence[ColunaTabela],
        criar_entidade: CriadorEntidade,
        salvar_entidade: SalvarEntidade | None = None,
    ) -> Callable:
        return lambda parent: FormularioCadastro(
            parent,
            titulo,
            descricao,
            dao,
            campos,
            colunas,
            criar_entidade,
            salvar_entidade,
        )

    def salvar_item_ficha(item: ItemFicha, valores: Mapping[str, object]) -> None:
        dao_item_ficha.salvar(item)
        ficha = valores["ficha"]
        ficha.adicionar_item(item)
        dao_item_ficha.persistir("Item Ficha")
        dao_ficha.persistir("Ficha")

    return {
        "Aluno": criar_formulario(
            "Cadastro de aluno",
            "Informe os dados do aluno para adicioná-lo ao sistema.",
            dao_aluno,
            (
                CampoFormulario("nome", "Nome"),
                CampoFormulario("matricula", "Matrícula"),
            ),
            (
                ("ID", lambda aluno: aluno.id),
                ("Nome", lambda aluno: aluno.nome),
                ("Matrícula", lambda aluno: aluno.matricula),
            ),
            lambda novo_id, valores: Aluno(
                novo_id, valores["nome"], valores["matricula"]
            ),
        ),
        "Instrutor": criar_formulario(
            "Cadastro de instrutor",
            "Informe os dados profissionais do instrutor.",
            dao_instrutor,
            (
                CampoFormulario("nome", "Nome"),
                CampoFormulario("cref", "CREF"),
            ),
            (
                ("ID", lambda instrutor: instrutor.id),
                ("Nome", lambda instrutor: instrutor.nome),
                ("CREF", lambda instrutor: instrutor.cref),
            ),
            lambda novo_id, valores: Instrutor(
                novo_id, valores["nome"], valores["cref"]
            ),
        ),
        "Exercício": criar_formulario(
            "Cadastro de exercício",
            "Cadastre um exercício e seu grupo muscular.",
            dao_exercicio,
            (
                CampoFormulario("nome", "Nome"),
                CampoFormulario("grupo_muscular", "Grupo muscular"),
            ),
            (
                ("ID", lambda exercicio: exercicio.id),
                ("Nome", lambda exercicio: exercicio.nome),
                ("Grupo muscular", lambda exercicio: exercicio.grupo_muscular),
            ),
            lambda novo_id, valores: Exercicio(
                novo_id, valores["nome"], valores["grupo_muscular"]
            ),
        ),
        "Ficha": criar_formulario(
            "Cadastro de ficha de treino",
            "Selecione o aluno e o instrutor responsáveis pela ficha.",
            dao_ficha,
            (
                CampoFormulario(
                    "aluno",
                    "Aluno",
                    opcoes=lambda: listar_registros(dao_aluno),
                    exibir_opcao=lambda aluno: f"{aluno.id} | {aluno.nome}",
                    mensagem_sem_opcoes="Cadastre um aluno antes de criar uma ficha.",
                ),
                CampoFormulario(
                    "instrutor",
                    "Instrutor",
                    opcoes=lambda: listar_registros(dao_instrutor),
                    exibir_opcao=lambda instrutor: f"{instrutor.id} | {instrutor.nome}",
                    mensagem_sem_opcoes="Cadastre um instrutor antes de criar uma ficha.",
                ),
            ),
            (
                ("ID", lambda ficha: ficha.id),
                ("Aluno", lambda ficha: getattr(ficha.aluno, "nome", "")),
                ("Instrutor", lambda ficha: getattr(ficha.instrutor, "nome", "")),
            ),
            lambda novo_id, valores: FichaTreino(
                novo_id,
                aluno=valores["aluno"],
                instrutor=valores["instrutor"],
            ),
        ),
        "Item Ficha": criar_formulario(
            "Cadastro de item da ficha",
            "Escolha uma ficha e um exercício, depois informe séries e repetições.",
            dao_item_ficha,
            (
                CampoFormulario(
                    "ficha",
                    "Ficha",
                    opcoes=lambda: listar_registros(dao_ficha),
                    exibir_opcao=lambda ficha: (
                        f"{ficha.id} | {getattr(ficha.aluno, 'nome', 'Aluno')}"
                    ),
                    mensagem_sem_opcoes="Cadastre uma ficha antes de adicionar itens.",
                ),
                CampoFormulario(
                    "exercicio",
                    "Exercício",
                    opcoes=lambda: listar_registros(dao_exercicio),
                    exibir_opcao=lambda exercicio: f"{exercicio.id} | {exercicio.nome}",
                    mensagem_sem_opcoes="Cadastre um exercício antes de adicionar itens.",
                ),
                CampoFormulario(
                    "series", "Séries", conversor=texto_positivo
                ),
                CampoFormulario(
                    "repeticoes", "Repetições", conversor=texto_positivo
                ),
            ),
            (
                ("ID", lambda item: item.id),
                ("Ficha", lambda item: item.id_ficha),
                ("Exercício", lambda item: getattr(item.exercicio, "nome", "")),
                ("Séries", lambda item: item.series),
                ("Repetições", lambda item: item.repeticoes),
            ),
            lambda novo_id, valores: ItemFicha(
                novo_id,
                exercicio=valores["exercicio"],
                series=valores["series"],
                repeticoes=valores["repeticoes"],
                id_ficha=valores["ficha"].id,
            ),
            salvar_item_ficha,
        ),
    }
