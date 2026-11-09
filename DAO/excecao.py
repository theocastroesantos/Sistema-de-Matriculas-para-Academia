from DAO.EntidadeDAO import DAO


class PersistenceException(Exception):
    def __init__ (self, operacao, valor, erros):
        self.operacao = operacao
        self.valor = valor 
        self.erros = erros

        mensagem = (f" erro ao {self.operacao} : {self.erros} valor: {self.valor}")

        super.__init__(mensagem)





    


