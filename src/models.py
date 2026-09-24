class Jogo():                                                                            #classe base, tem as informações básicas de todo jogo
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao):
        pass

class JogoCampanha(Jogo):                                                                                           #subclasse de Jogo
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao, progresso, percent_conclusao):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao)                              #o super herda as  
        pass                                                                                                        #informações da subclasse

class JogoCompetitivo(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao, partidas, vit, der, rank, taxa_vit):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao,)
        pass

class JogoCooperativo(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao, max_jogadores, sessoes_coop, participantes_frequentes):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao)
        pass

class Colecao():    #classe que agrupa objetos do tipo jogo
    pass

class Usuario():    #classe que agrupa coleções
    pass