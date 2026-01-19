class Cliente:
    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.__cpf = cpf 

    @property
    def cpf(self):
        return self.__cpf