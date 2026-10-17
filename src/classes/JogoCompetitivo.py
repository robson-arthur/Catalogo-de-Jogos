import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from src.classes.Jogo import Jogo

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
    def __init__(self, titulo: str, genero: str, plataforma: str, status="NÃO INICIADO", horas_jogadas=0.0, avaliacao=0, partidas=0, vit=0, der=0, rank="SEM RANK", taxa_vit=0.0):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao)
        self.partidas = partidas
        self._vit = vit
        self._der = der  
        self.rank = rank
        self._taxa_vit = taxa_vit

    def __str__(self):
        return f"{super().__str__()}, {self._partidas}, {self._vit}, {self._der}, {self._rank}, {self._taxa_vit}"

    def __repr__(self):
        return f"{super().__str__()} \nTotal de partidas: {self._partidas} \nTotal de vitórias: {self._vit} \nTotal de derrotas: {self._der} \nRank: {self._rank} \nTaxa de vitórias: {self._taxa_vit}"

    def __eq__(self, other):
        return super().__eq__(other)

    @property
    def partidas(self):
            return self._partidas
    
    @partidas.setter
    def partidas(self, novas_partidas):
        if isinstance(novas_partidas, int):
            if novas_partidas >= 0:
                self._partidas = novas_partidas
                self._vit = 0
                self._der = 0
            else:
                raise Exception("Valor de partidas inválido")
        else:
            raise TypeError("Tipo da variável partidas inválida")

    @property
    def vit(self):
        return self._vit

    @property
    def der(self):
        return self._der

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, novo_rank):
        if isinstance(novo_rank, str):
            if len(novo_rank) == 0:
                raise Exception("Rank vazio inválido")
            elif len(novo_rank) > 20:
                raise Exception("Rank com mais de 20 caracteres")
            else:
                self._rank = novo_rank            
        else:
            raise TypeError("Tipo da variável rank inválida")

    @property
    def taxa_vit(self):
        return self._taxa_vit