from Jogo import *

#subclasse de Jogo, especifico para jogos no estilo competitivo
class JogoCompetitivo(Jogo):
    """Subclasse de Jogo, engloba as partidas totais, número de vitórias, número de derrotas, rank e taxa de vitórias

    Atributos:

    titulo: str

    genero: str

    plataforma: str

    status: str

    horas_jogadas: float

    partidas: int

    vit: int

    der: int

    rank: str

    taxa_vit: float
    """
    def __init__(self, titulo: str, genero: str, plataforma: str, status="NÃO INICIADO", horas_jogadas=0.0, partidas=0, rank="SEM RANK"):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas)
        self.partidas = partidas
        self.__vit = 0
        self.__der = 0  
        self.rank = rank
        self.__taxa_vit = 0.0

    def __str__(self):
        return f"{super().__str__()} \nTotal de partidas: {self.__partidas} \nTotal de vitórias: {self.__vit} \nTotal de derrotas: {self.__der} \nRank: {self.__rank} \nTaxa de vitórias: {self.__taxa_vit}"

    def __eq__(self, other):
        return super().__eq__(other)

    @property
    def partidas(self):
            return self.__partidas
    
    @partidas.setter
    def partidas(self, novas_partidas):
        if isinstance(novas_partidas, int):
            if novas_partidas >= 0:
                self.__partidas = novas_partidas
                self.__vit = 0
                self.__der = 0
            else:
                raise Exception("Valor de partidas inválido")
        else:
            raise TypeError("Tipo da variável partidas inválida")

    @property
    def vit(self):
        return self.__vit

    @property
    def der(self):
        return self.__der

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, novo_rank):
        if isinstance(novo_rank, str):
            if len(novo_rank) == 0:
                raise Exception("Rank vazio inválido")
            elif len(novo_rank) > 20:
                raise Exception("Rank com mais de 20 caracteres")
            else:
                self.__rank = novo_rank            
        else:
            raise TypeError("Tipo da variável rank inválida")

    @property
    def taxa_vit(self):
        return self.__taxa_vit