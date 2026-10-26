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
from sqlite3 import Error, IntegrityError   #permite analisar o erro caso aconteça ao tratar os dados

class dados():
    """Interface que trata os métodos CRUD do banco de dados.
    
    Atributos:
    
    nome_banco: str
    
    pasta: str"""

    def __init__(self):
        pass

    # Tratar coleções
    def adicionarColecao(self, nova_colecao: Colecao):
        
        # checa se a variável é do tipo coleção
        if isinstance(nova_colecao, Colecao):
            conexao = conectar()
            if conexao:
                try:
                    cursor = conexao.cursor()

                    
                    cursor.execute(
                            "INSERT INTO colecoes (nome_colecao, numero_jogos, jogos) VALUES (?, ?, ?)",
                            (nova_colecao.nome_colecao, nova_colecao._numero_jogos, None)
                    )
                    conexao.commit()
                    
                    print(f"Coleção {nova_colecao.nome_colecao} adicionada com sucesso")

                    return True
                except Error as e:
                    print(f"Erro ao adicionar Coleção: {e}")
                    return False
                finally:
                    conexao.close()
        else:
            raise TypeError("Tipo de coleção inválido")

    def removerColecao(self, nome_colecao: str):
        if isinstance(nome_colecao, str):
            conexao = conectar()
            if conexao:
                try:
                    cursor = conexao.cursor()
                    cursor.execute("PRAGMA foreign_keys = ON;")

                    cursor.execute("DELETE FROM colecoes WHERE nome_colecao = ?", (nome_colecao,))
                    conexao.commit()

                    if cursor.rowcount > 0:
                        print(f"Coleção {nome_colecao} foi removida")
                        return True
                    else:
                        print(f"Nenhuma coleção encontrada com o nome {nome_colecao}.")
                        return False

                except Error as e:
                    conexao.rollback()
                    print(f"Erro ao remover coleção: {e}")
                    return False
                finally:
                    conexao.close()
        else:
            raise TypeError("Tipo de nome de coleção inválido")

    def adicionarJogoColecao(self, jogo: Jogo, colecao: Colecao):
        conexao = conectar()

        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                cursor.execute("""
                    SELECT id 
                    FROM jogos
                    WHERE titulo = ?;
                """, (jogo.titulo,))
                
                jogo_id = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT id
                    FROM colecoes
                    WHERE nome_colecao = ?;
                """, (colecao.nome_colecao,))

                colecao_id = cursor.fetchone()[0]
                
                # Insere a relação na tabela intermediária
                cursor.execute("""
                    INSERT INTO colecoes_jogos (colecao_id, jogo_id)
                    VALUES (?, ?);
                """, (colecao_id, jogo_id))

                conexao.commit()
                print(f"Jogo {jogo.titulo} adicionado à coleção {colecao.nome_colecao} com sucesso!")

                return True

            except IntegrityError as e:
                # erro costuma acontecer se o jogo já estiver nessa coleção (por causa da Primary Key composta)
                conexao.rollback()
                print(f"Erro: O jogo já pertence a esta coleção: {e}")
                return False
            except Error as e:
                conexao.rollback()
                print(f"Erro ao adicionar jogo a coleção: {e}")
            finally:
                conexao.close()

    def buscarColecao(self, nome_colecao):
        conexao = conectar()
        if conexao:
            try:
                cursor = conexao.cursor()

                cursor.execute("""
                    SELECT nome_colecao, numero_jogos, jogos 
                    FROM colecoes 
                    WHERE nome_colecao LIKE ?
                """, (f"%{nome_colecao}%",))

                colecao = cursor.fetchone()

                if not colecao:
                    print(f"Nenhuma coleção com o nome: {nome_colecao} encontrado")
                    return None

                nome_colecao, numero_jogos, jogos = colecao

                return Colecao(nome_colecao=nome_colecao, numero_jogos=numero_jogos, jogos=jogos)
            
            except Error as e:
                print(f"Erro ao buscar coleção: {e}")
            finally:
                conexao.close()

    def atualizarColecao(self, nova_colecao: Colecao, nome_antigo: str):
        if isinstance(nova_colecao, Colecao):
            antiga_colecao = self.buscarColecao(nome_antigo)

            if not antiga_colecao:
                return print("Coleção não encontrado")
        
            conexao = conectar()
            if conexao:
                try:

                    cursor = conexao.cursor()

                    cursor.execute("PRAGMA foreign_keys = ON;")  # habilita as classes estrangeiras

                    if len(nova_colecao.jogos) > 0:
                        jogos_str = ", ".join(nova_colecao.jogos)
                    else:
                        jogos_str = None
                    
                    cursor.execute("""
                        UPDATE colecoes
                        SET nome_colecao = ?, numero_jogos = ?, jogos = ?
                        WHERE nome_colecao = ?
                    """, (nova_colecao.nome_colecao, nova_colecao._numero_jogos, jogos_str, antiga_colecao.nome_colecao))

                    conexao.commit()

                except Error as e:
                    conexao.rollback()
                    print(f"Erro ao atualizar coleção: {e}")
                finally:
                    conexao.close()
        else:
            raise TypeError("Tipo inválido de coleção")

    # Tratar jogos
    def adicionarJogo(self, novo_jogo):  # retorna True caso o jogo tenha sido cadastrado, False caso já tenha um jogo com o mesmo nome e plataforma

        #chea o tipo da variável novo_jogo
        if isinstance(novo_jogo, Jogo):

            if self.buscarJogo(novo_jogo.titulo):
                jogo_achado = self.buscarJogo(novo_jogo.titulo)
                
                ## compara o titulo e a plataforma, se forem iguais, retorna o erro e encerra
                if jogo_achado == novo_jogo:
                    print(f"Jogo '{novo_jogo.titulo} e plataforma {novo_jogo.plataforma} já cadastrado.")
                    return False

            conexao = conectar()

            if conexao:
                try:

                    cursor = conexao.cursor()

                    # habilita as chaves secundárias
                    cursor.execute("PRAGMA foreign_keys = ON;")
                    
                    cursor.execute(
                        "INSERT INTO jogos (titulo, genero, plataforma, status, horas_jogadas, avaliacao) VALUES (?, ?, ?, ?, ?, ?)",
                        (novo_jogo.titulo, novo_jogo.genero, novo_jogo.plataforma, novo_jogo.status, novo_jogo.horas_jogadas, novo_jogo.avaliacao)
                    )

                    # retorna o id do jogo que foi inserido para usar como id da subclasse
                    jogo_id = cursor.lastrowid

                    # checa para qual tabela de subclasse os dados serão enviado e relacionados
                    if isinstance(novo_jogo, JogoCampanha):

                        cursor.execute(
                            "INSERT INTO jogos_campanha (id, progresso, percent_conclusao) VALUES (?, ?, ?)",
                            (jogo_id, novo_jogo.progresso, novo_jogo.percent_conclusao)
                        )
                        
                    elif isinstance(novo_jogo, JogoCompetitivo):

                        cursor.execute(
                            "INSERT INTO jogos_competitivos (id, partidas, vit, der, rank, taxa_vit) VALUES (?, ?, ?, ?, ?, ?)",
                            (jogo_id, novo_jogo.partidas, novo_jogo.vit, novo_jogo.der, novo_jogo.rank, novo_jogo.taxa_vit)
                        )
                        
                    elif isinstance(novo_jogo, JogoCooperativo):

                        # cria str apartir da lista do atributo participantes_frequentes
                        copia_participantes = ", ".join(novo_jogo.participantes_frequentes)

                        cursor.execute(
                            "INSERT INTO jogos_cooperativos (id, max_jogadores, sessoes_coop, participantes_frequentes) VALUES (?, ?, ?, ?)",
                            (jogo_id, novo_jogo.max_jogadores, novo_jogo.sessoes_coop, copia_participantes)
                        )

                    conexao.commit()
                    print(f"Jogo {novo_jogo.titulo} cadastrado com sucesso")
                    return True
                    
                except Error as e:
                    print(f"Erro ao cadastrar jogo: {e}")
                    conexao.rollback()
                    return False
                finally:
                    conexao.close()
        else:
            raise TypeError("Tipo de jogo inválido")

    def removerJogo(self, nome_jogo):
        if isinstance(nome_jogo, str):
            conexao = conectar()
            if conexao:
                try:
                    cursor = conexao.cursor()
                    cursor.execute("PRAGMA foreign_keys = ON;")

                    cursor.execute("DELETE FROM jogos WHERE titulo = ?", (nome_jogo,))
                    conexao.commit()

                    if cursor.rowcount > 0:
                        print(f"Jogo {nome_jogo} foi removido")
                        return True
                    else:
                        print(f"Nenhum jogo encontrado com o titulo {nome_jogo}.")
                        return False

                except Error as e:
                    conexao.rollback()
                    print(f"Erro ao remover coleção: {e}")
                    return False
                finally:
                    conexao.close()
        else:
            raise TypeError("Tipo de nome de jogo inválido")
                    
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
                return None
            finally:
                conexao.close()

    def atualizarJogo(self, novo_jogo: Jogo, titulo_antigo: str):

        if isinstance(novo_jogo, Jogo):
            antigo_jogo = self.buscarJogo(titulo_antigo)

            if not antigo_jogo:
                print("Jogo não encontrado")
                return False
            
            conexao = conectar()
            if conexao:
                try:

                    cursor = conexao.cursor()

                    cursor.execute("PRAGMA foreign_keys = ON;")  # habilita as classes estrangeiras

                    # checa se já existem 3 jogos com o status JOGANDO caso atualize o status
                    if novo_jogo.status == "JOGANDO" and antigo_jogo.status != "JOGANDO":
                        cursor.execute("""
                            SELECT COUNT(*) 
                            FROM jogos 
                            WHERE status = ?
                        """, ("JOGANDO",))

                        total_jogando = cursor.fetchone()[0]

                        if total_jogando == 3:
                            print("Mais de 3 jogos com o status jogando. Falha em atualizar status")
                            return False
                    
                     
                    cursor.execute("""
                            UPDATE jogos
                            SET titulo = ?, genero = ?, plataforma = ?, status = ?, horas_jogadas = ?, avaliacao = ?
                            WHERE titulo = ?
                    """, (novo_jogo.titulo, novo_jogo.genero, novo_jogo.plataforma, novo_jogo.status, novo_jogo.horas_jogadas, novo_jogo.avaliacao, antigo_jogo.titulo))

                    jogo_id = cursor.lastrowid


                    if isinstance(novo_jogo, JogoCampanha):
                        cursor.execute("""
                                UPDATE jogos_campanha
                                SET progresso = ?, percent_conclusao = ?
                                WHERE id = ?
                        """, (novo_jogo.progresso, novo_jogo.percent_conclusao, jogo_id))
                    elif isinstance(novo_jogo, JogoCompetitivo):
                        cursor.execute("""
                                UPDATE jogos_competitivos
                                SET partidas = ?, vit = ?, der = ?, rank = ?, taxa_vit = ?
                                WHERE id = ?
                        """, (novo_jogo.partidas, novo_jogo.vit, novo_jogo.der, novo_jogo.rank, novo_jogo.taxa_vit, jogo_id))
                    elif isinstance(novo_jogo, JogoCooperativo):
                        if len(novo_jogo.participantes_frequentes) > 0:
                            part_str = ", ".join(novo_jogo.participantes_frequentes)
                        else:
                            part_str = None

                        cursor.execute("""
                                UPDATE jogos_cooperativos
                                SET max_jogadores = ?, sessoes_coop = ?, participantes_frequentes = ?
                                WHERE id = ?
                        """, (novo_jogo.max_jogadores, novo_jogo.sessoes_coop, part_str, jogo_id))
                    
                    
                    conexao.commit()
                    
                    return True

                except Error as e:
                    conexao.rollback()
                    print(f"Erro ao atualizar jogo: {e}")
                    return False
                finally:
                    conexao.close()
        else:
            raise TypeError("Tipo de jogo inválido")

    # Listas e ordenações
    def listarJogos(self, genero =None, status=None, plataforma=None, nota_min=None):
        conexao = conectar()

        if conexao:
            try:

                cursor = conexao.cursor()

                # Query base unindo a tabela principal e as subclasses
                query = """
                    SELECT 
                        j.titulo, j.genero, j.plataforma, j.status, j.horas_jogadas, j.avaliacao,
                        jc.progresso, jc.percent_conclusao,
                        jcomp.partidas, jcomp.vit, jcomp.vit, jcomp.der, jcomp.rank, jcomp.taxa_vit,
                        jcoop.max_jogadores, jcoop.sessoes_coop, jcoop.participantes_frequentes
                    FROM jogos j
                    LEFT JOIN jogos_campanha jc ON j.id = jc.id
                    LEFT JOIN jogos_competitivos jcomp ON j.id = jcomp.id
                    LEFT JOIN jogos_cooperativos jcoop ON j.id = jcoop.id
                    WHERE 1=1
                """
                
                # Lista para armazenar os parâmetros de segurança do SQL
                parametros = []

                # Adiciona filtros dinamicamente se eles foram informados
                if genero:
                    query += " AND j.genero LIKE ?"
                    parametros.append(f"%{genero}%")

                if plataforma:
                    query += " AND j.plataforma LIKE ?"
                    parametros.append(f"%{plataforma}%")

                if status is not None:
                    query += " AND j.status = ?"
                    parametros.append(status)

                if nota_min:
                    query += " AND j.avaliacao >= ?"
                    parametros.append(f"%{nota_min}%")

                cursor.execute(query, parametros)
                resultados = cursor.fetchall()
                conexao.close()

                jogos_instanciados = []

                # Instancia os objetos corretos para cada linha retornada
                for linha in resultados:
                    ( titulo, genero, plataforma, status, horas_jogadas, avaliacao, progresso, percent_conclusao, partidas, vit, vit, der, rank, taxa_vit, max_jogadores, sessoes_coop, participantes_frequentes
                    ) = linha

                    # Identifica a subclasse e instancia o objeto
                    if progresso is not None:
                        obj = JogoCampanha(
                            titulo=titulo,
                            genero=genero,
                            plataforma=plataforma,
                            status=status,
                            horas_jogadas=horas_jogadas,
                            avaliacao=avaliacao,
                            progresso=progresso,
                            percent_conclusao=percent_conclusao
                            )
                    elif partidas is not None:
                        obj = JogoCompetitivo(
                            titulo=titulo,
                            genero=genero,
                            plataforma=plataforma,
                            status=status,
                            horas_jogadas=horas_jogadas,
                            avaliacao=avaliacao,
                            partidas=partidas,
                            vit=vit,
                            der=der,
                            rank=rank,
                            taxa_vit=taxa_vit
                            )
                    elif max_jogadores is not None:
                        obj = JogoCooperativo(
                            titulo=titulo,
                            genero=genero,
                            plataforma=plataforma,
                            status=status,
                            horas_jogadas=horas_jogadas,
                            avaliacao=avaliacao,
                            max_jogadores=max_jogadores,
                            sessoes_coop=sessoes_coop,
                            participantes_frequentes=participantes_frequentes
                        )

                    jogos_instanciados.append(obj)

                if len(jogos_instanciados) == 0:
                    return None
                return jogos_instanciados

            except Error as e:
                print(f"Erro ao listar jogos: {e}")
            finally:
                conexao.close()

    # Retorna número de jogos cadastrados e total de horas jogadas
    def relatorioSimples(self):

        conexao = conectar()

        if conexao:
            try:
                cursor = conexao.cursor()

                # retorna o número total de jogos
                cursor.execute("SELECT COUNT(*) FROM jogos;")
                total_jogos = cursor.fetchone()[0]
                resultado_jogos = total_jogos if total_jogos is not None else 0   # caso não haja jogos no banco e esse valor seja NULL(ou None), ele retorna 0 e não apenas None

                #retorna as horas jogadas
                cursor.execute("SELECT SUM(horas_jogadas) FROM jogos;")
                horas_totais = cursor.fetchone()[0]
                resultado_horas = horas_totais if horas_totais is not None else 0.0   # caso não haja jogos no banco e esse valor seja NULL(ou None), ele retorna 0.0 e não apenas None

                return resultado_jogos, resultado_horas

            except Error as e:
                print(f"Erro ao retornar relatório simples: {e}")
                conexao.rollback()
                return False
            finally:
                conexao.close()


if __name__ == "__main__":
    db = dados()
    jogo = db.buscarJogo("Ori")
    col = db.buscarColecao("Favoritos")

    if jogo and col:


        db.adicionarJogoColecao(jogo,col)

        db.atualizarColecao(col, col.nome_colecao)

        print(jogo)
        print(col)

    