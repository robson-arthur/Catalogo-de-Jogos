from Jogo import *
#subclasse de Jogo, especifio para jogos no estilo campanha
class JogoCampanha(Jogo):                                                                                           
    def __init__(self, titulo, genero, plataforma, status="NÃO INICIADO", horas_jogadas=0.0, avaliacao=0, progresso=0, percent_conclusao=0.0):
        #o super herda as informações e métodos da subclasse, pegando apenas as informações proprias da subclasse
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao)
        self.progresso = progresso
        self.percent_conclusao = percent_conclusao

    def __str__(self):
        return f"{super().__str__()} \nProgesso de missões/capitulos: {self.__progresso} \nPercentual de conclusão: {self.__percent_conclusao}"

    ##usa o msm __eq__ da classe pai
    def __eq__(self, other):
        return super().__eq__(other)

    @property
    def progresso(self):
        return self.__progresso

    @progresso.setter
    def progresso(self, novo_progresso):
        if isinstance(novo_progresso, int):
            if novo_progresso >= 0 and novo_progresso < 1000:
                self.__progresso = novo_progresso
            else:
                raise Exception("Valor de progresso inválido")
        else:
            raise TypeError("Tipo da variável progesso inválida")

    @property
    def percent_conclusao(self):
        return self.__percent_conclusao

    @percent_conclusao.setter
    def percent_conclusao(self, novo_percent):
        if isinstance(novo_percent, float):
            if novo_percent >= 0 and novo_percent <= 100:
                self.__percent_conclusao = novo_percent
            else:
                raise Exception("Valor de percentual inválido")
        else:
            raise TypeError("Tipo da variável percentual de conclusão inválida")
    

