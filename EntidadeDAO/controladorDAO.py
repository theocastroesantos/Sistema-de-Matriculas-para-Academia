from EntidadeDAO import EntidadeDAO

class cotrolador:
    def __init__(self,tipo_DAO):
        self.tipo_DAO = tipo_DAO #o dipo da entidade que vc quer criar um DAO pra ela
        self.DAOS = {}  #onde armazena todos os DAO ja criados 

    def gerenciaDAO(self):
        if self.tipo_DAO not in self.DAOS:  # aqui so permite que seja criado e armazenado um dao para cada entidade
            self.DAOS[self.tipo_DAO] =  EntidadeDAO()

        return self.DAOS        #retorna uma dicionario com as entidades que ja tem um DAO  