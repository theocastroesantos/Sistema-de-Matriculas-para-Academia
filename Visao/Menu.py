import tkinter as tk
from collections.abc import Callable, Mapping
from tkinter import ttk


FormFactory = Callable[[ttk.Frame], tk.Widget]


class Menu(tk.Tk):
    """Janela principal com navegação lateral e páginas carregadas no painel."""

    NESTED_SECTIONS = {"Ficha": (("Item Ficha", "Itens da ficha"),)}

    def __init__(
        self,
        dao_controller=None,
        form_factories: Mapping[str, FormFactory] | None = None,
    ):
        super().__init__()

        self.title("CODE FIT | Sistema de Matrículas")
        self.geometry("1200x760")
        self.minsize(900, 600)
        self.configure(background="#f3f5f9")

        self.dao_controller = dao_controller
        self.form_factories = dict(form_factories or {})
        self.pages: dict[str, tk.Widget] = {}
        self.navigation_buttons: dict[str, ttk.Button] = {}
        self.sections = self._get_sections()

        self._configure_styles()
        self._build_layout()
        self._register_pages()
        self.show_page("inicio")

    def _get_sections(self) -> list[tuple[str, str]]:
        if self.dao_controller is None:
            return []

        nested_section_keys = {
            child
            for children in self.NESTED_SECTIONS.values()
            for child, _ in children
        }
        return [
            (entity.getNameModel(), entity.getNameModel())
            for entity in self.dao_controller.DAOS
            if entity.getNameModel() not in nested_section_keys
        ]

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.configure("App.TFrame", background="#f3f5f9")
        style.configure("Sidebar.TFrame", background="#172238")
        style.configure(
            "Brand.TLabel",
            background="#172238",
            foreground="#ffffff",
            font=("Arial", 19, "bold"),
        )
        style.configure(
            "Nav.TButton",
            background="#172238",
            foreground="#d9e1ef",
            anchor="w",
            padding=(18, 12),
            font=("Arial", 11),
            borderwidth=0,
        )
        style.map(
            "Nav.TButton",
            background=[("active", "#263651")],
            foreground=[("active", "#ffffff")],
        )
        style.configure(
            "Active.Nav.TButton",
            background="#30466b",
            foreground="#ffffff",
            anchor="w",
            padding=(18, 12),
            font=("Arial", 11, "bold"),
            borderwidth=0,
        )
        style.map("Active.Nav.TButton", background=[("active", "#30466b")])
        style.configure(
            "PageTitle.TLabel",
            background="#f3f5f9",
            foreground="#172238",
            font=("Arial", 23, "bold"),
        )
        style.configure(
            "Body.TLabel",
            background="#f3f5f9",
            foreground="#65718a",
            font=("Arial", 11),
        )
        style.configure(
            "Card.TFrame",
            background="#ffffff",
            relief="solid",
            borderwidth=1,
        )
        style.configure(
            "CardTitle.TLabel",
            background="#ffffff",
            foreground="#172238",
            font=("Arial", 13, "bold"),
        )
        style.configure(
            "CardBody.TLabel",
            background="#ffffff",
            foreground="#65718a",
            font=("Arial", 10),
        )

    def _build_layout(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Frame(self, style="App.TFrame", padding=(28, 18))
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(
            header,
            text="Sistema de Matrículas",
            style="PageTitle.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="CODE FIT",
            style="Body.TLabel",
        ).grid(row=0, column=1, sticky="e")

        self.sidebar = ttk.Frame(self, style="Sidebar.TFrame", width=240)
        self.sidebar.grid(row=1, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.columnconfigure(0, weight=1)
        ttk.Label(
            self.sidebar,
            text="CODE FIT",
            style="Brand.TLabel",
            padding=(20, 24, 16, 24),
        ).grid(row=0, column=0, sticky="ew")

        self._add_navigation_button("inicio", "Início", row=1)
        for row, (key, title) in enumerate(self.sections, start=2):
            self._add_navigation_button(key, title, row=row)

        self.content = ttk.Frame(self, style="App.TFrame", padding=(30, 28))
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

    def _add_navigation_button(self, key: str, title: str, row: int) -> None:
        button = ttk.Button(
            self.sidebar,
            text=title,
            style="Nav.TButton",
            command=lambda page_key=key: self.show_page(page_key),
        )
        button.grid(row=row, column=0, sticky="ew")
        self.navigation_buttons[key] = button

    def _register_pages(self) -> None:
        self.pages["inicio"] = self._create_home_page()

        for key, title in self.sections:
            nested_sections = self.NESTED_SECTIONS.get(key)
            if nested_sections:
                page = self._create_grouped_page(key, title, nested_sections)
            else:
                page = self._create_form_page(self.content, key, title)
            page.grid(row=0, column=0, sticky="nsew")
            page.grid_remove()
            self.pages[key] = page

    def _create_form_page(
        self, parent: ttk.Frame, key: str, title: str
    ) -> tk.Widget:
        factory = self.form_factories.get(key)
        if factory is not None:
            return factory(parent)
        return self._create_form_placeholder(parent, title)

    def _create_grouped_page(
        self,
        key: str,
        title: str,
        nested_sections: tuple[tuple[str, str], ...],
    ) -> ttk.Frame:
        page = ttk.Frame(self.content, style="App.TFrame")
        page.columnconfigure(0, weight=1)
        page.rowconfigure(0, weight=1)

        notebook = ttk.Notebook(page)
        notebook.grid(row=0, column=0, sticky="nsew")
        notebook.bind("<<NotebookTabChanged>>", self._refresh_selected_tab)

        for section_key, tab_title in ((key, title), *nested_sections):
            tab = ttk.Frame(notebook, style="App.TFrame", padding=20)
            notebook.add(tab, text=tab_title)
            self._create_form_page(tab, section_key, tab_title).pack(
                fill="both", expand=True
            )

        return page

    def _create_home_page(self) -> ttk.Frame:
        page = ttk.Frame(self.content, style="App.TFrame")
        page.columnconfigure(0, weight=1)
        ttk.Label(
            page,
            text="Bem-vindo ao CODE FIT",
            style="PageTitle.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            page,
            text="Selecione uma opção no menu para acessar os formulários.",
            style="Body.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(8, 24))

        cards = ttk.Frame(page, style="App.TFrame")
        cards.grid(row=2, column=0, sticky="ew")
        for column in range(2):
            cards.columnconfigure(column, weight=1, uniform="cards")

        for index, (key, title) in enumerate(self.sections):
            card = ttk.Frame(cards, style="Card.TFrame", padding=18)
            card.grid(
                row=index // 2,
                column=index % 2,
                sticky="nsew",
                padx=(0, 12) if index % 2 == 0 else (0, 0),
                pady=(0, 12),
            )
            ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
            ttk.Label(
                card,
                text="Acesse o formulário desta seção.",
                style="CardBody.TLabel",
            ).pack(anchor="w", pady=(7, 12))
            ttk.Button(
                card,
                text="Abrir seção",
                command=lambda page_key=key: self.show_page(page_key),
            ).pack(anchor="w")

        return page

    def _create_form_placeholder(self, parent: ttk.Frame, title: str) -> ttk.Frame:
        page = ttk.Frame(parent, style="App.TFrame")
        page.columnconfigure(0, weight=1)
        ttk.Label(
            page,
            text=f"Formulário de {title}",
            style="PageTitle.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            page,
            text=(
                "Esta área está pronta para receber o formulário desta seção. "
                "Você pode conectá-lo pela opção form_factories."
            ),
            style="Body.TLabel",
            wraplength=700,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(10, 0))
        return page

    def show_page(self, key: str) -> None:
        page = self.pages.get(key)
        if page is None:
            raise KeyError(f"Página não cadastrada: {key}")

        for existing_page in self.pages.values():
            existing_page.grid_remove()
        page.grid()
        self._refresh_descendants(page)

        for page_key, button in self.navigation_buttons.items():
            button.configure(
                style="Active.Nav.TButton" if page_key == key else "Nav.TButton"
            )

    def _refresh_descendants(self, widget: tk.Widget) -> None:
        refresh = getattr(widget, "refresh", None)
        if callable(refresh):
            refresh()
        for child in widget.winfo_children():
            self._refresh_descendants(child)

    def _refresh_selected_tab(self, event) -> None:
        selected_tab = event.widget.nametowidget(event.widget.select())
        self._refresh_descendants(selected_tab)
