from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from .Recommender import Recommender
from .MJira import MesaJira


# Create your views here.

# ...
# ...
# Area do projeto

def projetos(request):
    projects = MProject.objects.all()
    args = {'projects': projects}

    return render(request, 'core/listar_projetos.html', args)


def detalhar_projeto(request, projeto_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    args = {"projeto": projeto}
    try:
        alocacao = get_list_or_404(AlocacaoP, projeto=projeto)
        args["alocacao"] = alocacao
    except Exception:
        print("Deu erro pegando alocacao")

    mesa_jira = MesaJira()
    # mesa_jira.debugIssue(projeto)

    #
    # Pegar as squads
    squads = {}
    recomendacoes_squad = {}

    try:

        for squad in projeto.squad_set.all():
            squads[squad.nome] = mesa_jira.get_squad_data(projeto, squad)

            #
            # Pegar as recomendação das squads
            try:
                recomendador = Recommender()
                cards = squads[squad.nome]  # Pegas os cards da sprint atual

                alocacoes_squad = projeto.alocacaop_set.filter(squad__nome=squad.nome)  # pegas as alocacoes da squad
                devs_alocados_squad = []

                # Pegas os devs da squad
                for alocacao in alocacoes_squad:
                    devs_alocados_squad.append(alocacao.dev)
                recomendacoes_squad[squad.nome] = recomendador.recomendar_dev_para_JiraIssue(
                    cards,
                    devs_alocados_squad)


            except Exception:
                print("Deu erro pegando as recomendações da squad {}".format(squad.nome))

        args["squads"] = squads
        args["recomendacoes"] = recomendacoes_squad

    except Exception:
        print("Deu erro pegando os dados da squad")

    return render(request, "core/detalhe_projeto.html", args)


def cadastrar_projeto(request):
    if request.method == 'POST':
        try:
            nome = request.POST['nome']
            url = request.POST['url']
            status = True if request.POST['status'] == "on" else False
            experiencias = request.POST['experiencias']

            projeto = MProject(name=nome, url=url, status=status)
            projeto.save()

            # Vincula as liguagens
            linguagens = request.POST.getlist("linguagens")

            for ling in linguagens:
                linguagem = get_object_or_404(Linguagem, pk=ling)
                projeto.linguagens.add(linguagem)

            projeto.save()

            # Cadatra as experiências e linca ao dev
            experiencias = experiencias.lower().replace(".", "").replace("!", "").replace(";", ",")
            experiencias = experiencias.split(",")
            exps = []

            for exp in experiencias:
                exps.append(exp.strip())
            for exp in exps:
                Ex, created = Experiencia.objects.get_or_create(exp=exp)
                Ex.projeto.add(projeto)

            return redirect('core:detalhe_projeto', projeto_id=projeto.id)
        except (KeyError):
            linguagens = Linguagem.objects.all()
            args = {"linguagens": linguagens}
            return render(request, 'core/cadastrar_projeto.html', args)
    else:
        linguagens = Linguagem.objects.all()
        args = {"linguagens": linguagens}
        return render(request, 'core/cadastrar_projeto.html', args)


def editar_projeto(request, projeto_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    if request.method == 'POST':
        try:
            nome = request.POST['nome']
            url = request.POST['url']
            status = True if request.POST['status'] == "on" else False
            experiencias = request.POST['experiencias']

            projeto.name = nome
            projeto.url = url
            projeto.status = status
            projeto.save()

            # Vincula as liguagens
            linguagens = request.POST.getlist("linguagens")

            for ling in linguagens:
                linguagem = get_object_or_404(Linguagem, pk=ling)
                projeto.linguagens.add(linguagem)

            projeto.save()

            # Cadatra as experiências e linca ao dev
            experiencias = experiencias.lower().replace(".", "").replace("!", "").replace(";", ",")
            experiencias = experiencias.split(",")
            exps = []

            for exp in experiencias:
                exps.append(exp.strip())
            for exp in exps:
                Ex, created = Experiencia.objects.get_or_create(exp=exp)
                Ex.projeto.add(projeto)

            return redirect('core:detalhe_projeto', projeto_id=projeto.id)
        except (KeyError):
            linguagens = Linguagem.objects.all()
            args = {"linguagens": linguagens, "projeto": projeto}
            return render(request, 'core/editar_projeto.html', args)
    else:
        linguagens = Linguagem.objects.all()
        args = {"linguagens": linguagens, "projeto": projeto}
        return render(request, 'core/editar_projeto.html', args)


# ...
# ...
# Area do desenvolvedor

def desenvolvedores(request):
    desenvolvedores = MDev.objects.all()
    args = {"desenvolvedores": desenvolvedores}
    return render(request, 'core/listar_desenvolvedores.html', args)


def detalhar_desenvolverdor(request, desenvolvedor_id):
    dev = get_object_or_404(MDev, pk=desenvolvedor_id)
    args = {"dev": dev}
    return render(request, "core/detalhe_desenvolvedor.html", args)


def cadastrar_desenvolverdor(request):
    if request.method == "POST":
        try:
            # Cadastrar o dev
            nome = request.POST['nome']
            email = request.POST['email']
            id_jira = request.POST['id_jira']
            experiencias = request.POST['experiencias']
            desenvolvedor = MDev(name=nome, email=email, id_jira=id_jira)
            desenvolvedor.save()

            # Vincula as liguagens
            linguagens = request.POST.getlist("linguagens")

            for ling in linguagens:
                linguagem = get_object_or_404(Linguagem, pk=ling)
                desenvolvedor.linguagens.add(linguagem)

            desenvolvedor.save()

            # Cadatra as experiências e linca ao dev
            experiencias = experiencias.lower()
            experiencias = experiencias.split(",")
            exps = []

            for exp in experiencias:
                exps.append(exp.strip())
            for exp in exps:
                Ex, created = Experiencia.objects.get_or_create(exp=exp)
                Ex.dev.add(desenvolvedor)

            return redirect('core:detalhe_dev', desenvolvedor_id=desenvolvedor.id)
        except (KeyError):
            projetos = MProject.objects.all()
            linguagens = Linguagem.objects.all()
            args = {"projetos": projetos, "linguagens": linguagens}
            return render(request, "core/cadastrar_desenvolvedor.html", args)
    else:
        projetos = MProject.objects.all()
        linguagens = Linguagem.objects.all()
        args = {"projetos": projetos, "linguagens": linguagens}
        return render(request, "core/cadastrar_desenvolvedor.html", args)


# ...
# ...
# Area da squad

def listar_squad(request, projeto_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    args = {"projeto": projeto}
    return render(request, "core/listar_squads.html", args)


def detalhar_squad(request, projeto_id, squad_id):
    squad = get_object_or_404(Squad, pk=squad_id)
    args = {"squad": squad}

    return render(request, "core/detalhe_squad.html", args)


def cadastrar_squad(request, projeto_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    args = {"projeto": projeto}

    if request.method == "POST":
        try:
            nome = request.POST['nome']
            sprint = request.POST['sprint']
            squad = Squad(nome=nome, sprint=sprint, projeto=projeto)
            squad.save()
            return redirect("core:squads", projeto_id=projeto.id)

        except (KeyError):
            return render(request, "core/cadastrar_squad.html", args)
    else:
        return render(request, "core/cadastrar_squad.html", args)


def editar_squad(request, projeto_id, squad_id):
    squad = get_object_or_404(Squad, pk=squad_id)
    args = {"squad": squad}

    if request.method == "POST":
        try:
            squad.nome = request.POST['nome']
            squad.sprint = request.POST['sprint']
            squad.save()
            return redirect("core:squads", projeto_id=squad.projeto.id)

        except (KeyError):
            return render(request, "core/editar_squad.html", args)
    else:
        return render(request, "core/editar_squad.html", args)


def deletar_squad(request, projeto_id, squad_id):
    try:
        squad = get_object_or_404(Squad, pk=squad_id)
        squad.delete()
        return redirect('core:squads', projeto_id=projeto_id)
    except (KeyError):

        return redirect('core:squads', projeto_id=projeto_id)


# ...
# ...
# Alocação de dev para projeto

def listar_alodos(request, projeto_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    args = {"projeto": projeto, "alocados": projeto.alocacaop_set.all()}
    return render(request, "core/listar_alocacao.html", args)


def alocar_dev(request, projeto_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    # devs_mesa = MDev.objects.all().filter(alocacaop__isnull=True).filter(linguagens__in=projeto.linguagens.all())
    devs_mesa = MDev.objects.all()

    # Area de recomendacao
    recomendador = Recommender()
    # devs_do_recomendador = recomendador.recomendar_dev_para_projeto(projeto, devs_mesa).items()
    devs_do_recomendador = recomendador.recomendar_dev_para_projeto(projeto, devs_mesa)
    ids_devs_recomendados = []

    devs_recomendados = []

    for dev in devs_do_recomendador:
        devs_recomendados.append(get_object_or_404(MDev, pk=dev["id"]))
        ids_devs_recomendados.append(dev["id"])
    devs_disponiveis = MDev.objects.all().exclude(id__in=ids_devs_recomendados)

    args = {"projeto": projeto, "alocacao": projeto.alocacaop_set.all(), "devs_mesa": devs_disponiveis,
            "devs_recomendados": devs_recomendados}

    if request.method == "POST":
        try:
            devs_mesa = request.POST.getlist('devs_mesa')
            devs_recomendados = request.POST.getlist('devs_recomendados')

            for dev_selecionado in devs_mesa:
                dev = get_object_or_404(MDev, pk=dev_selecionado)
                alocar = AlocacaoP(projeto=projeto, dev=dev, squad=None)
                alocar.save()
                update_dev_data(projeto, dev)

            for dev_selecionado in devs_recomendados:
                dev = get_object_or_404(MDev, pk=dev_selecionado)
                alocar = AlocacaoP(projeto=projeto, dev=dev, squad=None)
                alocar.save()
                update_dev_data(projeto, dev)

            return redirect('core:listar_alocacao', projeto_id=projeto.id)

        except (KeyError):
            return render(request, "core/alocar_dev.html", args)
    else:
        return render(request, "core/alocar_dev.html", args)


def alocar_dev_squad(request, projeto_id, dev_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    dev = get_object_or_404(MDev, pk=dev_id)
    args = {"projeto": projeto, "dev": dev}

    if request.method == "POST":
        try:
            alocacao = get_object_or_404(AlocacaoP, projeto_id=projeto_id, dev_id=dev_id)
            squad = get_object_or_404(Squad, pk=request.POST['squad'])

            alocacao.squad = squad
            alocacao.save()

            return redirect('core:listar_alocacao', projeto_id=projeto.id)

        except (KeyError):
            return render(request, "core/alocar_dev_squad.html", args)
    else:
        return render(request, "core/alocar_dev_squad.html", args)


def remover_alocar_dev(request, projeto_id, alocacao_id):
    alocao = get_object_or_404(AlocacaoP, pk=alocacao_id)
    alocao.delete()
    return redirect('core:listar_alocacao', projeto_id=projeto_id)


# ...
# ...
# Alocação de dev para uma issue


def recomendacao(request, projeto_id):
    return HttpResponse("Tela da recomendação do projeto %s" % projeto_id)


# Funcoes
# NLTK C:\Users\vinic\AppData\Roaming\nltk_data
# def cadastrar_issue(jiraIssue):
#     print("\n\n")
#     try:
#         print(jiraIssue.key)
#         return get_object_or_404(JiraIssues, key=jiraIssue.key)
#
#     except Exception:
#         try:
#             print(jiraIssue.key)
#             key = jiraIssue.key
#             if not key:
#                 key = "No Key"
#         except Exception:
#             key = "No Key"
#             print("Key Problem")
#
#         try:
#             print(jiraIssue.fields.summary)
#             title = jiraIssue.fields.summary
#             if not title:
#                 title = "No Title"
#         except Exception:
#             title = "No Title"
#             print("Title Problem")
#
#         try:
#             print(jiraIssue.fields.description)
#             if jiraIssue.fields.description:
#                 descricao_limpa = " ".join(limpar_texto(jiraIssue.fields.description))
#                 description = descricao_limpa
#             elif jiraIssue.fields.customfield_10083:
#                 descricao_limpa = " ".join(limpar_texto(jiraIssue.fields.customfield_10083))
#                 description = descricao_limpa
#             else:
#                 description = "No Description"
#
#         except Exception:
#             description = "No Description"
#             print("Description Problem")
#
#         try:
#             print(jiraIssue.fields.customfield_10029)
#             feature = jiraIssue.fields.customfield_10029
#             if not feature:
#                 feature = "No Feature"
#         except Exception:
#             feature = "No Feature"
#             print("Feature Problem")
#
#         try:
#             print(jiraIssue.fields.priority)
#             prioridade = jiraIssue.fields.priority
#             if not prioridade:
#                 prioridade = "No Priority"
#         except Exception:
#             prioridade = "No Priority"
#             print("Priority Problem")
#
#         try:
#             print(jiraIssue.fields.customfield_10026)
#             storyPoint = jiraIssue.fields.customfield_10026
#             if not storyPoint:
#                 storyPoint = 0
#         except Exception:
#             storyPoint = 0
#             print("Story Point Problem")
#
#         issue = JiraIssues(key=key,
#                            title=title,
#                            description=description,
#                            feature=feature,
#                            storyPoint=storyPoint,
#                            prioridade=prioridade,
#                            dev=None)
#         issue.save()
#         return issue
#
#
# def limpar_texto(texto):
#
#     # Remover links
#     texto_sem_links = re.sub('http://\S+|https://\S+', '', texto)
#
#     # Tokenize o texto
#     texto_tokenizado = word_tokenize(texto_sem_links)
#
#     # Remover stopwords
#     stopwords = ['a', 'à', 'adeus', 'agora', 'aí', 'ainda', 'além', 'algo', 'alguém', 'algum', 'alguma', 'algumas',
#                  'alguns', 'ali', 'ampla', 'amplas', 'amplo', 'amplos', 'ano', 'anos', 'ante', 'antes', 'ao', 'aos',
#                  'apenas', 'apoio', 'após', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aqui', 'aquilo', 'área', 'as',
#                  'às',
#                  'assim', 'até', 'atrás', 'através', 'baixo', 'bastante', 'bem', 'boa', 'boas', 'bom', 'bons', 'breve',
#                  'cá', 'cada', 'catorze', 'cedo', 'cento', 'certamente', 'certeza', 'cima', 'cinco', 'coisa', 'coisas',
#                  'com', 'como', 'conselho', 'contra', 'contudo', 'custa', 'da', 'dá', 'dão', 'daquela', 'daquelas',
#                  'daquele', 'daqueles', 'dar', 'das', 'de', 'debaixo', 'dela', 'delas', 'dele', 'deles', 'demais',
#                  'dentro',
#                  'depois', 'desde', 'dessa', 'dessas', 'desse', 'desses', 'desta', 'destas', 'deste', 'destes', 'deve',
#                  'devem', 'devendo', 'dever', 'deverá', 'deverão', 'deveria', 'deveriam', 'devia', 'deviam', 'dez',
#                  'dezanove', 'dezasseis', 'dezassete', 'dezoito', 'dia', 'diante', 'disse', 'disso', 'disto', 'dito',
#                  'diz',
#                  'dizem', 'dizer', 'do', 'dois', 'dos', 'doze', 'duas', 'dúvida', 'e', 'é', 'ela', 'elas', 'ele',
#                  'eles',
#                  'em', 'embora', 'enquanto', 'entre', 'era', 'eram', 'éramos', 'és', 'essa', 'essas', 'esse', 'esses',
#                  'esta', 'está', 'estamos', 'estão', 'estar', 'estas', 'estás', 'estava', 'estavam', 'estávamos',
#                  'este',
#                  'esteja', 'estejam', 'estejamos', 'estes', 'esteve', 'estive', 'estivemos', 'estiver', 'estivera',
#                  'estiveram', 'estivéramos', 'estiverem', 'estivermos', 'estivesse', 'estivessem', 'estivéssemos',
#                  'estiveste', 'estivestes', 'estou', 'etc', 'eu', 'exemplo', 'faço', 'falta', 'favor', 'faz', 'fazeis',
#                  'fazem', 'fazemos', 'fazendo', 'fazer', 'fazes', 'feita', 'feitas', 'feito', 'feitos', 'fez', 'fim',
#                  'final', 'foi', 'fomos', 'for', 'fora', 'foram', 'fôramos', 'forem', 'forma', 'formos', 'fosse',
#                  'fossem',
#                  'fôssemos', 'foste', 'fostes', 'fui', 'geral', 'grande', 'grandes', 'grupo', 'há', 'haja', 'hajam',
#                  'hajamos', 'hão', 'havemos', 'havia', 'hei', 'hoje', 'hora', 'horas', 'houve', 'houvemos', 'houver',
#                  'haver', 'houvera', 'houverá', 'houveram', 'houvéramos', 'houverão', 'houverei', 'houverem',
#                  'houveremos',
#                  'houveria', 'houveriam', 'houveríamos', 'houvermos', 'houvesse', 'houvessem', 'houvéssemos', 'isso',
#                  'isto', 'já', 'la', 'lá', 'lado', 'lhe', 'lhes', 'lo', 'local', 'logo', 'longe', 'lugar', 'maior',
#                  'maioria', 'mais', 'mal', 'mas', 'máximo', 'me', 'meio', 'menor', 'menos', 'mês', 'meses', 'mesma',
#                  'mesmas', 'mesmo', 'mesmos', 'meu', 'meus', 'mil', 'minha', 'minhas', 'momento', 'muita', 'muitas',
#                  'muito', 'muitos', 'na', 'nada', 'não', 'naquela', 'naquelas', 'naquele', 'naqueles', 'nas', 'nem',
#                  'nenhum', 'nenhuma', 'nessa', 'nessas', 'nesse', 'nesses', 'nesta', 'nestas', 'neste', 'nestes',
#                  'ninguém',
#                  'nível', 'no', 'noite', 'nome', 'nos', 'nós', 'nossa', 'nossas', 'nosso', 'nossos', 'nova', 'novas',
#                  'nove', 'novo', 'novos', 'num', 'numa', 'número', 'nunca', 'o', 'obra', 'obrigada', 'obrigado',
#                  'oitava',
#                  'oitavo', 'oito', 'onde', 'ontem', 'onze', 'os', 'ou', 'outra', 'outras', 'outro', 'outros', 'para',
#                  'parece', 'parte', 'partir', 'paucas', 'pela', 'pelas', 'pelo', 'pelos', 'pequena', 'pequenas',
#                  'pequeno',
#                  'pequenos', 'per', 'perante', 'perto', 'pode', 'pude', 'pôde', 'podem', 'podendo', 'poder', 'poderia',
#                  'poderiam', 'podia', 'podiam', 'põe', 'põem', 'pois', 'ponto', 'pontos', 'por', 'porém', 'porque',
#                  'porquê', 'posição', 'possível', 'possivelmente', 'posso', 'pouca', 'poucas', 'pouco', 'poucos',
#                  'primeira', 'primeiras', 'primeiro', 'primeiros', 'própria', 'próprias', 'próprio', 'próprios',
#                  'próxima',
#                  'próximas', 'próximo', 'próximos', 'pude', 'puderam', 'quais', 'quáis', 'qual', 'quando', 'quanto',
#                  'quantos', 'quarta', 'quarto', 'quatro', 'que', 'quê', 'quem', 'quer', 'quereis', 'querem', 'queremas',
#                  'queres', 'quero', 'questão', 'quinta', 'quinto', 'quinze', 'relação', 'sabe', 'sabem', 'são', 'se',
#                  'segunda', 'segundo', 'sei', 'seis', 'seja', 'sejam', 'sejamos', 'sem', 'sempre', 'sendo', 'ser',
#                  'será',
#                  'serão', 'serei', 'seremos', 'seria', 'seriam', 'seríamos', 'sete', 'sétima', 'sétimo', 'seu', 'seus',
#                  'sexta', 'sexto', 'si', 'sido', 'sim', 'sistema', 'só', 'sob', 'sobre', 'sois', 'somos', 'sou', 'sua',
#                  'suas', 'tal', 'talvez', 'também', 'tampouco', 'tanta', 'tantas', 'tanto', 'tão', 'tarde', 'te', 'tem',
#                  'tém', 'têm', 'temos', 'tendes', 'tendo', 'tenha', 'tenham', 'tenhamos', 'tenho', 'tens', 'ter',
#                  'terá',
#                  'terão', 'terceira', 'terceiro', 'terei', 'teremos', 'teria', 'teriam', 'teríamos', 'teu', 'teus',
#                  'teve',
#                  'ti', 'tido', 'tinha', 'tinham', 'tínhamos', 'tive', 'tivemos', 'tiver', 'tivera', 'tiveram',
#                  'tivéramos',
#                  'tiverem', 'tivermos', 'tivesse', 'tivessem', 'tivéssemos', 'tiveste', 'tivestes', 'toda', 'todas',
#                  'todavia', 'todo', 'todos', 'trabalho', 'três', 'treze', 'tu', 'tua', 'tuas', 'tudo', 'última',
#                  'últimas',
#                  'último', 'últimos', 'um', 'uma', 'umas', 'uns', 'vai', 'vais', 'vão', 'vários', 'vem', 'vêm', 'vendo',
#                  'vens', 'ver', 'vez', 'vezes', 'viagem', 'vindo', 'vinte', 'vir', 'você', 'vocês', 'vos', 'vós',
#                  'vossa',
#                  'vossas', 'vosso', 'vossos', 'zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', '!', '"',
#                  '#',
#                  '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[',
#                  '\\',
#                  ']', '^', '`', '{', '|', '}', '~']
#
#     texto_sem_stopwords = [p for p in texto_tokenizado if p not in stopwords]
#
#     # Stemizar o texto
#     stemmer = RSLPStemmer()
#     texto_stemmizado = [stemmer.stem(p) for p in texto_sem_stopwords]
#
#     return texto_stemmizado
#     # print(texto_sem_stopwords)
#     # lista_de_acentos = []
#     # for c in acentos:
#     #     if c not in stopwords:
#     #         lista_de_acentos.append(c)
#
#     # print(lista_de_acentos)
#     # print(len(acentos))
#     # print(len(lista_de_acentos))
#

def update_dev_data(projeto, dev):
    mesa_jira = MesaJira()
    issues_dev = mesa_jira.get_dev_data(projeto, dev)

    for issue in issues_dev:
        issue_cadastrada = mesa_jira.cadastrar_issue(issue)
        issue_cadastrada.dev = dev
        issue_cadastrada.save()



