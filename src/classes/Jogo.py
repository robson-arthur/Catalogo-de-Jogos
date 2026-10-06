#classe base, tem as informações básicas de todo jogo
class Jogo():                                                                            
    def __init__(self, titulo=str, genero=str, plataforma=str, status="NÃO INICIADO", horas_jogadas=0.0):
        #atributos: _titulo, _genero, _plataforma, _status, _horas_jogadas, _avaliacao. todos são privados e possuem getter e setter
        #apenas os atributos titulo, genero e plataforma são obrigatórios, os outros são definidos por padrão como acima
        self.titulo = titulo
        self.genero = genero
        self.plataforma = plataforma
        self.status = status
        self.horas_jogadas = horas_jogadas
        self._avaliacao = 0

    def __str__(self):
        return f"Nome: {self._titulo} \nGênero: {self._genero} \nPlataforma: {self._plataforma} \nStatus: {self._status} \nHoras de jogo: {self._horas_jogadas} \nAvaliação: {self._avaliacao}"

    def __eq__(self, other):
        if isinstance(other, Jogo):
            ##caso os objetos tenham título e plataforma igual, retorna True, do contrário retorna False
            return self._titulo == other._titulo and self._plataforma == other._plataforma
        else:
            return "Objeto não pertence a classe Jogo" ##caso o objeto other nao seja da classe Jogo, retorna False
    
    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, novo_titulo):
        if isinstance(novo_titulo, str):
            if len(novo_titulo) == 0:
                raise Exception("Título vazio inválido")
            elif len(novo_titulo) > 20:                                   ## maior número de caracteres é 20
                raise Exception("Título com mais de 20 caracteres")
            else:
                self._titulo = novo_titulo
        else:
            raise TypeError("Tipo da variável título inválido")

    @property
    def genero(self):
        return self._genero

    @genero.setter
    def genero(self, novo_genero):
        if isinstance(novo_genero, str):
            if len(novo_genero) == 0:
                raise Exception("Gênero vazio inválido")
            elif len(novo_genero) > 20:
                raise Exception("Gênero com mais de 20 caracteres inválido")
            else:
                self._genero = novo_genero
        else:
            raise TypeError("Tipo da variável do gênero inválido")

    @property
    def plataforma(self):
        return self._plataforma

    @plataforma.setter
    def plataforma(self, nova_plataforma):
        if isinstance(nova_plataforma, str):
            if len(nova_plataforma) == 0:
                raise Exception("Plataforma vazia inválida")
            elif len(nova_plataforma) > 10:
                raise Exception("Plataforma com mais de 10 caracteres inválida")
            else:
                self._plataforma = nova_plataforma
        else:
            raise TypeError("Tipo da variável da plataforma inválido")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, novo_status):
        if isinstance(novo_status, str):
            if not (len(novo_status) > 0):
                raise Exception("Status vazio inválido")
            elif novo_status not in ["NÃO INICIADO", "JOGANDO", "FINALIZADO"]:
                raise Exception("Categoria de Status inválida")
            else:
                self._status = novo_status
        else:
            raise TypeError("Tipo da variável do status inválido")

    @property
    def horas_jogadas(self):
        return self._horas_jogadas

    @horas_jogadas.setter
    def horas_jogadas(self, nova_hora):
        if isinstance(nova_hora, float) or isinstance(nova_hora, int):
            if nova_hora >= 0:
                self._horas_jogadas = nova_hora
            else:
                raise Exception("Hora menor que zero")
        else:
            raise TypeError("Hora não é do tipo válido")

    @property
    def avaliacao(self):
        return self._avaliacao

    @avaliacao.setter
    def avaliacao(self, nova_avaliacao):
        if isinstance(nova_avaliacao, int):
            if self._status == "FINALIZADO":
                if nova_avaliacao in range(0,11):
                    self._avaliacao = nova_avaliacao
                else:
                    raise Exception("Avaliação fora do intervalo esperado")
            else:
                raise Exception("Jogo não finalizado, avaliação indisponível")
        else:
            raise TypeError("Tipo da variável da avaliação inválido")
