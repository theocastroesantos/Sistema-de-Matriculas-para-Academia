from Visao.Formularios import construir_formularios
from Visao.Menu import Menu
from DAO.ControladorDAO import ControladorDAO
from Entidade.Aluno import Aluno
from Entidade.Exercicio import Exercicio
from Entidade.FichaTreino import FichaTreino
from Entidade.ItemFicha import ItemFicha
from Entidade.Instrutor import Instrutor

class Program:
    @staticmethod
    def main():
        dao_controller = ControladorDAO(
            [Aluno, Exercicio, FichaTreino, ItemFicha, Instrutor]
        )
        for entidade in dao_controller.DAOS:
            dao_controller.gerenciaDAO(entidade).recuperar(entidade.getNameModel())

        form_factories = construir_formularios(dao_controller)
        Menu(dao_controller, form_factories=form_factories).mainloop()


if __name__ == "__main__":
    Program.main()
