#classe base, tem as informações básicas de todo jogo
class Jogo():                                                                            
    def __init__(self, titulo=str, genero=str, plataforma=str, status="NÃO INICIADO", horas_jogadas=0.0, avaliacao=0):
        #atributos: __titulo, __genero, __plataforma, __status, __horas_jogadas, __avaliacao. todos são privados e possuem getter e setter
        #apenas os atributos titulo, genero e plataforma são obrigatórios, os outros são definidos por padrão como acima
        self.titulo = titulo
        self.genero = genero
        self.plataforma = plataforma
        self.status = status
        self.horas_jogadas = horas_jogadas
        self.avaliacao = avaliacao

    def __str__(self):
        return f"Nome: {self.__titulo} \nGênero: {self.__genero} \nPlataforma: {self.__plataforma} \nStatus: {self.__status} \nHoras de jogo: {self.__horas_jogadas} \nAvaliação: {self.__avaliacao}"

    def __eq__(self, other):
        if isinstance(other, Jogo):
            return self.__titulo == other.__titulo and self.__plataforma == other.__plataforma
        else:
            return False ##caso o objeto other nao seja da classe Jogo, o retorna False

    
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
            raise TypeError("Tipo da variável título inválido")

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
            raise TypeError("Tipo da variável do gênero inválido")

    @property
    def plataforma(self):
        return self.__plataforma

    @plataforma.setter
    def plataforma(self, nova_plataforma):
        if isinstance(nova_plataforma, str):
            if len(nova_plataforma) > 0:
                self.__plataforma = nova_plataforma
            else:
                raise Exception("Plataforma vazia inválida")
        else:
            raise TypeError("Tipo da variável da plataforma inválido")

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, nova_plataforma):
        if isinstance(nova_plataforma, str):
            if not (len(nova_plataforma) > 0):
                raise Exception("Status vazio inválido")
            if nova_plataforma not in ["NÃO INICIADO", "JOGANDO", "FINALIZADO"]:
                raise Exception("Categoria de Status inválida")
            else:
                self.__status = nova_plataforma
        else:
            raise TypeError("Tipo da variável do status inválido")

    @property
    def horas_jogadas(self):
        return self.__horas_jogadas

    @horas_jogadas.setter
    def horas_jogadas(self, nova_hora):
        if isinstance(nova_hora, float) or isinstance(nova_hora, int):
            if nova_hora >= 0:
                self.__horas_jogadas = nova_hora
            else:
                raise Exception("Hora menor que zero")
        else:
            raise TypeError("Hora não é do tipo válido")

    @property
    def avaliacao(self):
        return self.__avaliacao

    @avaliacao.setter
    def avaliacao(self, nova_avaliacao):
        if isinstance(nova_avaliacao, int):
            if nova_avaliacao in range(0,11):
                self.__avaliacao = nova_avaliacao
            else:
                raise Exception("Avaliação fora do intervalo esperado")
        else:
            raise TypeError("Tipo da variável da avaliação inválido")
