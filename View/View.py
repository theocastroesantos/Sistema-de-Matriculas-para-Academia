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

class OperationDAO(Enum):

    NONE = (0, "0", "Voltar")
    INSERT = (1, "1", "Inserir")
    UPDATE = (2, "2", "Atualizar")
    DELETE = (3, "3", "Excluir")
    SEARCH = (4, "4", "Buscar")
    SEARCH_ALL = (5, "5", "Buscar Todos")

    def __init__(self, code, char, operationName):
        self.code = code
        self.char = char
        self.operationName = operationName

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

        dao = self.DAOController.gerenciaDAO(entidadeClass)
        entityName = entidadeClass.getNameModel()
        
        while True:
            clearConsole()
            self.printMenuName(entityName)
            option = self.getOperationSelected()
            clearConsole()
            match option:
                case OperationDAO.NONE:
                    return
                
                case OperationDAO.INSERT:            
                    obj = entidadeClass()
                    setAtributesObject(obj)
                    dao.salvar(obj)
                    if self.confirmOperation():
                        dao.persistir(entityName)
                        clearConsole()
                        print("Registro inserido com sucesso!")
                    else:
                        clearConsole()
                        print("Inserção do registro cancelada!")    
                        dao.apagar(obj.id)

                case OperationDAO.UPDATE:
                    id_busca = input("Informe o ID do registro que deseja atualizar: ")        
                    obj_existente = dao.buscar(id_busca) 
                    if obj_existente: # se existe...
                        setAtributesObject(obj_existente, ignore=["id"])
                        dao.atualizar(obj_existente) 
                        if self.confirmOperation():
                            dao.persistir(entityName)
                            clearConsole()
                            print("Registro atualizado com sucesso!")
                        else:
                            clearConsole()
                            print("Atualização do registro cancelada!")
                            dao.recuperar(entityName) 
                    else:
                        print("Registro não encontrado.")

                case OperationDAO.DELETE:
                    id = input(f"digite o id do {entityName}:")
                    obj_busca = dao.buscar(id)

                    if obj_busca:
                        
                        if self.confirmOperation():
                            dao.apagar(id)
                            dao.persistir(entityName)
                            print(f"{entityName} apagado com sucesso")

                        else:
                            print("operação concelada")

                    else:
                        print(f"{entityName} não existe")
                        
                       

                case OperationDAO.SEARCH:
                    id_busca = input(f"Informe o ID do(a) {entityName}: ")
                
                    obj_encontrado = dao.buscar(id_busca)
                    
                    self.printMenuName(f"RESULTADO DA BUSCA - {entityName}")
                    if obj_encontrado:
                        for atribute, value in vars(obj_encontrado).items():
                            print(f"  {atribute}: {value}")
                        self.printBar()
                    else:
                        print(f"Nenhum registo de {entityName} encontrado com o ID '{id_busca}'.")       

                case OperationDAO.SEARCH_ALL:
                    objetos = dao.carregar()
                    
                    self.printMenuName(f"LISTA DE {entityName}")
                    if objetos: 
                        for obj in objetos:
                            for atribute, value in vars(obj).items(): 
                                print(f"  {atribute}: {value}")
                            self.printBar()
                    else:
                        print(f"Nenhum registro de {entityName} encontrado.")   

            input("\nAperte enter para continuar...")                   

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
        print(" " * 20 + entityName)
        self.printBar()

    def getOperationSelected(self):
        for operation in OperationDAO:
            print(f"{operation.char} - {operation.operationName}")

        self.printBar()

        option = input("Digite uma operação: ")

        operationSelected = next(
            (
                operation
                for operation in OperationDAO
                if operation.char == option
            ),
            OperationDAO.NONE
        )

        return operationSelected

    def printBar(self):
        print("=" * self.WIDTH_BAR)
    
