from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *


# Create your views here.

def projetos(request):
    projects = MProject.objects.all()
    args = {'projects': projects}
    return render(request, 'core/listar_projetos.html', args)


def detalhar_projeto(request, projeto_id):
    projeto = get_object_or_404(MProject, pk=projeto_id)
    args = {"projeto": projeto}
    return render(request, "core/detalhe_projeto.html", args)


def cadastrar_projeto(request):
    if request.method == 'POST':
        try:
            nome = request.POST['nome']
            url = request.POST['url']
            status = True if request.POST['status'] == "on" else False
            projeto = MProject(name=nome, url=url, status=status)
            projeto.save()
            # args = {"projeto_id": projeto.id}
            return redirect('core:detalhe_projeto', projeto_id=projeto.id)
        except (KeyError):
            return render(request, 'core/cadastrar_projeto.html')
    else:
        return render(request, 'core/cadastrar_projeto.html')


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
            projeto = get_object_or_404(MProject, pk=request.POST['projeto'])
            nome = request.POST['nome']
            email = request.POST['email']
            id_jira = request.POST['id_jira']
            experiencias = request.POST['experiencias']
            desenvolvedor = MDev(name=nome, email=email, project=projeto, id_jira=id_jira)
            desenvolvedor.save()

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
            args = {"projetos": projetos}
            return render(request, "core/cadastrar_desenvolvedor.html", args)
    else:
        projetos = MProject.objects.all()
        args = {"projetos": projetos}
        return render(request, "core/cadastrar_desenvolvedor.html", args)


def recomendacao(request, projeto_id):
    return HttpResponse("Tela da recomendação do projeto %s" % projeto_id)

def detalhar_squad(request, projeto_id, squad_id):
    return HttpResponse("Tela do squad do projeto %s" % squad_id)

def cadastrar_squad(request, projeto_id):
    return HttpResponse("Tela de cadastro da squad para o projeto %s" % projeto_id)

def editar_squad(request, projeto_id, squad_id):
    return HttpResponse("Tela de editar o squad {} do projeto {}".format(squad_id, projeto_id))