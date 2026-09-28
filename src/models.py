#classe base, tem as informações básicas de todo jogo
class Jogo():                                                                            
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao):
        pass

#subclasse de Jogo, especifio para jogos no estilo campanha
class JogoCampanha(Jogo):                                                                                           
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao, progresso, percent_conclusao):
        #o super herda as informações e métodos da subclasse, pegando apenas as informações proprias da subclasse
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao)                              

#subclasse de Jogo, especifico para jogos no estilo competitivo
class JogoCompetitivo(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao, partidas, vit, der, rank, taxa_vit):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao,)
        pass

#subclasse de Jogo para jogos cooperativos
class JogoCooperativo(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao, max_jogadores, sessoes_coop, participantes_frequentes):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao)
        pass

 #classe que agrupa objetos do tipo jogo
class Colecao():   
    pass
