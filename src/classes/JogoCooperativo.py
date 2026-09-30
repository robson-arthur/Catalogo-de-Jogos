import Jogo

#subclasse de Jogo para jogos cooperativos
class JogoCooperativo(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao, max_jogadores, sessoes_coop, participantes_frequentes):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao)
        pass