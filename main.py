from View.View import Menu
from DAO.ControladorDAO import ControladorDAO
from Entidade.Aluno import Aluno
from Entidade.Exercicio import Exercicio
from Entidade.FichaTreino import FichaTreino
from Entidade.ItemFicha import ItemFicha
from Entidade.Instrutor import Instrutor

class Program:
    @staticmethod
    def main():
        DAOController = ControladorDAO([Aluno, Exercicio, FichaTreino, ItemFicha, Instrutor])
        menu = Menu(DAOController)
        menu.showMenu()


if __name__ == "__main__":
    Program.main()
