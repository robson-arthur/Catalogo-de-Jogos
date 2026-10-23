# classes usadas no projeto
from src.database.dados import dados
from src.classes.Jogo import Jogo
from src.classes.JogoCooperativo import JogoCooperativo
from src.classes.JogoCampanha import JogoCampanha
from src.classes.JogoCompetitivo import JogoCompetitivo
from src.classes.Colecao import Colecao

# biblioteca para criar a interface CLI de execução
import argparse


## funções que implementam os argumentos nos métodos do projeto
def cmd_cadastrar_campanha(args):
    dados = {
        "titulo": args.titulo,
        "genero": args.genero,
        "plataforma": args.plataforma,
    }

    jogo = JogoCampanha(dados["titulo"], dados["genero"], dados["plataforma"])

    print(jogo)
    print(f"Jogo '{args.titulo}' cadastrado com sucesso.")


## cria o parser e adiciona os argumentos
def criar_parser():
    parser = argparse.ArgumentParser(
        prog="Catálogo de Jogos ",
        description="Gerenciador de catálogo de jogos pessoal",
    )

    comandos = parser.add_subparsers(
        dest="entidade",
        required=True,
        title="entidades",
    )

    
    jogo = comandos.add_parser(
        "jogo",
        help="CRUD de Jogos",
    )
    acoes_jogo = jogo.add_subparsers(
        dest="acao",
        required=True,
    )

    cadastrar = acoes_jogo.add_parser(
        "cadastrar",
        help="Cadastrar um jogo",
    )
    tipos = cadastrar.add_subparsers(
        dest="tipo",
        required=True
    )

    # Jogo de campanha
    campanha = tipos.add_parser("campanha")
    campanha.add_argument("-t", "--titulo", required=True)
    campanha.add_argument("-g", "--genero", required=True)
    campanha.add_argument("-p", "--plataforma", required=True)
    campanha.set_defaults(func=cmd_cadastrar_campanha)

    return parser


# executa o script
def main():
    parser = criar_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except ValueError as erro:
        parser.exit(1, f"Erro: {erro}\n")
    except Exception as erro:
        parser.exit(1, f"Falha na operação: {erro}\n")

if __name__ == '__main__':
    main()