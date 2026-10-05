
#classe que agrupa objetos do tipo jogo
class Colecao():   
    def __init__(self, nome_colecao):
        self.nome_colecao = nome_colecao
        self.__numero_jogos = 0

    def __str__(self):
        return f"Nome da coleção: {self.__nome_colecao} \nNúmero de jogos: {self.__numero_jogos}"

    def __eq__(self, other):
        if isinstance(other, Colecao):
            ##caso os objetos tenham nomes iguais, retorna True, do contrário retorna False
            return self.__nome_colecao == other.____nome_colecao
        else:
            return "Objeto não pertence a classe Colecao" ##caso o objeto other nao seja da classe Colecao, retorna False

    @property
    def nome_colecao(self):
        return self.__nome_colecao

    @nome_colecao.setter
    def nome_colecao(self, novo_nome):
        if isinstance(novo_nome, str):
            if len(novo_nome) == 0:
                raise Exception("Variável vazia")
            elif len(novo_nome) > 20:
                raise Exception("Nome da coleção maior que 20 caracteres")
            else:
                self.__nome_colecao = novo_nome
        else:
            raise TypeError("Variável não é do tipo str")
    