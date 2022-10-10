from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from .Recommender import Recommender


# Create your views here.

def projetos(request):
    projects = MProject.objects.all()
    args = {'projects': projects}
    return render(request, 'core/listar_projetos.html', args)


def detalhar_projeto(request, projeto_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    try:
        alocacao = get_list_or_404(AlocacaoP, projeto=projeto)
        args = {"projeto": projeto, "alocacao": alocacao}
    except Exception:
        args = {"projeto": projeto}

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
            experiencias = experiencias.lower().replace(".","").replace("!","").replace(";",",")
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

def editar_projeto(request,projeto_id):
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
            experiencias = experiencias.lower().replace(".","").replace("!","").replace(";",",")
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
            args = {"linguagens": linguagens, "projeto":projeto}
            return render(request, 'core/editar_projeto.html', args)
    else:
        linguagens = Linguagem.objects.all()
        args = {"linguagens": linguagens, "projeto":projeto}
        return render(request, 'core/editar_projeto.html', args)


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


def recomendacao(request, projeto_id):
    return HttpResponse("Tela da recomendação do projeto %s" % projeto_id)


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


def listar_alodos(request, projeto_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    args = {"projeto": projeto, "alocados": projeto.alocacaop_set.all()}
    return render(request, "core/listar_alocacao.html", args)

def alocar_dev(request,projeto_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    # devs_mesa = MDev.objects.all().filter(alocacaop__isnull=True).filter(linguagens__in=projeto.linguagens.all())
    devs_mesa = MDev.objects.all()

    # Area de recomendacao
    recomendador = Recommender()
    # devs_do_recomendador = recomendador.recomendar_dev_para_projeto(projeto, devs_mesa).items()
    devs_do_recomendador = recomendador.recomendar_dev_para_projeto(projeto, devs_mesa)
    ids_devs_recomendados=[]


    devs_recomendados = []

    for dev in devs_do_recomendador:
        devs_recomendados.append(get_object_or_404(MDev, pk=dev["id"]))
        ids_devs_recomendados.append(dev["id"])
    devs_disponiveis = MDev.objects.all().exclude(id__in=ids_devs_recomendados)

    args = {"projeto": projeto, "alocacao": projeto.alocacaop_set.all(), "devs_mesa": devs_disponiveis, "devs_recomendados":devs_recomendados}

    if request.method == "POST":
        try:
            devs_mesa = request.POST.getlist('devs_mesa')
            devs_recomendados = request.POST.getlist('devs_recomendados')

            for dev_selecionado in devs_mesa:
                dev = get_object_or_404(MDev, pk=dev_selecionado)
                alocar = AlocacaoP(projeto=projeto, dev=dev, squad=None)
                alocar.save()

            for dev_selecionado in devs_recomendados:
                dev = get_object_or_404(MDev, pk=dev_selecionado)
                alocar = AlocacaoP(projeto=projeto, dev=dev, squad=None)
                alocar.save()

            return redirect('core:listar_alocacao', projeto_id=projeto.id)

        except (KeyError):
            return render(request, "core/alocar_dev.html", args)
    else:
        return render(request, "core/alocar_dev.html", args)

def alocar_dev_squad(request,projeto_id,dev_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    dev = get_object_or_404(MDev,pk=dev_id)
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