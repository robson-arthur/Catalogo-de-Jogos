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

        if dados_existe:
            print(f"Banco da dados '{nome_banco}' já criado, conexão realizada")
        else:
            print(f"Arquivo '{nome_banco}' criado, conexão realizada")

        return conexao

    except Error:
        print(f"Não foi possível conectar ou criar o banco de dados: {Error}")

    return conexao   ##retorna o estado da conexão, apenas se ela for concluida retornará True
