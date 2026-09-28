from DAO.ControladorDAO import ControladorDAO
from enum import Enum

import os

def clearConsole():
    # 'nt' refere-se ao Windows, 'posix' ao Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear') 

def setAtributesObject(objeto, ignore=None):
    if ignore is None:
        ignore = []

    for atribute in vars(objeto):
        if atribute in ignore:
            continue

        value = input(f"Informe o {atribute}: ")
        setattr(objeto, atribute, value)

class Menu():
    WIDTH_BAR = 50

    def __init__(self, DAOController: ControladorDAO = None):
        self.DAOController = DAOController

    def showMenu(self):
        
        while True:
            clearConsole()
            self.printSystemName()
            self.printMenuOptions()
            self.printBar()

            option = input("Digite uma opção: ")
            if option == '0':
                exit()

            self.redirectToSubMenu(option)

    def showSubMenu(self, entidadeClass):
        clearConsole()

        entityName = entidadeClass.getNameModel()
        while True:
            self.printMenuName(entityName)

            print("1 - Incluir")
            print("2 - Atualizar") 
            print("3 - Excluir") 
            print("4 - Pesquisar")   
            print("0 - Voltar")       

            self.printBar()
            
            option = input("Digite uma operação: ")

            clearConsole()
            match option:
                case "0":
                    return
                case "1":
                    
                    obj = entidadeClass()
                    setAtributesObject(obj)
                    self.DAOController.gerenciaDAO(entidadeClass).salvar(obj)
                    if self.confirmOperation():
                        self.DAOController.gerenciaDAO(entidadeClass).persistir(entityName)
                    else:
                        self.DAOController.gerenciaDAO(entidadeClass).apagar(obj.id)
                case "2":
                    self.DAOController.buscar()
                case "3":
                    self.DAOController.carregar()

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

    def printMenuOptions(self):
        i = 0
        for entity in self.DAOController.DAOS:
            i += 1
            print(f"{i} - {entity.getNameModel()}")

        print("0 - Sair")

    def redirectToSubMenu(self, option):
        try:
            entity = list(self.DAOController.DAOS)[int(option) - 1]
            self.showSubMenu(entity)
        except (ValueError, IndexError):
            print("Opção inválida")

    def printMenuName(self, entityName):
        print("\n" + "=" * self.WIDTH_BAR)
        print(" " * 20 + "MENU " + entityName)
        self.printBar()

    def printBar(self):
        print("=" * self.WIDTH_BAR)
    
