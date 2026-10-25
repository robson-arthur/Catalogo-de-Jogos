# classes usadas no projeto
from src.database.dados import dados
from src.classes.Jogo import Jogo
from src.classes.JogoCooperativo import JogoCooperativo
from src.classes.JogoCampanha import JogoCampanha
from src.classes.JogoCompetitivo import JogoCompetitivo
from src.classes.Colecao import Colecao
from src.database.dados import dados as dadosdb

# biblioteca para criar a interface CLI de execução
import argparse


## funções que implementam os argumentos nos métodos do projeto
def cmd_cadastrar_campanha(args):
    dados = {
        "titulo": args.titulo,
        "genero": args.genero,
        "plataforma": args.plataforma,
        "horas_jogadas": args.horas_jogadas,
        "progresso": args.progresso,
        "percent_conclusao": args.percent_conclusao
    }

    jogo = JogoCampanha(
        titulo=dados["titulo"], 
        genero=dados["genero"], 
        plataforma=dados["plataforma"],
        horas_jogadas=dados["horas_jogadas"],
        progresso=dados["progresso"],
        percent_conclusao=dados["percent_conclusao"]
        )

    print(jogo)
    print(f"Jogo '{args.titulo}' cadastrado com sucesso.")

def cmd_cadastrar_competitivo(args):
    dados = {
        "titulo": args.titulo,
        "genero": args.genero,
        "plataforma": args.plataforma,
        "horas_jogadas": args.horas_jogadas,
        "rank": args.rank
    }
    
    jogo = JogoCompetitivo(
        titulo=dados["titulo"], 
        genero=dados["genero"], 
        plataforma=dados["plataforma"],
        horas_jogadas=dados["horas_jogadas"],
        rank=dados["rank"]
        )

    print(jogo)
    print(f"Jogo '{args.titulo}' cadastrado com sucesso.")

def cmd_cadastrar_cooperativo(args):


    dados = {
        "titulo": args.titulo,
        "genero": args.genero,
        "plataforma": args.plataforma,
        "horas_jogadas": args.horas_jogadas,
        "max_jogadores": args.max_jogadores,
        "participantes_frequentes": args.participantes_frequentes
    }
    
    jogo = JogoCooperativo(
        titulo=dados["titulo"], 
        genero=dados["genero"], 
        plataforma=dados["plataforma"],
        horas_jogadas=dados["horas_jogadas"],
        max_jogadores=dados["max_jogadores"],
        participantes_frequentes=dados["participantes_frequentes"]
        )

    print(jogo)
    print(f"Jogo '{args.titulo}' cadastrado com sucesso.")

def cmd_listar_jogos(args):
    dados = {
        "genero": args.genero,
        "plataforma": args.plataforma,
        "status": args.status,
        "nota_min": args.nota_min
    }

    db = dadosdb()

    jogos = db.listarJogos(genero=dados["genero"], plataforma=dados["plataforma"], status=dados["status"], nota_min=dados["nota_min"])

    if jogos == None:
        print("Nenhum jogo encontrado")
    else:
        for jogo in jogos:
            print()
            print(f"{"Jogos":=^100}")
            print(repr(jogo))
            print("-"*100)
        print()

## cria o parser e adiciona os argumentos e subparsers
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

    listar = acoes_jogo.add_parser(
        "listar",
        help = "Lista todos os jogos já cadastrados"
    )

    # Jogo de campanha
    campanha = tipos.add_parser("campanha")
    campanha.add_argument("-t", "--titulo", required=True)
    campanha.add_argument("-g", "--genero", required=True)
    campanha.add_argument("-p", "--plataforma", required=True)
    campanha.add_argument("-hj", "--horas_jogadas", default=0.0, type=float)
    campanha.add_argument("--progresso", default=0, type=int)
    campanha.add_argument("--percent_conclusao", default=0.0, type=float)
    campanha.set_defaults(func=cmd_cadastrar_campanha)

    # Jogo competitivo
    competitivo = tipos.add_parser("competitivo")
    competitivo.add_argument("-t", "--titulo", required=True)
    competitivo.add_argument("-g", "--genero", required=True)
    competitivo.add_argument("-p", "--plataforma", required=True)
    competitivo.add_argument("-hj", "--horas_jogadas", default=0.0, type=float)
    competitivo.add_argument("--rank", default="SEM RANK")
    competitivo.set_defaults(func=cmd_cadastrar_competitivo)

    # Jogo cooperativo
    cooperativo = tipos.add_parser("cooperativo")
    cooperativo.add_argument("-t", "--titulo", required=True)
    cooperativo.add_argument("-g", "--genero", required=True)
    cooperativo.add_argument("-p", "--plataforma", required=True)
    cooperativo.add_argument("-hj", "--horas_jogadas", default=0.0, type=float)
    cooperativo.add_argument("--max_jogadores", default=0, type=int)
    cooperativo.add_argument("--participantes_frequentes", nargs="*", default=[], help="Nome dos participantes frequentes")
    cooperativo.set_defaults(func=cmd_cadastrar_cooperativo)

    # Listar por Genero, plataforma, status, nota minima ou nenhum
    listar.add_argument("--genero", default=None)
    listar.add_argument("--plataforma", default=None)
    listar.add_argument("--status", default=None, choices=["NÃO INICIADO", "JOGANDO", "FINALIZADO"])
    listar.add_argument("--nota_min", default=None, choices=range(0,11), type=int)
    listar.set_defaults(func=cmd_listar_jogos)

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