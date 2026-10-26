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

#jogos
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

    print(repr(jogo))

    db = dadosdb()
    db.adicionarJogo(jogo)

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

    db = dadosdb()
    db.adicionarJogo(jogo)

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

    db = dadosdb()
    db.adicionarJogo(jogo)

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

def cmd_remover_jogo(args):
    nome_jogo = args.titulo

    db = dadosdb()

    db.removerJogo(nome_jogo)

#colecoes
def cmd_cadastrar_colecao(args):
    nome_colecao = args.nome

    colecao = Colecao(nome_colecao=nome_colecao)

    print(repr(colecao))

    db = dadosdb()
    db.adicionarColecao(colecao)

def cmd_remover_colecao(args):
    nome_colecao = args.nome_colecao

    db = dadosdb()
    db.removerColecao(nome_colecao)

def cmd_adicionarJogo_colecao(args):
    nome_colecao = args.nome_colecao
    nome_jogo = args.nome_jogo

    db = dadosdb()
    
    jogo =db.buscarJogo(nome_jogo)

    if not jogo:
        return print("Jogo não encontrado")

    col = db.buscarColecao(nome_colecao)

    if not col:
        return print("Colecao não encontrada")

    
    resultado = db.adicionarJogoColecao(jogo,col) #caso o jogo já exista na coleção, retorna o erro e não executa

    if resultado:
        db.atualizarColecao(col, col.nome_colecao)

        col.adicionarJogo(jogo)
    

## cria o parser e adiciona os argumentos e subparsers
def criar_parser():
    #parser principal
    parser = argparse.ArgumentParser(
        prog="Catálogo de Jogos ",
        description="Gerenciador de catálogo de jogos pessoal",
    )

    comandos = parser.add_subparsers(
        dest="entidade",
        required=True,
        title="entidades",
    )

    # --------------------------------
    #    subcomandos de jogo
    # --------------------------------
    jogo = comandos.add_parser(
        "jogo",
        help="CRUD de Jogos",
    )
    acoes_jogo = jogo.add_subparsers(
        dest="acao_jogo",
        required=True,
    )

    cadastrar_jogo = acoes_jogo.add_parser(
        "cadastrar",
        help="Cadastrar um jogo",
    )
    tipos = cadastrar_jogo.add_subparsers(
        dest="tipo",
        required=True
    )

    remover_jogo = acoes_jogo.add_parser(
        "remover",
        help="Remover jogo do banco de dados atráves do nome"
    )

    listar_jogos = acoes_jogo.add_parser(
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

    # Listar jogos por genero, plataforma, status, nota minima ou nenhum
    listar_jogos.add_argument("--genero", default=None)
    listar_jogos.add_argument("--plataforma", default=None)
    listar_jogos.add_argument("--status", default=None, choices=["NÃO INICIADO", "JOGANDO", "FINALIZADO"])
    listar_jogos.add_argument("--nota_min", default=None, choices=range(0,11), type=int)
    listar_jogos.set_defaults(func=cmd_listar_jogos)

    # remover jogo
    remover_jogo.add_argument("--titulo", required=True)
    remover_jogo.set_defaults(func=cmd_remover_jogo)


    # --------------------------------
    #     subcomandos de colecao
    # --------------------------------
    colecao = comandos.add_parser(
        "colecao",
        help="CRUD de coleções"
    )
    acoes_colecao = colecao.add_subparsers(
        dest="acao_colecao",
        required=True
    )

    cadastrar_colecao = acoes_colecao.add_parser(
        "cadastrar",
        help="Cadastra uma nova colecao"
    )

    remover_colecao = acoes_colecao.add_parser(
        "remover",
        help="Remove uma coleção apartir do nome"
    )

    adicionarJogo_colecao = acoes_colecao.add_parser(
        "adicionarJogo",
        help="Adiciona um jogo a uma coleção atráves dos nomes"
    )

    ## cadastrar colecao
    cadastrar_colecao.add_argument("--nome", required=True)
    cadastrar_colecao.set_defaults(func=cmd_cadastrar_colecao)

    # remover colecao
    remover_colecao.add_argument("--nome_colecao", required=True)
    remover_colecao.set_defaults(func=cmd_remover_colecao)

    #adicionarJogo_colecao
    adicionarJogo_colecao.add_argument("--nome_colecao", required=True)
    adicionarJogo_colecao.add_argument("--nome_jogo", required=True)
    adicionarJogo_colecao.set_defaults(func=cmd_adicionarJogo_colecao)

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