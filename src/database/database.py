import os ##serve para criar o arquivo dados.db caso não exista em uma pasta escolhida e exibir uma mensagem personalizada
import sqlite3 as s
from sqlite3 import Error  #permite analisar o erro caso aconteça na conexão

def conectar(nome_banco="dados.db", pasta="src/database"):
    """Conecta ao banco de dados se já existente, ou cria um novo banco de dados
    
    Atributos:
    
    nome_banco: str
    pasta: str
    """
    #inicializa a variável conexão com um valor nulo
    conexao = None
    try:
        #verifica se a pasta src/database/ existe, para não ocorrer erro
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"Pasta '{pasta}' criada com sucesso!")

        #cria o caminho que o banco deverá seguir, no caso a pasta src/database/
        destino_banco = os.path.join(pasta, nome_banco)

        # retorna true caso o arquivo já exista
        dados_existe = os.path.exists(destino_banco)

        # conecta com o banco, se ele n existe, o arquvio é criado automaticamente
        conexao = s.connect(destino_banco)

        # isso permite acessar os dados das colunas facilmente pelo nome, como "linha[nome_da_coluna]"
        conexao.row_factory = s.Row 

        if not dados_existe:
            print(f"Arquivo '{nome_banco}' criado, conexão realizada")

        ## criar tabelas
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
                    conexao.rollback()
        
        return conexao

    except Error:
        print(f"Não foi possível conectar ou criar o banco de dados: {Error}")

    return conexao   ##retorna o estado da conexão caso ocorra erro, no caso False

