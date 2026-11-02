# importação relativa para evitar erros de importação em diferentes sos
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)

# classes usadas no projeto
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

#relatório
def cmd_relatorio(args):
    tipo = args.tipo

    db = dadosdb()

    if tipo == "simples":
        resultado = db.relatorioSimples()
        if resultado:
            print(f"Total de horas jogadas: {resultado[1]}")
            print(f"Total de jogos cadastrados: {resultado[0]}")
    elif tipo == "media_avaliacao":
        resultado = db.media_avaliacao()
        if resultado:
            print(f"Média de avaliação dos jogos: {resultado:.2f}")
    elif tipo == "percentual":
        resultado = db.percentual_status()
        if resultado:
            print("Percentual por status:")
            print(f"FINALIZADOS: {resultado["FINALIZADOS"]}")
            print(f"JOGANDO: {resultado["JOGANDO"]}")
            print(f"NÃO INCIADOS: {resultado["NÃO INCIADOS"]}")
    elif tipo == "top5":
        resultado = db.top5()
        if resultado:
            print()
            print(f"{"Jogos":^150}")
            for jogo in resultado:
                print(repr(jogo))
                print("-"*150)
            print()


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
    }
    
    jogo = JogoCooperativo(
        titulo=dados["titulo"], 
        genero=dados["genero"], 
        plataforma=dados["plataforma"],
        horas_jogadas=dados["horas_jogadas"],
        max_jogadores=dados["max_jogadores"]
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
        print()
        print(f"{"Jogos":^150}")
        for jogo in jogos:
            print(repr(jogo))
            print("-"*150)
        print()

def cmd_ordenar_jogos(args):
    tipo = args.tipo
    ordem = args.ordem

    db = dadosdb()

    jogos = db.ordenarJogos(tipo, ordem)

    if not jogos:
        print("Nenhum jogo encontrado")
    else:
        print()
        print(f"{"Jogos":^150}")
        for jogo in jogos:
            print(repr(jogo))
            print("-"*150)
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
def cmd_vit(args):
    nome_jogo = args.nome_jogo
    vit = args.vit

    if vit <= 0:
        raise argparse.ArgumentTypeError("A quantidade de vitórias não pode ser negativa ou igual a zero")
    
    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if not isinstance(jogo, JogoCompetitivo):
        print(repr(jogo))
        return print("Jogo encontrado não é do tipo competitivo")

    if jogo:
        print(repr(jogo))
        resp = confirmar()

        if resp == "S":
            jogo.registrarVit(vit)

            resultado = db.atualizarJogo(jogo, jogo.titulo)
            if resultado:
                print("Vitórias registradas")
        else:
            print("Operação cancelada")

def cmd_der(args):
    nome_jogo = args.nome_jogo
    der = args.der

    if der <= 0:
        raise argparse.ArgumentTypeError("A quantidade de derrotas não pode ser negativa ou igual a zero")
    
    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if not isinstance(jogo, JogoCompetitivo):
        print(repr(jogo))
        return print("Jogo encontrado não é do tipo competitivo")

    if jogo:
        print(repr(jogo))
        resp = confirmar()

        if resp == "S":
            jogo.registrarDer(der)

            resultado = db.atualizarJogo(jogo, jogo.titulo)
            if resultado:
                print("Derrotas registradas")
        else:
            print("Operação cancelada")

def cmd_rank(args):
    nome_jogo = args.nome_jogo
    rank = args.rank

    
    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if not isinstance(jogo, JogoCompetitivo):
        print(repr(jogo))
        return print("Jogo encontrado não é do tipo competitivo")

    if jogo:
        print(repr(jogo))
        resp = confirmar()

        if resp == "S":
            jogo.rank = rank

            resultado = db.atualizarJogo(jogo, jogo.titulo)
            if resultado:
                print("Rank registrado")
        else:
            print("Operação cancelada")

#jogos_cooperativos
def cmd_sessoes_coop(args):
    nome_jogo = args.nome_jogo
    sessoes = args.sessoes

    if sessoes <= 0:
        raise argparse.ArgumentTypeError("A quantidade de sessões não pode ser negativa ou igual a zero")
    
    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if not isinstance(jogo, JogoCooperativo):
        print(repr(jogo))
        return print("Jogo encontrado não é do tipo cooperativo")

    if jogo:
        print(repr(jogo))
        resp = confirmar()

        if resp == "S":
            jogo.registrarSessoes(sessoes)

            resultado = db.atualizarJogo(jogo, jogo.titulo)
            if resultado:
                print("Sessões registradas")
        else:
            print("Operação cancelada")

def cmd_atualizar_participantes(args):
    nome_jogo = args.nome_jogo
    participantes = args.participantes
  
    db = dadosdb()

    jogo = db.buscarJogo(nome_jogo)

    if not isinstance(jogo, JogoCooperativo):
        print(repr(jogo))
        return print("Jogo encontrado não é do tipo cooperativo")

    if jogo:
        print(repr(jogo))
        resp = confirmar()

        if resp == "S":

            for part in participantes:
                # caso um nome seja repetido, o participante é removido
                if part in jogo.participantes_frequentes:
                    jogo.removerParticipante(part)
                else:
                    jogo.adicionarParticipante(part)

            resultado = db.atualizarJogo(jogo, jogo.titulo)
            if resultado:
                print("Participantes registrados")
        else:
            print("Operação cancelada")

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

    ordenar_jogos = acoes_jogo.add_parser(
        "ordenar",
        help="Lista os jogos de acordo com a ordem escolhida"
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
    # subcomandos para tipo competitivo
    vit = dados.add_parser(
        "vit",
        help="Registrar vitórias"
    )
    der = dados.add_parser(
        "der",
        help="Registrar derrotas"
    )
    rank = dados.add_parser(
        "rank",
        help="Registrar novo rank"
    )

    # subcomandos para tipo cooperativo
    sessoes = dados.add_parser(
        "sessoes",
        help="Registra sessões cooperativas"
    )
    part_frequentes = dados.add_parser(
        "part_frequentes",
        help="Registra um ou mais participantes frequentes"
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
    cooperativo.set_defaults(func=cmd_cadastrar_cooperativo)

    # Listar jogos por genero, plataforma, status, nota minima ou nenhum
    listar_jogos.add_argument("--genero", default=None)
    listar_jogos.add_argument("--plataforma", default=None)
    listar_jogos.add_argument("--status", default=None, choices=["NÃO INICIADO", "JOGANDO", "FINALIZADO"])
    listar_jogos.add_argument("--nota_min", default=None, choices=range(0,11), type=int)
    listar_jogos.set_defaults(func=cmd_listar_jogos)

    # ordenar jogos por titulo, horas_jogadas, avaliacao ou status
    ordenar_jogos.add_argument("--tipo", choices=["titulo", "horas_jogadas", "avaliacao", "status"], default="titulo")
    ordenar_jogos.add_argument("--ordem", choices=["ASC", "DESC"], default="ASC")
    ordenar_jogos.set_defaults(func=cmd_ordenar_jogos)

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

    #vit
    vit.add_argument("--nome_jogo", required=True)
    vit.add_argument("--vit", required=True, type=int)
    vit.set_defaults(func=cmd_vit)

    #der
    der.add_argument("--nome_jogo", required=True)
    der.add_argument("--der", required=True, type=int)
    der.set_defaults(func=cmd_der)

    #rank
    rank.add_argument("--nome_jogo", required=True)
    rank.add_argument("--rank", required=True)
    rank.set_defaults(func=cmd_rank)

    #sessoes
    sessoes.add_argument("--nome_jogo", required=True)
    sessoes.add_argument("--sessoes", required=True, type=int)
    sessoes.set_defaults(func=cmd_sessoes_coop)

    #part_frequentes
    part_frequentes.add_argument("--nome_jogo", required=True)
    part_frequentes.add_argument("--participantes", required=True, nargs="+", help="Insira os nomes separados por um espaço simples, apenas um nome por participante, insira o nome de um participante que já existe para remover dos dados")
    part_frequentes.set_defaults(func=cmd_atualizar_participantes)

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

    # ------------------
    #  relatorios
    # ------------------
    relatorio = comandos.add_parser(
        "relatorio",
        help="Exibir relatórios dos jogos cadastrados"
    )

    relatorio.add_argument("--tipo", choices=["simples", "media_avaliacao", "percentual", "top5"], required=True)
    relatorio.set_defaults(func=cmd_relatorio)

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