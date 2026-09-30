import Jogo
#subclasse de Jogo, especifio para jogos no estilo campanha
class JogoCampanha(Jogo):                                                                                           
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao, progresso, percent_conclusao):
        #o super herda as informações e métodos da subclasse, pegando apenas as informações proprias da subclasse
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao) 