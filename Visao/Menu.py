
from tkinter import *


class Calculadora(Tk):

    def __init__(self):
        super().__init__()

        self.title("CODE FIT")
        self.resizable(False, False)
        self.geometry("1920x1080")

        self.valor = None
        self.operador = None

        f = ("Arial", 20)

        self.criaPainel()
        self.criaDisplay(f)
        self.criaBotoes(f)

    def criaPainel(self):
        painel = LabelFrame(
            self,
            text="Meu Painel",
            padx=10,
            pady=10
        )
        painel.pack(padx=20, pady=20)

        # Carrega a imagem
        self.imagem = PhotoImage(file="imagens/logo_menu.png")

        # Exibe a imagem
        rotulo_img = Label(painel, image=self.imagem)
        rotulo_img.pack()

    def criaDisplay(self, f):
        self.display = Entry(self, font=f)
        self.display.pack()

    def criaBotoes(self, f):

        p1 = Frame(self)
        p1.pack()

        self.btsoma = Button(
            p1, text="Teste", width=10,
            font=f, command=self.opSoma
        )
        self.btsoma.pack(side=LEFT)

        self.btsubt = Button(
            p1, text="Teste13232", width=10,
            font=f, command=lambda: self.cliqueOP("-")
        )
        self.btsubt.pack(side=LEFT)

        p2 = Frame(self)
        p2.pack()

        self.btmult = Button(
            p2, text="Teste412432", width=10,
            font=f, command=lambda: self.cliqueOP("*")
        )
        self.btmult.pack(side=LEFT)

        self.btdivi = Button(
            p2, text="Aluno", width=10,
            font=f, command=lambda: self.cliqueOP("/")
        )
        self.btdivi.pack(side=LEFT)

        p3 = Frame(self)
        p3.pack()

        self.btrstd = Button(
            p3, text="=", width=10,
            font=f, command=self.cliqueRstd
        )
        self.btrstd.pack(side=LEFT)

        self.btzera = Button(
            p3, text="C", width=10,
            font=f, command=self.cliqueZera
        )
        self.btzera.pack(side=LEFT)

    def opSoma(self):
        self.cliqueOP("+")

    def executaOperacao(self):
        s = self.display.get()

        if self.operador == "+":
            self.valor += float(s)
        elif self.operador == "-":
            self.valor -= float(s)
        elif self.operador == "*":
            self.valor *= float(s)
        elif self.operador == "/":
            self.valor /= float(s)
        else:
            print("Operação inválida")

    def cliqueOP(self, operador):

        if self.valor is None:
            self.valor = float(self.display.get())
        else:
            self.executaOperacao()

        self.operador = operador

        self.display.delete(0, END)
        self.display.focus_force()

        print(self.valor, " | ", self.operador)

    def cliqueRstd(self):

        if (self.valor, self.operador) == (None, None):
            return

        self.executaOperacao()

        print(self.valor, " | ", self.operador)

        self.display.delete(0, END)
        self.display.insert(0, str(self.valor))

        self.valor = None
        self.operador = None

    def cliqueZera(self):
        self.valor = None
        self.operador = None

        self.display.delete(0, END)
        self.display.focus_force()


Calculadora().mainloop()
