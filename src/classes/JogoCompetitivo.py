import Jogo

#subclasse de Jogo, especifico para jogos no estilo competitivo
class JogoCompetitivo(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao, partidas, vit, der, rank, taxa_vit):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao,)
        pass