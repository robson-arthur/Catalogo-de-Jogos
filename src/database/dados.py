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

    #Tratar coleções
    def criarTabelaColecao(self):
        colecoes_existem = self.tabela_existe("colecoes")
        if not colecoes_existem:
            conexao = conectar()
            if conexao:
                try:
                    ##criando cursor para modificar tabelas
                    cursor = conexao.cursor()
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS colecoes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_colecao TEXT NOT NULL,
                        numero_jogos INTEGER,
                        jogos TEXT
                        );
                    """)
                    conexao.commit()
                    print("Tabela colecoes criada com sucesso.")
                except Exception:
                        print(f"Erro ao criar tabela: {Exception}")
                finally:
                        conexao.close()
        else:
            print("Tabela colecoes já criada.")
