## o os e sys servem para resolver erros de importação, sendo possível executar os métodos da classe de qualquer arquivo e diretório
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from src.classes import Colecao
from src.database.database import conectar
import sqlite3 as s
from sqlite3 import Error  #permite analisar o erro caso aconteça na conexão

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
                        horas_jogadas REAL
                        );
                """)
                conexao.commit()

                # tabela intermediária: colecoes_jogos serve para relação de muitos para muitos
                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS colecao_jogos (
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
                print("Sucesso")

            except Error:
                 print(f"Erro ao criar tabelas: {Error}")
            finally:
                conexao.close()
