from EntidadeDAO.EntidadeDAO import EntidadeDAO

import os

def limpar_consola():
    # 'nt' refere-se ao Windows, 'posix' ao Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')

# Exemplo de uso:
limpar_consola()

def imprimirMenu2(nomeEntidade, DAO):
    limpar_consola()

    print("------------------------------------")
    print("MENU " + nomeEntidade)
    print("------------------------------------")
    print("0 - Retornar para o menu principal")
    print("1 - Salvar")
    print("2 - Atualizar")
    print("3 - Apagar" )
    print("4 - Buscar" )
    print("5 - Carregar")
    print("6 - Persistir")
    print("7 - Recuperar")
    print("------------------------------------\n")
    

    opcao = int(input("\nDigite uma operacao: "))

    match opcao:
        case 0:
            imprimirMenu1()
        case 1:
            DAO.salvar()
        case 2:
            DAO.atualizar()
        case 3:
            DAO.apagar()
        case 4:
            DAO.buscar()
        case 5:
            DAO.carregar()
        case 6:
            DAO.persistir()
        case 7:
            DAO.recuperar()
        case _:
            print("Opção inválida")  # O '_' funciona como o 'default'

def imprimirMenu1():
    limpar_consola()

    print("+----------------------------------+")
    print("|        BEM VINDO A CODEFIT       |")
    print("+----------------------------------+")

    while True:
        print("1 - Aluno")
        print("2 - Exercicio")
        print("3 - Instrutor")
        print("4 - Ficha")
        print("5 - Item Ficha")
        print("7 - Sair")

        opcao = int(input("Digite uma opção: "))

        match opcao:
            case 1:
                Aluno = EntidadeDAO()
                imprimirMenu2("Aluno", Aluno)
            case 2:
                imprimirMenu2("Exercicio")
            case 3:
                imprimirMenu2("Instrutor")
            case 4:
                imprimirMenu2("Ficha")
            case _:
                print("Opção inválida")  # O '_' funciona como o 'default'

    
