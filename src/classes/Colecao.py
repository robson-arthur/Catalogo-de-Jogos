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
    
    jogos: list[str]
    """

    def __init__(self, nome_colecao: str, numero_jogos=0, jogos=[]):
        self.nome_colecao = nome_colecao
        self._numero_jogos = numero_jogos
        self.jogos = jogos

    def __str__(self):
        return f"{self._nome_colecao}, {self._numero_jogos}, {self._jogos}"
    
    def __repr__(self):
        return f"Nome da coleção: {self._nome_colecao} Número de jogos: {self._numero_jogos} Jogos: {self._jogos}"

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
        return self._jogos

    @jogos.setter
    def jogos(self, novos_jogos):
        if isinstance(novos_jogos, list):
            self._jogos = novos_jogos
        elif isinstance(novos_jogos, str):
            copia_lista = novos_jogos.split(", ")
            self._jogos = copia_lista
        else:
            raise TypeError("Tipo de jogos inválido(lista ou string)")

    def adicionarJogo(self, novo_jogo: Jogo):
        if isinstance(novo_jogo, Jogo):
            self._jogos.append(novo_jogo.titulo)
        else:
            raise TypeError("Tipo de jogo inválido")

    def removerJogo(self, jogo: Jogo):
        if isinstance(jogo, Jogo):
            self._jogos.remove(jogo.titulo)
        else:
            raise TypeError("Tipo de jogo inválido")

    def listarJogos(self):
        print("="*100)
        print(f"Jogos de {self.nome_colecao}:")
        print("-"*100)
        for jogo in self.jogos:
            print(jogo)
        print("="*100)