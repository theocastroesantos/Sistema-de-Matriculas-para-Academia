from DAO.EntidadeDAO import EntidadeDAO

class ControladorDAO:
    def __init__(self, tipos_DAO):
        self.DAOS = {}

        for tipo_DAO in tipos_DAO:
            self.DAOS[tipo_DAO] = EntidadeDAO()

    def gerenciaDAO(self, tipo_DAO):
        return self.DAOS[tipo_DAO]

# jeito antigo
# class ControladorDAO:
#     def __init__(self, tipo_DAO):
        # self.tipo_DAO = tipo_DAO #o dipo da entidade que vc quer criar um DAO pra ela
        # self.DAOS = {}  #onde armazena todos os DAO ja criados 

    # def gerenciaDAO(self):
    #     if self.tipo_DAO not in self.DAOS:  # aqui so permite que seja criado e armazenado um dao para cada entidade
    #         self.DAOS[self.tipo_DAO] =  EntidadeDAO()

    #     return self.DAOS        #retorna uma dicionario com as entidades que ja tem um DAO  