## o os e sys servem para resolver erros de importação, sendo possível executar os métodos da classe de qualquer arquivo e diretório
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from src.classes.Colecao import Colecao
from src.classes.Jogo import Jogo
from src.classes.JogoCampanha import JogoCampanha
from src.classes.JogoCompetitivo import JogoCompetitivo
from src.classes.JogoCooperativo import JogoCooperativo
from src.database.database import conectar
from sqlite3 import Error   #permite analisar o erro caso aconteça ao tratar os dados

class dados():
    """Interface que trata os métodos CRUD do banco de dados.
    
    Atributos:
    
    nome_banco: str
    
    pasta: str"""

    def __init__(self):
        pass


    ## checar se a tabela existe antes de cria-lá, retorna True se existir, caso contrário retorna False
    def tabela_existe(self, nome_tabela:str):

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            # consulta a tabela interna do SQLite
            cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name=?;
                """, (nome_tabela,))
            ## fetchone() retorna a linha encontrada, ou None se não achar
            resultado = cursor.fetchone()

            conexao.close()

            ## caso o resultado não seja encontrada, a função retorna False
            return resultado is not None


    ## criar tabelas no banco de dados
    def criarTabelasBD(self):

        conexao = conectar()
        if conexao:
            try:
                ## criando cursos para criar tabelas
                cursor = conexao.cursor()

                # habilita chaves estrangeiras no SQLite 
                cursor.execute("PRAGMA foreign_keys = ON;")

                # tabela de coleções: colecoes
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS colecoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_colecao TEXT NOT NULL,
                    numero_jogos INTEGER,
                    jogos TEXT
                    );
                """)

                # tabela de jogos: jogos
                cursor = conexao.cursor()
                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS jogos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL,
                        genero TEXT NOT NULL,
                        plataforma TEXT NOT NULL,
                        status TEXT NOT NULL,
                        horas_jogadas REAL,
                        avaliacao INTEGER
                        );
                """)
                conexao.commit()

                # tabela intermediária: colecoes_jogos serve para relação de muitos para muitos entre coleções e jogos
                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS colecoes_jogos (
                        colecao_id INTEGER,
                        jogo_id INTEGER,
                        PRIMARY KEY (colecao_id, jogo_id),
                        FOREIGN KEY (colecao_id) REFERENCES colecoes(id) ON DELETE CASCADE,
                        FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE
                        );
                """)

                # tabela de jogoscampanha, é relacionada com a tabela jogos pela chave primária ID: jogos_campanha
                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS jogos_campanha (
                        id INTEGER PRIMARY KEY,
                        progresso INTEGER,
                        percent_conclusao REAL,
                        FOREIGN KEY (id) REFERENCES jogos(id) ON DELETE CASCADE
                        );
                """)

                #tabela de jogoscompetitivos: jogos_competitivos
                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS jogos_competitivos (
                        id INTEGER PRIMARY KEY,
                        partidas INTEGER,
                        vit INTEGER,
                        der INTEGER,
                        rank TEXT,
                        taxa_vit REAL,
                        FOREIGN KEY (id) REFERENCES jogos(id) ON DELETE CASCADE
                        );
                """)

                #tabela de jogoscooperativos: jogos_cooperativos
                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS jogos_cooperativos (
                        id INTEGER PRIMARY KEY,
                        max_jogadores INTEGER,
                        sessoes_coop INTEGER,
                        participantes_frequentes TEXT,
                        FOREIGN KEY (id) REFERENCES jogos(id) ON DELETE CASCADE
                        );
                """)

                conexao.commit()

            except Error as e:
                 print(f"Erro ao criar tabelas: {e}")
            finally:
                conexao.close()


    # Tratar coleções
    def adicionarColecao(self, nova_colecao: Colecao):
        
        # checa se a tabela existe no banco de dados
        if not self.tabela_existe("colecoes"):
            self.criarTabelasBD()

        # checa se a variável é do tipo coleção
        if isinstance(nova_colecao, Colecao):
            conexao = conectar()
            if conexao:
                try:
                    cursor = conexao.cursor()

                    cursor.execute(
                            "INSERT INTO colecoes (nome_colecao, numero_jogos, jogos) VALUES (?, ?, ?)",
                            (nova_colecao.nome_colecao, nova_colecao._numero_jogos, nova_colecao.jogos)
                    )
                    conexao.commit()
                except Error as e:
                    print(f"Erro ao adicionar Coleção: {e}")
                finally:
                    conexao.close()
        else:
            raise TypeError("Tipo de coleção inválido")


    # Tratar jogos
    def adicionarJogo(self, novo_jogo):

        if self.buscarJogo(novo_jogo.titulo):
            jogo_achado = self.buscarJogo(novo_jogo.titulo)
            
            ## compara o titulo e a plataforma, se forem iguais, retorna o erro e encerra
            if jogo_achado == novo_jogo:
                return print(f"Jogo com mesmo título e plataforma já cadastrado")
                
        if isinstance(novo_jogo, JogoCampanha):
            self.adicionarJogoCampanha(novo_jogo)
        elif isinstance(novo_jogo, JogoCompetitivo):
            self.adicionarJogoCompetitivo(novo_jogo)
        elif isinstance(novo_jogo, JogoCooperativo):
            self.adicionarJogoCooperativo(novo_jogo)
        else:
            raise TypeError("Tipo de jogo inválido")
            
    def adicionarJogoCampanha(self, novo_jogo: JogoCampanha):

        # checa se a tabela existe
        if not self.tabela_existe("jogos"):
            self.criarTabelasBD()

        #checa se a variável é do tipo JogoCampanha
        if isinstance(novo_jogo, JogoCampanha):
            conexao = conectar()
            if conexao:
                try:
                    cursor = conexao.cursor()

                    cursor.execute(
                        "INSERT INTO jogos (titulo, genero, plataforma, status, horas_jogadas, avaliacao) VALUES (?, ?, ?, ?, ?, ?)",
                        (novo_jogo.titulo, novo_jogo.genero, novo_jogo.plataforma, novo_jogo.status, novo_jogo.horas_jogadas, novo_jogo.avaliacao)
                    )

                    # retorna o id do jogo que foi inserido para usar como id da subclasse
                    jogo_id = cursor.lastrowid

                    cursor.execute(
                        "INSERT INTO jogos_campanha (id, progresso, percent_conclusao) VALUES (?, ?, ?)",
                        (jogo_id, novo_jogo.progresso, novo_jogo.percent_conclusao)
                    )
                    
                    conexao.commit()
                except Error as e:
                    print(f"Erro ao adicionar Jogo: {e}")
                    conexao.rollback()   #desfaz alterações com o cursor caso apareça erros
                finally:
                    conexao.close()
        else:
            raise TypeError("Tipo de jogo inválido")

    def adicionarJogoCompetitivo(self, novo_jogo: JogoCompetitivo):

        # checa se a tabela existe
        if not self.tabela_existe("jogos"):
            self.criarTabelasBD()

        #checa se a variável é do tipo JogoCompetitivo
        if isinstance(novo_jogo, JogoCompetitivo):
            conexao = conectar()
            if conexao:
                try:
                    cursor = conexao.cursor()

                    cursor.execute(
                        "INSERT INTO jogos (titulo, genero, plataforma, status, horas_jogadas, avaliacao) VALUES (?, ?, ?, ?, ?, ?)",
                        (novo_jogo.titulo, novo_jogo.genero, novo_jogo.plataforma, novo_jogo.status, novo_jogo.horas_jogadas, novo_jogo.avaliacao)
                    )

                    # retorna o id do jogo que foi inserido para usar como id da subclasse
                    jogo_id = cursor.lastrowid

                    cursor.execute(
                        "INSERT INTO jogos_competitivos (id, partidas, vit, der, rank, taxa_vit) VALUES (?, ?, ?, ?, ?, ?)",
                        (jogo_id, novo_jogo.partidas, novo_jogo.vit, novo_jogo.der, novo_jogo.rank, novo_jogo.taxa_vit)
                    )
                    
                    conexao.commit()
                except Error as e:
                    print(f"Erro ao adicionar Jogo: {e}")
                    conexao.rollback()   #desfaz alterações com o cursor caso apareça erros
                finally:
                    conexao.close()
        else:
            raise TypeError("Tipo de jogo inválido")

    def adicionarJogoCooperativo(self, novo_jogo: JogoCooperativo):

        # checa se a tabela existe
        if not self.tabela_existe("jogos"):
                self.criarTabelasBD()
    
        #checa se a variável é do tipo JogoCompetitivo
        if isinstance(novo_jogo, JogoCooperativo):
            conexao = conectar()
            if conexao:
                try:
                    cursor = conexao.cursor()

                    cursor.execute(
                        "INSERT INTO jogos (titulo, genero, plataforma, status, horas_jogadas, avaliacao) VALUES (?, ?, ?, ?, ?, ?)",
                        (novo_jogo.titulo, novo_jogo.genero, novo_jogo.plataforma, novo_jogo.status, novo_jogo.horas_jogadas, novo_jogo.avaliacao)
                    )

                    # retorna o id do jogo que foi inserido para usar como id da subclasse
                    jogo_id = cursor.lastrowid

                    copia_participantes = ", ".join(novo_jogo.participantes_frequentes)

                    cursor.execute(
                        "INSERT INTO jogos_cooperativos (id, max_jogadores, sessoes_coop, participantes_frequentes) VALUES (?, ?, ?, ?)",
                        (jogo_id, novo_jogo.max_jogadores, novo_jogo.sessoes_coop, copia_participantes)
                    )
                    
                    conexao.commit()
                except Error as e:
                    print(f"Erro ao adicionar Jogo: {e}")
                    conexao.rollback()   #desfaz alterações com o cursor caso apareça erros
                finally:
                    conexao.close()
        else:
            raise TypeError("Tipo de jogo inválido")

    def buscarJogo(self, titulo_jogo: str):

        conexao = conectar()
        if conexao:
            try:
                cursor = conexao.cursor()

                query = """
                    SELECT 
                        j.titulo, j.genero, j.plataforma, 
                        j.status, j.horas_jogadas, j.avaliacao,
                        jc.progresso, jc.percent_conclusao,
                        jcomp.partidas, jcomp.vit, jcomp.der, jcomp.rank, jcomp.taxa_vit,
                        jcoop.max_jogadores, jcoop.sessoes_coop, jcoop.participantes_frequentes
                    FROM jogos j
                    LEFT JOIN jogos_campanha jc ON j.id = jc.id
                    LEFT JOIN jogos_competitivos jcomp ON j.id = jcomp.id
                    LEFT JOIN jogos_cooperativos jcoop ON j.id = jcoop.id
                    WHERE j.titulo LIKE ?
                """

                # '%' para permitir buscar partes do titulo 
                cursor.execute(query, (f"%{titulo_jogo}%",))
                resultado = cursor.fetchone()

                if not resultado:
                    print(f"Nenhum jogo encontrado com o titulo '{titulo_jogo}'.")
                    return None

                # extraindo os dados da tupla retornada pelo SQL
                titulo, genero, plataforma, status, horas_jogadas, avaliacao, progresso , percent_conclusao, partidas, vit, der, rank, taxa_vit, max_jogadores, sessoes_coop, participantes_frequentes = resultado

                # identificando a subclasse com base em qual campo não é NULO
                if progresso is not None:
                    return JogoCampanha(titulo, genero, plataforma, status , horas_jogadas, avaliacao, progresso, percent_conclusao)
                elif partidas is not None:
                    return JogoCompetitivo(titulo, genero, plataforma, status , horas_jogadas, avaliacao, partidas, vit, der, rank, taxa_vit)
                elif max_jogadores is not None:
                    return JogoCooperativo(titulo, genero, plataforma, status , horas_jogadas, avaliacao, max_jogadores, sessoes_coop, participantes_frequentes)
            except Error as e:
                print(f"Erro ao buscar jogo: {e}")
            finally:
                conexao.close()

    def atualizarJogo(self, novo_jogo: Jogo, titulo_antigo: str):



        if isinstance(novo_jogo, Jogo):
            antigo_jogo = self.buscarJogo(titulo_antigo)


            if not antigo_jogo:
                return print("Jogo não encontrado")
            

            conexao = conectar()
            if conexao:
                try:

                    cursor = conexao.cursor()

                    cursor.execute("PRAGMA foreign_keys = ON;")  # habilita as classes estrangeiras
                     
                    cursor.execute("""
                        UPDATE jogos
                        SET titulo = ?, genero = ?, plataforma = ?, status = ?, horas_jogadas = ?, avaliacao = ?
                        WHERE titulo = ?
                    """, (novo_jogo.titulo, novo_jogo.genero, novo_jogo.plataforma, novo_jogo.status, novo_jogo.horas_jogadas, novo_jogo.avaliacao, antigo_jogo.titulo))

                    jogo_id = cursor.lastrowid

                    if isinstance(novo_jogo, JogoCampanha):
                        cursor.execute("""
                                UPTADE jogos_campanha
                                SET progresso = ?, percent_conclusao
                                WHERE id = ?
                        """, (novo_jogo.progresso, novo_jogo.percent_conclusao, jogo_id))
                    elif isinstance(novo_jogo, JogoCompetitivo):
                        cursor.execute("""
                                UPTADE jogos_competitivos
                                SET partidas = ?, vit = ?, der = ?, rank = ?, taxa_vit = ?
                                WHERE id = ?
                        """, (novo_jogo.partidas, novo_jogo.vit, novo_jogo.der, novo_jogo.rank, novo_jogo.taxa_vit, jogo_id))
                    elif isinstance(novo_jogo, JogoCooperativo):
                        cursor.execute("""
                                UPTADE jogos_cooperativos
                                SET max_jogadores = ?, sessoes_coop = ?, participantes_frequentes = ?
                                WHERE id = ?
                        """, (novo_jogo.max_jogadores, novo_jogo.sessoes_coop, novo_jogo.participantes_frequentes, jogo_id))
                    
                    
                    conexao.commit()

                except Error as e:
                    conexao.rollback()
                    print(f"Erro ao atualizar jogo: {e}")
                finally:
                    conexao.close()
        else:
            raise TypeError("Tipo de jogo inválido")

    # Retorna número de jogos cadastrados e total de horas jogadas
    def relatorioSimples(self):
        conexao = conectar()

        if conexao:
            try:
                cursor = conexao.cursor()

                # retorna o número total de jogos
                cursor.execute("SELECT COUNT[*] FROM jogos;")
                total_jogos = cursor.fetchone()[0]

                #retorna as horas jogadas
                cursor.execute("SELECT SUM[horas_jogadas] FROM jogos;")
                horas_totais = cursor.fetchone()[0]
                resultado_horas = horas_totais if horas_totais is not None else 0.0   # caso não haja jogos no banco e esse valor seja NULL(ou None), ele retorna 0 e não apenas None

                return total_jogos, resultado_horas

            except Error as e:
                print(f"Erro ao retornar relatório simples: {e}")
                conexao.rollback()
            finally:
                conexao.close()