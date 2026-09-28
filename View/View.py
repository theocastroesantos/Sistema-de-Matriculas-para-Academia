from EntidadeDAO.ControladorDAO import ControladorDAO
from enum import Enum

import os

def clearConsole():
    # 'nt' refere-se ao Windows, 'posix' ao Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear') 

def preencher_objeto(objeto, ignore=None):
    if ignore is None:
        ignore = []

    for atributo in vars(objeto):
        if atributo in ignore:
            continue

        valor = input(f"Informe o {atributo}: ")
        setattr(objeto, atributo, valor)

class Menu():
    WIDTH_BAR = 50

    def __init__(self, DAOController: ControladorDAO = None):
        self.DAOController = DAOController

    def showMenu(self):
        
        while True:
            clearConsole()
            self.printSystemName()
            self.printMenuOptions(self.DAOController)
            self.printBar()

            option = input("Digite uma opção: ")
            if option == '0':
                exit()

            self.redirectToSubMenu(self.DAOController, option)

    def subMenu(self, ControladorDAO, entidadeClass):
        clearConsole()

        entityName = entidadeClass.getNameModel()
        while True:
            self.printMenuName(entityName)

            print("1 - Incluir")
            print("2 - Atualizar") 
            print("3 - Excluir") 
            print("4 - PecontroladorDAOsquisar")   
            print("0 - Voltar")       

            self.printBar()
            
            opcao = input("Digite uma operação: ")

            clearConsole()
            match opcao:
                case "0":
                    self.menu_principal()
                case "1":
                    
                    object = entidadeClass()
                    preencher_objeto(object)
                    ControladorDAO.gerenciaDAO(entidadeClass).salvar(object)
                    if self.confirmOperation():
                        ControladorDAO.gerenciaDAO(entidadeClass).persistir(entityName)
                    else:
                        ControladorDAO.gerenciaDAO(entidadeClass).apagar(object.id)
                case "2":
                    ControladorDAO.buscar()
                case "3":
                    ControladorDAO.carregar()

    def confirmOperation(self) -> bool:
        while True:
            clearConsole()

            self.printBar()
            print("Deseja prosseguir com a operação?")
            self.printBar()
            print("1 - SIM")
            print("2 - NÃO")

            self.printBar()

            opcao = input("Digite uma opção: ")

            match opcao:
                case "1":
                    return True
                case "2":
                    return False

    def printSystemName(self):
        print("\n" + "=" * self.WIDTH_BAR)
        print(" BEM VINDO A CODEFIT ")
        self.printBar()

    def printMenuOptions(self, DAOController):
        i = 0
        for entity in DAOController.DAOS:
            i += 1
            print(f"{i} - {entity.getNameModel()}")

        print("0 - Sair")

    def redirectToSubMenu(self, DAOController, option):
        try:
            entity = list(DAOController.DAOS)[int(option) - 1]
            self.subMenu(DAOController, entity)
        except (ValueError, IndexError):
            print("Opção inválida")

    def printMenuName(self, entityName):
        print("\n" + "=" * self.WIDTH_BAR)
        print(" " * 20 + "MENU " + entityName)
        self.printBar()

    def printBar(self):
        print("=" * self.WIDTH_BAR)
    
