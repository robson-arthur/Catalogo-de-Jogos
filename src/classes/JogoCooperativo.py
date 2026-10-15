import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from src.classes.Jogo import Jogo

class JogoCooperativo(Jogo):
    """Subclasse de Jogo para jogos no estilo cooperativo. Engloba o máximo de jogadores, as sessões cooperativas e os participantes frequentes

    Atributos:

    titulo: str

    genero: str

    plataforma: str

    status: str

    horas_jogadas: float

    max_jogadores: int

    sessoes_coop: int

    participantes_frequentes: list[str]
    """
    def __init__(self, titulo, genero, plataforma, status="NÃO INICIADO", horas_jogadas=0.0, avaliacao=0, max_jogadores=0, sessoes_coop=0, participantes_frequentes=[]):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas, avaliacao)
        self._max_jogadores = max_jogadores
        self._sessoes_coop = sessoes_coop
        self.participantes_frequentes = participantes_frequentes

    def __str__(self):
        return f"{super().__str__()} \nMáximo de jogadores: {self._max_jogadores} \nSessões coop: {self._sessoes_coop} \nParticipantes frequente: {self._participantes_frequentes}"

    def __eq__(self, other):
        return super().__eq__(other)

    @property
    def max_jogadores(self):
        return self._max_jogadores

    @max_jogadores.setter
    def max_jogadores(self, novo_max):
        if isinstance(novo_max, int):
            if novo_max > 0:
                self._max_jogadores = novo_max
            else:
                raise Exception("Valor de max_jogadores inválido")
        else:
            raise TypeError("Tipo da variável max_jogadores inválida")

    @property
    def sessoes_coop(self):
        return self._sessoes_coop

    @sessoes_coop.setter
    def sessoes_coop(self, nova_sessoes):
        if isinstance(nova_sessoes, int):
            if nova_sessoes > 0:
                self._sessoes_coop = nova_sessoes
            else:
                raise Exception("Valor de sessoes_coop inválido")
        else:
            raise TypeError("Tipo da variável sessoes_coop inválida")

    @property
    def participantes_frequentes(self):
        return self._participantes_frequentes

    @participantes_frequentes.setter
    def participantes_frequentes(self, nova_lista):
        if isinstance(nova_lista, list):
            self._participantes_frequentes = nova_lista
        elif isinstance(nova_lista, str):
            copia_lista = nova_lista.split(", ")
            self._participantes_frequentes = copia_lista

