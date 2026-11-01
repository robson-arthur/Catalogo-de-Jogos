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

# função para confimar operações
def confirmar():

    while True:
        resp = input("Confirma? (S/N): ").upper()

        if resp == "S":
            break
        elif resp == "N":
            break
        print("Opção inválida")

    return resp

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

    if not jogos:
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

    jogo = db.buscarJogo(nome_jogo)

    if jogo:
        print(repr(jogo))
        resp = confirmar()

        if resp == "S":
            db.removerJogo(nome_jogo)
        else:
            print("Operação cancelada")
    
def cmd_status(args):
    nome_jogo = args.nome_jogo
    novo_status = args.status

    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if jogo:
        if jogo.status == novo_status:
            return print("Erro na alteração, status igual ao anterior")

        jogo.status = novo_status

        resultado = db.atualizarJogo(jogo, jogo.titulo)
        if resultado:
            print("Status atualizado")

def cmd_horas(args):
    nome_jogo = args.nome_jogo
    horas = args.horas

    if horas <= 0:
        raise argparse.ArgumentTypeError("As horas jogadas não podem ser negativas ou iguais a zero")
    
    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if jogo:

        resp = confirmar()

        if resp == "S":
            jogo.registrarHoras(horas)

            resultado = db.atualizarJogo(jogo, jogo.titulo)
            if resultado:
                print("Horas registradas")
        else:
            print("Operação cancelada")

def cmd_reiniciar(args):
    nome_jogo = args.nome_jogo

    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if jogo:

        resp = confirmar()

        if resp == "S":

            jogo.reiniciarJogo()

            resultado = db.atualizarJogo(jogo, jogo.titulo)
            if resultado:
                print("Jogo reiniciado")
        else:
            print("Operação cancelada")

def cmd_avaliacao(args):
    nome_jogo = args.nome_jogo
    nova_avaliacao = args.avaliacao

    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if jogo:
        if jogo.status == "FINALIZADO":
            jogo.avaliacao = nova_avaliacao
            resultado = db.atualizarJogo(jogo, jogo.titulo)
            if resultado:
                print("Avaliação atualizada")
        else:
            print("Erro, jogo não finalizado")

#jogos_campanha
def cmd_progresso(args):
    nome_jogo = args.nome_jogo
    progresso = args.progresso

    if progresso <= 0:
        raise argparse.ArgumentTypeError("O progresso não pode ser negativo ou igual a zero")
    
    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if not isinstance(jogo, JogoCampanha):
        print(repr(jogo))
        return print("Jogo encontrado não é do tipo campanha")

    if jogo:
        print(repr(jogo))
        resp = confirmar()

        if resp == "S":
            jogo.atualizarProgresso(progresso)

            resultado = db.atualizarJogo(jogo, jogo.titulo)
            if resultado:
                print("Progresso registrado")
        else:
            print("Operação cancelada")

def cmd_conclusao(args):
    nome_jogo = args.nome_jogo
    percentual = args.conclusao

    if percentual < 0 or percentual > 100:
        raise argparse.ArgumentTypeError(f"O percentual deve estar entre 0% e 100%")
    
    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if not isinstance(jogo, JogoCampanha):
        print(repr(jogo))
        return print("Jogo encontrado não é do tipo campanha")

    if jogo:

        jogo.atualizarPercentual(percentual)

        resultado = db.atualizarJogo(jogo, jogo.titulo)
        if resultado:
            print("Percentual registrado")

#jogos_competitivos
# def cmd_vit(args):

# def cmd_der(args):

# def cmd_rank(args):

# def cmd_taxa_vit(args):

#jogos_cooperativos
# def cmd_sessoes_coop(args):

# def cmd_adicionar_participantes(args):
#colecoes
def cmd_cadastrar_colecao(args):
    nome_colecao = args.nome

    db = dadosdb()

    colecao_bd = db.buscarColecao(nome_colecao)

    if colecao_bd == nome_colecao:
        return print("Coleção já existe com esse nome")

    colecao = Colecao(nome_colecao=nome_colecao)

    print(repr(colecao))

    db.adicionarColecao(colecao)

def cmd_remover_colecao(args):
    nome_colecao = args.nome_colecao

    db = dadosdb()
    db.removerColecao(nome_colecao)

def cmd_adicionarJogo_colecao(args):
    nome_colecao = args.nome_colecao
    nome_jogo = args.nome_jogo

    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if not jogo:
        return print("Jogo não encontrado")

    col = db.buscarColecao(nome_colecao)

    if not col:
        return print("Colecao não encontrada")

    
    
    resultado = db.adicionarJogoColecao(jogo,col) #caso o jogo já exista na coleção, retorna o erro e não executa

    # caso a relação tenha sido cadastrada, a coleção é também atualizada
    if resultado:
        col.adicionarJogo(jogo)
        db.atualizarColecao(col, col.nome_colecao)

