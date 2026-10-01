from Jogo import *
#subclasse de Jogo, especifio para jogos no estilo campanha
class JogoCampanha(Jogo):                                                                                           
    def __init__(self, titulo, genero, plataforma, status="NÃO INICIADO", horas_jogadas=0.0, avaliacao=0, progresso=0, percent_conclusao=0.0):
        #o super herda as informações e métodos da subclasse, pegando apenas as informações proprias da subclasse
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao)

