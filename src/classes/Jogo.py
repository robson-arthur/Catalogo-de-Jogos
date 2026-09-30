#classe base, tem as informações básicas de todo jogo
class Jogo():                                                                            
    def __init__(self, titulo=str, genero=str, plataforma=str, status="NÃO INICIADO", horas_jogadas=0.0, avaliacao=0):
        self.__titulo = titulo
        self.__genero = genero
        self.__plataforma = plataforma
        self.__status = status
        self.__horas_jogadas = horas_jogadas
        self.__avaliacao = avaliacao

    def __str__(self):
        return f"Nome: {self.__titulo} \nGênero: {self.__genero} \nPlataforma: {self.__plataforma} \nStatus: {self.__status} \nHoras de jogo: {self.__horas_jogadas} \nAvaliação: {self.__avaliacao}"

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, novo_titulo):
        if isinstance(novo_titulo, str):
            if len(novo_titulo) > 0:
                self.__titulo = novo_titulo
            else:
                raise Exception("Título vazio inválido")
        else:
            raise TypeError("Tipo do título inválido")

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, novo_genero):
        if isinstance(novo_genero, str):
            if len(novo_genero) > 0:
                self.__genero = novo_genero
            else:
                raise Exception("Gênero vazio inválido")
        else:
            raise TypeError("Tipo do gênero inválido")

    @property
    def plataforma(self):
        return self.__plataforma

    @genero.setter
    def plataforma(self, nova_plataforma):
        if isinstance(nova_plataforma, str):
            if len(nova_plataforma) > 0:
                self.__genero = nova_plataforma
            else:
                raise Exception("Plataforma vazia inválida")
        else:
            raise TypeError("Tipo da plataforma inválida")

    @property
    def status(self):
        return self.__plataforma

    @genero.setter
    def status(self, nova_plataforma):
        if isinstance(nova_plataforma, str):
            if len(nova_plataforma) > 0:
                self.__genero = nova_plataforma
            else:
                raise Exception("Plataforma vazia inválida")
        else:
            raise TypeError("Tipo do status inválido")

    