def cmd_removerJogo_colecao(args):
    nome_colecao = args.nome_colecao
    nome_jogo = args.nome_jogo

    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if not jogo:
        return print("Jogo não encontrado")

    col = db.buscarColecao(nome_colecao)

    if not col:
        return print("Colecao não encontrada")

    
    resultado = db.removerJogoColecao(jogo,col) #caso o jogo não exista na coleção, retorna o erro e não executa

    # caso a relação tenha sido cadastrada, a coleção é também atualizada
    if resultado:
        col.removerJogo(jogo)
        db.atualizarColecao(col, col.nome_colecao)

def cmd_listarJogos_colecao(args):
    dados = {
            "nome_colecao": args.nome_colecao,
        }
    
    db = dadosdb()

    col = db.buscarColecao(dados["nome_colecao"])

    if not col:
        return print(f"Colecão {dados['nome_colecao']} não encontrada")


    jogos = db.listarJogos_colecao(col)

    if not jogos:
        return print(f"Nenhum jogo da coleção {dados['nome_colecao']} encontrado")
    
    for jogo in jogos:
        print()
        print(f"{"Jogos":=^100}")
        print(repr(jogo))
        print("-"*100)
    print()    

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

    atualizar = acoes_jogo.add_parser(
        "atualizar",
        help="Atualiza dados dos jogos"
    )
    dados = atualizar.add_subparsers(
        dest="dados",
        required=True
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

    status = dados.add_parser(
        "status",
        help="Adiciona um novo status a um jogo"
    )
    horas = dados.add_parser(
        "horas_jogadas",
        help="Registra horas jogadas"
    )
    avaliacao = dados.add_parser(
        "avaliacao",
        help="Atualiza a avaliacao de um jogo já finalizado"
    )
    reiniciar = dados.add_parser(
        "reiniciar",
        help="Reseta todas as informações de um jogo(exceto nome, plataforma, genêro e max_jogadores se aplicável)"
    )

    # subcomandos para tipo campanha
    progresso = dados.add_parser(
        "progresso",
        help="Registra novo progresso"
    )
    conclusao = dados.add_parser(
        "conclusao",
        help="Registra um novo percentual de conclusão"
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

    #status
    status.add_argument("--nome_jogo", required=True)
    status.add_argument("--status", required=True, choices=["NÃO INICIADO", "JOGANDO", "FINALIZADO"])
    status.set_defaults(func=cmd_status)

    #horas_jogadas
    horas.add_argument("--nome_jogo", required=True)
    horas.add_argument("--horas", type=float, required=True)
    horas.set_defaults(func=cmd_horas)

    #reiniciar
    reiniciar.add_argument("--nome_jogo", required=True)
    reiniciar.set_defaults(func=cmd_reiniciar)

    #avaliacao
    avaliacao.add_argument("--nome_jogo", required=True)
    avaliacao.add_argument("--avaliacao", required=True, choices=range(0,11), type=int)
    avaliacao.set_defaults(func=cmd_avaliacao)

    #progresso
    progresso.add_argument("--nome_jogo", required=True)
    progresso.add_argument("--progresso", required=True, type=int)
    progresso.set_defaults(func=cmd_progresso)

    #percentual_conclusao
    conclusao.add_argument("--nome_jogo", required=True)
    conclusao.add_argument("--conclusao", required=True, type=float)
    conclusao.set_defaults(func=cmd_conclusao)

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

    listarJogos_colecao = acoes_colecao.add_parser(
        "listarJogos",
        help="Lista jogos de uma determinada coleção"
    )

    adicionarJogo_colecao = acoes_colecao.add_parser(
        "adicionarJogo",
        help="Adiciona um jogo a uma coleção atráves dos nomes"
    )

    removerJogo_colecao = acoes_colecao.add_parser(
        "removerJogo",
        help="Remove um jogo de uma coleção atráves dos nomes"
    )

    ## cadastrar colecao
    cadastrar_colecao.add_argument("--nome", required=True)
    cadastrar_colecao.set_defaults(func=cmd_cadastrar_colecao)

    # remover colecao
    remover_colecao.add_argument("--nome_colecao", required=True)
    remover_colecao.set_defaults(func=cmd_remover_colecao)

    #listar jogos de uma coleção
    listarJogos_colecao.add_argument("--nome_colecao", required=True)
    listarJogos_colecao.set_defaults(func=cmd_listarJogos_colecao)

    #adicionarJogo_colecao
    adicionarJogo_colecao.add_argument("--nome_colecao", required=True)
    adicionarJogo_colecao.add_argument("--nome_jogo", required=True)
    adicionarJogo_colecao.set_defaults(func=cmd_adicionarJogo_colecao)

    #removerJogo_colecao
    removerJogo_colecao.add_argument("--nome_colecao", required=True)
    removerJogo_colecao.add_argument("--nome_jogo", required=True)
    removerJogo_colecao.set_defaults(func=cmd_removerJogo_colecao)

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