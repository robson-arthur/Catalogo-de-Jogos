import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from src.classes.Jogo import Jogo

class Colecao():
    """Objeto que agrupa outros objetos do tipo Jogo

    Atributos:

    nome_colecao: str

    numero_jogos: int
    
    jogos: list[Jogo]
    """

    def __init__(self, nome_colecao: str, numero_jogos=0, jogos=""):
        self.nome_colecao = nome_colecao
        self._numero_jogos = numero_jogos
        self._jogos = jogos

    def __str__(self):
        return f"{self._nome_colecao}, {self._numero_jogos}, {self._jogos}"
    
    def __repr__(self):
        return f"Nome da coleção: {self._nome_colecao} \nNúmero de jogos: {self._numero_jogos} \nJogos: {self._jogos}"

    def __eq__(self, other):
        if isinstance(other, Colecao):
            ##caso os objetos tenham nomes iguais, retorna True, do contrário retorna False
            return self._nome_colecao == other._nome_colecao
        else:
            return "Objeto não pertence a classe Colecao" ##caso o objeto other nao seja da classe Colecao, retorna False

    @property
    def nome_colecao(self):
        return self._nome_colecao

    @nome_colecao.setter
    def nome_colecao(self, novo_nome):
        if isinstance(novo_nome, str):
            if len(novo_nome) == 0:
                raise Exception("Variável vazia")
            elif len(novo_nome) > 20:
                raise Exception("Nome da coleção maior que 20 caracteres")
            else:
                self._nome_colecao = novo_nome
        else:
            raise TypeError("Variável não é do tipo str")

    @property
    def jogos(self):
        return f"{self._jogos}"
